"""Read-only PPTX layout, text-contrast, reading-panel and table checks. Requires python-pptx; Pillow improves text estimates and enables contrast checks. Never edits a deck."""

from __future__ import annotations

import argparse
import io
import json
import math
import re
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

try:
    from lxml import etree
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    from pptx.enum.text import PP_ALIGN
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    from pptx.oxml.ns import qn
    from pptx.util import Length
except ImportError:
    raise SystemExit("python-pptx is required for this read-only check: python -m pip install python-pptx")

try:
    from PIL import Image, ImageFilter, ImageFont
except ImportError:
    Image = ImageFilter = ImageFont = None

EMU_PER_PT = 12700
PT_PER_IN = 72
LINE_HEIGHT = 1.2  # PowerPoint single spacing is 1.2 x font size for every font
WIDTH_FUDGE = 1.04  # PowerPoint lays text out slightly wider than Pillow measures
DEFAULT_SIZE = 18.0
EDGE_MARGIN = 0.1 * PT_PER_IN
MIN_CELL_LR = 0.04 * PT_PER_IN
MIN_CELL_TB = 0.02 * PT_PER_IN
TOUCH = 2.0  # overlaps smaller than this many points are treated as touching
FOOTER_ZONE = 0.88  # small text starting in the bottom 12% of the slide is a footer or footnote
FOOTER_SIZE = 14.0
FOOTER_GAP = 0.1 * PT_PER_IN
MIN_CONTRAST = 3.0  # WCAG AA for large text; below this, text is hard to read on a projector
BUSY_CONTRAST, BUSY_EDGES = 4.5, 12.0  # over busy detail (>= 12% edge pixels), ask for normal-text contrast
DARK_SHARE = 0.10  # judge contrast against the worst 10% of the background behind the text
EDGE_LEVEL = 25  # FIND_EDGES response that counts as visible detail
BG_SCALE = 2  # background samples per point
PAGE_NUMBER = re.compile(r"^\s*\d{1,3}(\s*/\s*\d{1,3})?\s*$")
PANEL_OPACITY = 0.3  # filled shapes at least this opaque count as reading panels
PANEL_MAX_SHARE = 0.5  # larger fills are overlays, not panels
ALIGN = 4.0  # list items share a left edge within this many points
LIST_STEP = 2.0 * PT_PER_IN  # and start at most this far below the previous item
LIST_MIN = 3  # two aligned blocks are too often a lead line and a separate note to call them a list
BAND_ALIGN = 0.1 * PT_PER_IN  # one band per item: the bands share left and right edges within this
LIST_TABLE_ROWS = 5  # a table of at most this many items with a sentence each reads as a list, not a grid
PROSE_WORDS = 5  # a cell of this many words (or twice as many CJK characters) holds a sentence, not a value
PLAIN_TABLE_STYLES = {"{2D5ABB26-0587-4C30-8999-92F81FD0307C}", "{5940675A-B579-460E-94D1-54222C63F5DA}"}  # No Style, No Grid / Table Grid
DARK_HEADER = 0.2  # a first-row fill darker than this luminance is a heavy header bar

CLOUD_FONT_DIR = Path.home() / "AppData/Local/Microsoft/FontCache/4/CloudFonts"  # Office cloud fonts such as Aptos
FONT_DIRS =[Path("C:/Windows/Fonts"), Path.home() / "AppData/Local/Microsoft/Windows/Fonts",
             Path("/Library/Fonts"), Path("/System/Library/Fonts"), Path.home() / "Library/Fonts",
             Path("/usr/share/fonts")]
FONT_FILES = {
    "microsoft jhenghei": ("msjh.ttc", "msjhbd.ttc"), "microsoft jhenghei ui": ("msjh.ttc", "msjhbd.ttc"),
    "微軟正黑體": ("msjh.ttc", "msjhbd.ttc"), "microsoft yahei": ("msyh.ttc", "msyhbd.ttc"),
    "微软雅黑": ("msyh.ttc", "msyhbd.ttc"), "pmingliu": ("mingliu.ttc", "mingliub.ttc"),
    "新細明體": ("mingliu.ttc", "mingliub.ttc"), "consolas": ("consola.ttf", "consolab.ttf"),
    "arial": ("arial.ttf", "arialbd.ttf"), "calibri": ("calibri.ttf", "calibrib.ttf"),
    "segoe ui": ("segoeui.ttf", "segoeuib.ttf"), "times new roman": ("times.ttf", "timesbd.ttf"),
    "segoe ui semibold": ("seguisb.ttf", "segoeuib.ttf"), "segoe ui semilight": ("segoeuisl.ttf", "seguisb.ttf"),
    "segoe ui light": ("segoeuil.ttf", "segoeuib.ttf"), "segoe ui black": ("seguibl.ttf", "seguibl.ttf"),
    "calibri light": ("calibril.ttf", "calibrib.ttf"), "cambria": ("cambria.ttc", "cambriab.ttf"),
    "georgia": ("georgia.ttf", "georgiab.ttf"), "verdana": ("verdana.ttf", "verdanab.ttf"),
    "tahoma": ("tahoma.ttf", "tahomabd.ttf"), "trebuchet ms": ("trebuc.ttf", "trebucbd.ttf"),
    "century gothic": ("GOTHIC.TTF", "GOTHICB.TTF"), "garamond": ("GARA.TTF", "GARABD.TTF"),
    "palatino linotype": ("pala.ttf", "palab.ttf"), "franklin gothic medium": ("framd.ttf", "framd.ttf"),
    "bahnschrift": ("bahnschrift.ttf", "bahnschrift.ttf"), "aptos": ("Aptos.ttf", "Aptos-Bold.ttf"),
    "cascadia code": ("CascadiaCode.ttf", "CascadiaCode.ttf"), "cascadia mono": ("CascadiaMono.ttf", "CascadiaMono.ttf"),
}
FALLBACK_FILES = ("msjh.ttc", "msyh.ttc", "PingFang.ttc", "NotoSansCJK-Regular.ttc", "arial.ttf", "DejaVuSans.ttf")
WIDE = "\u2e80-\u9fff\uf900-\ufaff\ufe30-\ufe4f\uff00-\uffef\u3000-\u303f"
TOKEN = re.compile(f"[{WIDE}]|[^\\s{WIDE}]+\\s*|\\s+")


@lru_cache(maxsize=None)
def find_font_file(filename: str) -> Path | None:
    for folder in FONT_DIRS:
        if not folder.is_dir():
            continue
        if (folder / filename).exists():
            return folder / filename
        if folder == Path("/usr/share/fonts"):
            return next(folder.rglob(filename), None)
    return None


@lru_cache(maxsize=None)
def cloud_font_file(family: str, bold: bool) -> Path | None:
    """Office stores downloaded cloud fonts under numbered file names; pick the face by its internal style name."""
    if ImageFont is None or not family or not CLOUD_FONT_DIR.is_dir():
        return None
    folder = next((d for d in CLOUD_FONT_DIR.iterdir() if d.name.lower() == family.lower()), None)
    faces, family_words = {}, set(family.lower().split()) | {"regular"}
    for path in folder.glob("*.tt[fc]") if folder else ():
        try:
            style = ImageFont.truetype(str(path), 10).getname()[1].lower()  # e.g. "Display Bold" for Aptos Display
        except OSError:
            continue
        faces[frozenset(style.split()) - family_words] = path
    return faces.get(frozenset({"bold"} if bold else ())) or faces.get(frozenset()) or next(iter(faces.values()), None)


SUBSTITUTED: set[str] = set()


@lru_cache(maxsize=None)
def load_font(family: str, bold: bool):
    if ImageFont is None:
        return None
    names = FONT_FILES.get(family.lower(), ())
    candidates = ([names[1]] if bold and names else []) + list(names[:1])
    cloud = None if any(find_font_file(name) for name in candidates) else cloud_font_file(family, bold)
    if cloud:
        return ImageFont.truetype(str(cloud), 400)
    if family and not family.startswith("+") and not any(find_font_file(name) for name in candidates):
        SUBSTITUTED.add(family)
    for filename in candidates + list(FALLBACK_FILES):
        path = find_font_file(filename)
        if path:
            return ImageFont.truetype(str(path), 400)  # measured at 400 px, scaled per run
    return None


def text_width(text: str, size: float, family: str, bold: bool) -> float:
    font = load_font(family, bold)
    if font is None:
        width = sum(size if re.match(f"[{WIDE}]", ch) else 0.55 * size for ch in text)
    else:
        width = font.getlength(text) * size / 400
    return width * WIDTH_FUDGE


@dataclass
class Item:
    kind: str  # text, picture, block
    name: str
    box: tuple  # x0, y0, x1, y1 in points
    ink: tuple  # visible text or image area in points
    size: float = 0.0
    detail: str = ""
    panel: int | None = None  # index of the reading panel behind the text, if any


def group_transform(shape, outer):
    xfrm = shape._element.find(qn("p:grpSpPr")).find(qn("a:xfrm"))
    if xfrm is None or xfrm.find(qn("a:chExt")) is None:
        return outer
    off, ext = xfrm.find(qn("a:off")), xfrm.find(qn("a:ext"))
    ch_off, ch_ext = xfrm.find(qn("a:chOff")), xfrm.find(qn("a:chExt"))
    sx = int(ext.get("cx")) / (int(ch_ext.get("cx")) or 1)
    sy = int(ext.get("cy")) / (int(ch_ext.get("cy")) or 1)
    tx = int(off.get("x")) - int(ch_off.get("x")) * sx
    ty = int(off.get("y")) - int(ch_off.get("y")) * sy
    osx, osy, otx, oty = outer
    return sx * osx, sy * osy, tx * osx + otx, ty * osy + oty


def iter_shapes(shapes, transform=(1.0, 1.0, 0.0, 0.0)):
    for shape in shapes:
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from iter_shapes(shape.shapes, group_transform(shape, transform))
        else:
            yield shape, transform


def shape_box(shape, transform):
    if None in (shape.left, shape.top, shape.width, shape.height):
        return None
    sx, sy, tx, ty = transform
    x0, y0 = shape.left * sx + tx, shape.top * sy + ty
    return (x0 / EMU_PER_PT, y0 / EMU_PER_PT,
            (x0 + shape.width * sx) / EMU_PER_PT, (y0 + shape.height * sy) / EMU_PER_PT)


def run_style(r_pr, defaults):
    size, family, east, bold = defaults
    if r_pr is not None:
        size = int(r_pr.get("sz")) / 100 if r_pr.get("sz") else size
        bold = r_pr.get("b") in ("1", "true") if r_pr.get("b") else bold
        latin, ea = r_pr.find(qn("a:latin")), r_pr.find(qn("a:ea"))
        family = latin.get("typeface") if latin is not None else family
        east = ea.get("typeface") if ea is not None else east
    return size, family, east, bold


def frame_defaults(body):
    lvl1 = body.find(qn("a:lstStyle"))
    lvl1 = lvl1.find(qn("a:lvl1pPr")) if lvl1 is not None else None
    def_r_pr = lvl1.find(qn("a:defRPr")) if lvl1 is not None else None
    return run_style(def_r_pr, (DEFAULT_SIZE, "", "", False))


def paragraph_lines(paragraph, defaults, avail, wrap, scale):
    """Return (line widths, font size) for one paragraph using greedy wrapping."""
    p_pr = paragraph._p.find(qn("a:pPr"))
    if p_pr is not None and p_pr.find(qn("a:defRPr")) is not None:
        defaults = run_style(p_pr.find(qn("a:defRPr")), defaults)
    lines, width, size_max = [], 0.0, 0.0
    for child in paragraph._p:
        tag = child.tag.split("}")[1]
        if tag == "br":
            lines.append(width)
            width = 0.0
            continue
        if tag not in ("r", "fld"):
            continue
        size, family, east, bold = run_style(child.find(qn("a:rPr")), defaults)
        size *= scale
        size_max = max(size_max, size)
        segments = re.split(r"[\r\n\v]", child.findtext(qn("a:t")) or "")
        tokens = []
        for number, segment in enumerate(segments):
            tokens += (["\n"] if number else []) + TOKEN.findall(segment)
        for token in tokens:
            if token == "\n":  # a literal line break inside the run text
                lines.append(width)
                width = 0.0
                continue
            if token.isspace() and width == 0:
                continue
            face = east if east and re.match(f"[{WIDE}]", token) else family
            token_w = text_width(token, size, face or east or family, bold)
            if wrap and width + token_w > avail and width > 0:
                lines.append(width)
                width = 0.0
                if token.isspace():
                    continue
            if wrap and token_w > avail and width == 0:
                lines.extend([avail] * int(token_w // avail))
                token_w = token_w % avail
            width += token_w
    lines.append(width)
    if size_max == 0:
        end = paragraph._p.find(qn("a:endParaRPr"))
        size_max = run_style(end, defaults)[0] * scale
    return lines, size_max


def text_item(shape, box) -> Item | None:
    if not shape.has_text_frame or not shape.text_frame.text.strip():
        return None
    body = shape.text_frame._txBody
    body_pr = body.find(qn("a:bodyPr"))
    if body_pr.get("vert") not in (None, "horz") or shape.rotation:
        return None
    ins = [int(body_pr.get(k, d)) / EMU_PER_PT for k, d in
           (("lIns", 91440), ("tIns", 45720), ("rIns", 91440), ("bIns", 45720))]
    wrap = body_pr.get("wrap") != "none"
    scale, spacing_cut = 1.0, 0.0
    norm = body_pr.find(qn("a:normAutofit"))
    if norm is not None:
        scale = int(norm.get("fontScale", 100000)) / 100000
        spacing_cut = int(norm.get("lnSpcReduction", 0)) / 100000
    x0, y0, x1, y1 = box
    avail_w = max(x1 - x0 - ins[0] - ins[2], 1.0)
    avail_h = y1 - y0 - ins[1] - ins[3]
    defaults = frame_defaults(body)
    height, left, right, size_max = 0.0, math.inf, -math.inf, 0.0
    for paragraph in shape.text_frame.paragraphs:
        widths, size = paragraph_lines(paragraph, defaults, avail_w, wrap, scale)
        size_max = max(size_max, size)
        spacing = paragraph.line_spacing
        if isinstance(spacing, Length):
            height += len(widths) * spacing.pt
        else:
            multiple = max((spacing or 1.0) - spacing_cut, 0.5)
            height += LINE_HEIGHT * size * (1 + (len(widths) - 1) * multiple) + 0.6 * size * (multiple - 1)
        for gap in (paragraph.space_before, paragraph.space_after):
            height += gap.pt if gap is not None else 0.0
        for line_w in widths:
            align = paragraph.alignment
            if align == PP_ALIGN.CENTER:
                start = x0 + ins[0] + (avail_w - line_w) / 2
            elif align == PP_ALIGN.RIGHT:
                start = x1 - ins[2] - line_w
            else:
                start = x0 + ins[0]
            left, right = min(left, start), max(right, start + line_w)
    anchor = body_pr.get("anchor", "t")
    if anchor == "ctr":
        top = y0 + ins[1] + (avail_h - height) / 2
    elif anchor == "b":
        top = y1 - ins[3] - height
    else:
        top = y0 + ins[1]
    overflow = ""
    if body_pr.find(qn("a:spAutoFit")) is None and height > avail_h + 0.3 * LINE_HEIGHT * size_max:
        overflow = f"estimated text height {height / PT_PER_IN:.2f} in > available {max(avail_h, 0) / PT_PER_IN:.2f} in"
    elif body_pr.find(qn("a:spAutoFit")) is not None and height > avail_h + 0.3 * LINE_HEIGHT * size_max:
        overflow = f"auto-fit box is shorter than its text ({height / PT_PER_IN:.2f} in > {max(avail_h, 0) / PT_PER_IN:.2f} in); re-render to confirm"
    return Item("text", shape.name, box, (left, top, right, top + height), size_max, overflow)


def picture_ink(shape, box):
    """Visible (non-transparent) area of a picture, mapped through its crop onto the slide."""
    if Image is None:
        return box
    try:
        with Image.open(io.BytesIO(shape.image.blob)) as image:
            image.load()
            alpha = image.convert("RGBA").getchannel("A") if "A" in image.getbands() or image.mode == "P" else None
            bbox = alpha.getbbox() if alpha else (0, 0, image.width, image.height)
            width, height = image.size
    except Exception:
        return box
    if not bbox:
        return box
    cl, cr, ct, cb = shape.crop_left, shape.crop_right, shape.crop_top, shape.crop_bottom
    span_x, span_y = (1 - cl - cr) or 1, (1 - ct - cb) or 1
    x0, y0, x1, y1 = box

    def map_x(px):
        return x0 + min(max((px / width - cl) / span_x, 0), 1) * (x1 - x0)

    def map_y(py):
        return y0 + min(max((py / height - ct) / span_y, 0), 1) * (y1 - y0)

    return map_x(bbox[0]), map_y(bbox[1]), map_x(bbox[2]), map_y(bbox[3])


def has_visible_frame(shape) -> bool:
    try:
        fill = shape.fill.type is not None and shape.fill.type != 5  # 5 = no fill
        line = shape.line.fill.type is not None and shape.line.fill.type != 5
        return fill or line
    except Exception:
        return False


def intersection(a, b):
    return min(a[2], b[2]) - max(a[0], b[0]), min(a[3], b[3]) - max(a[1], b[1])


def inches(value: float) -> float:
    return round(value / PT_PER_IN, 2)


def theme_colours(slide) -> dict:
    """Map scheme colour names (dk1, lt1, accent1, tx1, bg1, ...) to RGB from the slide master's theme."""
    try:
        root = etree.fromstring(slide.slide_layout.slide_master.part.part_related_by(RT.THEME).blob)
    except Exception:
        return {}
    colours = {}
    scheme = root.find(".//" + qn("a:clrScheme"))
    for entry in scheme if scheme is not None else ():
        value = entry[0].get("val") if entry[0].tag == qn("a:srgbClr") else entry[0].get("lastClr")
        if value:
            colours[entry.tag.split("}")[1]] = value
    for alias, name in (("tx1", "dk1"), ("bg1", "lt1"), ("tx2", "dk2"), ("bg2", "lt2")):
        if name in colours:
            colours[alias] = colours[name]
    return colours


def solid_fill(parent, theme):
    """(r, g, b, opacity) of a solidFill under parent, or None."""
    fill = parent.find(qn("a:solidFill")) if parent is not None else None
    if fill is None or not len(fill):
        return None
    colour = fill[0]
    value = colour.get("val") if colour.tag == qn("a:srgbClr") else theme.get(colour.get("val"), colour.get("lastClr"))
    if not value or len(value) != 6:
        return None
    alpha = colour.find(qn("a:alpha"))
    return (*(int(value[i:i + 2], 16) for i in (0, 2, 4)), int(alpha.get("val")) / 100000 if alpha is not None else 1.0)


def text_colour(shape, theme):
    """Colour of the first visible run, following run, paragraph and frame defaults; theme text colour otherwise."""
    lvl1 = shape.text_frame._txBody.find(qn("a:lstStyle"))
    lvl1 = lvl1.find(qn("a:lvl1pPr")) if lvl1 is not None else None
    for paragraph in shape.text_frame.paragraphs:
        p_pr = paragraph._p.find(qn("a:pPr"))
        for run in paragraph._p.findall(qn("a:r")):
            if not (run.findtext(qn("a:t")) or "").strip():
                continue
            for source in (run.find(qn("a:rPr")), p_pr.find(qn("a:defRPr")) if p_pr is not None else None,
                           lvl1.find(qn("a:defRPr")) if lvl1 is not None else None):
                colour = solid_fill(source, theme)
                if colour:
                    return colour[:3]
            break
    value = theme.get("tx1", "000000")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb) -> float:
    """WCAG relative luminance of an sRGB colour."""
    def channel(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


GRAY_LUMINANCE = [luminance((v, v, v)) for v in range(256)]


def background_canvas(shape, box, slide_w, slide_h):
    """The full-slide picture drawn onto a slide-sized canvas, honouring its crop."""
    try:
        with Image.open(io.BytesIO(shape.image.blob)) as image:
            picture = image.convert("RGB")
    except Exception:
        return None
    w, h = picture.size
    picture = picture.crop((round(shape.crop_left * w), round(shape.crop_top * h),
                            round((1 - shape.crop_right) * w), round((1 - shape.crop_bottom) * h)))
    canvas = Image.new("RGB", (round(slide_w * BG_SCALE), round(slide_h * BG_SCALE)), "white")
    x0, y0, x1, y1 = (round(v * BG_SCALE) for v in box)
    canvas.paste(picture.resize((max(x1 - x0, 1), max(y1 - y0, 1))), (x0, y0))
    return canvas


def blend_panel(canvas, box, fill):
    """Composite a filled shape (a reading panel or a boxed label) over the canvas."""
    r, g, b, opacity = fill
    x0, y0, x1, y1 = (round(v * BG_SCALE) for v in box)
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, canvas.width), min(y1, canvas.height)
    if x1 <= x0 or y1 <= y0:
        return
    region = canvas.crop((x0, y0, x1, y1))
    canvas.paste(Image.blend(region, Image.new("RGB", region.size, (r, g, b)), opacity), (x0, y0))


def background_behind(canvas, ink, colour):
    """(contrast, busy %) for text over the canvas.

    Contrast is measured against the worst DARK_SHARE of the background behind the text; busy % is the share of
    pixels on a visible edge (leaves, wood grain, skylines) after any panels have been composited."""
    x0, y0, x1, y1 = (round(v * BG_SCALE) for v in ink)
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, canvas.width), min(y1, canvas.height)
    if x1 - x0 < 3 or y1 - y0 < 3:
        return None
    region = canvas.crop((x0, y0, x1, y1)).convert("L")
    histogram = region.histogram()
    total, text_lum = sum(histogram), luminance(colour)
    levels = range(256) if text_lum < 0.18 else range(255, -1, -1)  # dark text fears dark detail, light text fears light
    seen, contrast = 0, None
    for level in levels:
        seen += histogram[level]
        if seen >= DARK_SHARE * total:
            bg_lum = GRAY_LUMINANCE[level]
            contrast = (max(bg_lum, text_lum) + 0.05) / (min(bg_lum, text_lum) + 0.05)
            break
    edges = region.filter(ImageFilter.FIND_EDGES).histogram()
    busy = 100 * sum(edges[EDGE_LEVEL:]) / total
    return contrast, busy


def parallel_groups(texts):
    """Text blocks stacked like list items: the same left edge and font size, each close below the last."""
    groups = []
    for item in sorted(texts, key=lambda t: t.ink[1]):
        for group in groups:
            last = group[-1]
            if abs(last.ink[0] - item.ink[0]) <= ALIGN and abs(last.size - item.size) <= 0.5 \
                    and 0 < item.ink[1] - last.ink[1] <= LIST_STEP:
                group.append(item)
                break
        else:
            groups.append([item])
    return [group for group in groups if len(group) >= LIST_MIN]


def is_prose(text: str) -> bool:
    return len(re.findall(r"[^\W\d_]+", text)) >= PROSE_WORDS or len(re.findall(f"[{WIDE}]", text)) >= 2 * PROSE_WORDS


def table_findings(table, theme):
    """(check, detail) for a short list set as a table, or else a table left in PowerPoint's default style."""
    tbl_pr = table._tbl.tblPr
    flags = {key for key in ("firstRow", "bandRow") if tbl_pr is not None and tbl_pr.get(key) in ("1", "true")}
    rows = list(table.rows)
    body = rows[1:] if "firstRow" in flags else rows
    if 2 <= len(body) <= LIST_TABLE_ROWS and len(table.columns) <= 3 \
            and any(is_prose(cell.text) for row in body for cell in list(row.cells)[1:]):  # a sentence may be broken by hand
        return ("list_as_table",
                f"{len(body)} items with sentences in the cells read as a list, not a grid: set them as rows (icon, the name "
                "as a heading in its colour, the detail beneath, an owner or date as a small label) with no header row, "
                "or say in the delivery notes why viewers must read it across and down")
    fills = [solid_fill(cell._tc.tcPr, theme) for cell in rows[0].cells] if len(rows) > 1 else []
    style = tbl_pr.findtext(qn("a:tableStyleId")) if tbl_pr is not None else None
    if any(f and f[3] >= 0.5 and luminance(f[:3]) < DARK_HEADER for f in fills):
        looks = "a dark header bar"
    elif flags and style not in PLAIN_TABLE_STYLES:
        looks = "a built-in style's header-row or banded-row formatting and cell grid"
    else:
        return None
    return ("default_table_style",
            f"the table keeps PowerPoint's default look ({looks}): use the No Style, No Grid table style, a small bold "
            "header in a muted or semantic colour over one thin rule, and thin horizontal rules between rows")


def check_slide(slide, number, slide_w, slide_h):
    findings, items, panels, listed = [], [], [], []  # panels: (name, box) of filled shapes, back to front

    def add(level, check, names, detail):
        findings.append({"slide": number, "level": level, "check": check, "shapes": names, "detail": detail})

    theme = theme_colours(slide)
    canvas = None  # what lies behind the next shape: the background plus panels drawn so far
    for shape, transform in iter_shapes(slide.shapes):
        box = shape_box(shape, transform)
        if box is None:
            continue
        if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
            area = (box[2] - box[0]) * (box[3] - box[1])
            if area < 0.9 * slide_w * slide_h:
                items.append(Item("picture", shape.name, box, picture_ink(shape, box)))
            elif Image is not None:
                canvas = background_canvas(shape, box, slide_w, slide_h)
            continue
        if getattr(shape, "has_table", False) and shape.has_table:
            items.append(Item("block", shape.name, box, box))
            cells = [cell for row in shape.table.rows for cell in row.cells]
            lr = min(min(c.margin_left, c.margin_right) for c in cells) / EMU_PER_PT
            tb = min(min(c.margin_top, c.margin_bottom) for c in cells) / EMU_PER_PT
            if lr < MIN_CELL_LR or tb < MIN_CELL_TB:
                add("issue", "table_cell_padding", [shape.name],
                    f"smallest cell padding left/right {inches(lr)} in, top/bottom {inches(tb)} in; text will touch the cell borders")
            found = table_findings(shape.table, theme)
            if found:
                add("check", found[0], [shape.name], found[1])
            continue
        if getattr(shape, "has_chart", False) and shape.has_chart:
            items.append(Item("block", shape.name, box, box))
            continue
        fill = solid_fill(shape._element.find(qn("p:spPr")), theme)
        if canvas is not None and fill:
            blend_panel(canvas, box, fill)
        if fill and fill[3] >= PANEL_OPACITY and (box[2] - box[0]) * (box[3] - box[1]) < PANEL_MAX_SHARE * slide_w * slide_h:
            panels.append((shape.name, box))
        item = text_item(shape, box)
        if item is None:
            continue
        items.append(item)
        cx, cy = (item.ink[0] + item.ink[2]) / 2, (item.ink[1] + item.ink[3]) / 2
        item.panel = next((i for i in reversed(range(len(panels)))
                           if panels[i][1][0] <= cx <= panels[i][1][2] and panels[i][1][1] <= cy <= panels[i][1][3]), None)
        if item.detail:
            add("issue", "possible_text_overflow", [shape.name], item.detail)
        page_number = PAGE_NUMBER.match(shape.text_frame.text)  # the user accepts slide numbers over artwork
        if not page_number:
            listed.append(item)
        behind = background_behind(canvas, item.ink, text_colour(shape, theme)) if canvas is not None and not page_number else None
        if behind and behind[0] is not None:
            contrast, busy = behind
            if contrast < MIN_CONTRAST or (contrast < BUSY_CONTRAST and busy >= BUSY_EDGES):
                add("check", "text_contrast", [shape.name],
                    f"contrast {contrast:.1f}:1 against the worst 10% of the background behind the text, "
                    f"{busy:.0f}% of it busy detail; move the text to a calmer area or give it a local panel "
                    "(if it is one item of a list, treat the whole list alike: see partial_panel_group)")
        side = min(item.ink[0] - box[0], box[2] - item.ink[2])
        if has_visible_frame(shape) and side < MIN_CELL_LR:
            add("check", "boxed_text_padding", [shape.name],
                f"text comes within {inches(max(side, 0))} in of its filled or outlined shape's edge")

    texts = [i for i in items if i.kind == "text"]
    for item in texts:
        x0, y0, x1, y1 = item.ink
        if x0 < -TOUCH or y0 < -TOUCH or x1 > slide_w + TOUCH or y1 > slide_h + TOUCH:
            add("issue", "text_outside_slide", [item.name], "estimated text area extends past the slide edge")
        elif min(x0, y0, slide_w - x1, slide_h - y1) < EDGE_MARGIN:
            add("check", "text_near_edge", [item.name],
                f"text is {inches(min(x0, y0, slide_w - x1, slide_h - y1))} in from the slide edge")

    for index, a in enumerate(texts):
        for b in texts[index + 1:]:
            over_x, over_y = intersection(a.ink, b.ink)
            if over_x > TOUCH and over_y > TOUCH:
                add("issue", "text_overlap", [a.name, b.name],
                    f"estimated text areas overlap by {inches(over_x)} x {inches(over_y)} in")

    footers = [t for t in texts if t.ink[1] >= FOOTER_ZONE * slide_h and t.size <= FOOTER_SIZE]
    for footer in footers:
        for text in texts:
            if text in footers or text.ink[1] >= footer.ink[1]:
                continue
            over_x, over_y = intersection(text.ink, footer.ink)
            if over_x > TOUCH and -over_y < FOOTER_GAP:
                add("check", "footer_crowded", [text.name, footer.name],
                    f"content ends {inches(max(-over_y, 0))} in above the footer or footnote")

    reported = set()
    for group in parallel_groups([t for t in listed if t not in footers]):
        on = [t for t in group if t.panel is not None]
        used = sorted({t.panel for t in on})
        if not used or frozenset(used) in reported:  # headings and details of one list share the same panels
            continue
        reported.add(frozenset(used))
        if len(on) < len(group):
            add("check", "partial_panel_group", [t.name for t in group],
                f"{len(on)} of {len(group)} aligned items sit on a reading panel ({', '.join(t.name for t in on)}); "
                "treat the group alike: a matching band behind every item, one panel behind the whole group, "
                "or move the group so no item needs one")
        elif len(used) > 1:
            lefts, rights = [panels[i][1][0] for i in used], [panels[i][1][2] for i in used]
            spread = max(max(lefts) - min(lefts), max(rights) - min(rights))
            if spread > BAND_ALIGN:
                add("check", "uneven_panel_bands", [panels[i][0] for i in used],
                    f"the bands behind one aligned group differ by up to {inches(spread)} in at their left or right edge; "
                    "give them one shared left and right edge")

    for other in (i for i in items if i.kind in ("picture", "block")):
        for text in texts:
            if other.kind == "block" and text.box[0] >= other.box[0] and text.box[2] <= other.box[2] \
                    and text.box[1] >= other.box[1] and text.box[3] <= other.box[3]:
                continue
            over_x, over_y = intersection(other.ink, text.ink)
            if over_x > TOUCH and over_y > TOUCH:
                label = "image_text_overlap" if other.kind == "picture" else "block_text_overlap"
                add("check", label, [other.name, text.name],
                    f"visible area overlaps text by {inches(over_x)} x {inches(over_y)} in")
    return findings


def inspect_deck(path: Path) -> dict:
    result = {"path": str(path), "status": "FAIL"}
    try:
        deck = Presentation(str(path))
    except Exception as error:
        return {**result, "reason": f"Cannot open deck: {error}"}
    slide_w, slide_h = deck.slide_width / EMU_PER_PT, deck.slide_height / EMU_PER_PT
    SUBSTITUTED.clear()
    load_font.cache_clear()
    findings = [f for n, slide in enumerate(deck.slides, 1) for f in check_slide(slide, n, slide_w, slide_h)]
    issues = sum(f["level"] == "issue" for f in findings)
    result.update(
        status="GEOMETRY_FINDINGS_REVIEW_REQUIRED" if findings else "NO_GEOMETRY_FINDINGS_VISUAL_REVIEW_REQUIRED",
        slides=len(deck.slides), issues=issues, checks=len(findings) - issues,
        text_estimate="font metrics" if load_font("", False) else "character-width heuristic",
        fonts_substituted=sorted(SUBSTITUTED),
        findings=findings,
        visual_review="Text sizes are estimated from fonts, not rendered. Confirm every finding on the exported slide image; a clean result does not replace visual review.",
    )
    return result


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="PPTX files to inspect")
    args = parser.parse_args()
    results = [inspect_deck(path) for path in args.paths]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 1 if any(r["status"] == "FAIL" or r.get("issues") for r in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
