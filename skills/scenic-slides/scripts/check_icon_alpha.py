"""Read-only raster icon alpha checks. Requires Pillow; never edits an image."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("Pillow is required for this read-only check: python -m pip install Pillow")


def inspect_icon(path: Path) -> dict:
    result = {"path": str(path), "status": "FAIL"}
    try:
        with Image.open(path) as image:
            if getattr(image, "n_frames", 1) != 1:
                return {**result, "reason": "Use a single-frame raster icon."}
            image.load()
            rgba = image.convert("RGBA")
            alpha = rgba.getchannel("A")
            histogram = alpha.histogram()
            width, height = rgba.size
            pixels = width * height
            visible = pixels - histogram[0]
            result.update(
                size=[width, height],
                transparent_fraction=round(histogram[0] / pixels, 6),
                visible_fraction=round(visible / pixels, 6),
                alpha_range=list(alpha.getextrema()),
            )
            if histogram[0] == 0:
                return {**result, "reason": "No fully transparent background pixels."}
            if visible == 0:
                return {**result, "reason": "The image is entirely transparent."}
            border = [alpha.getpixel((x, 0)) for x in range(width)]
            if height > 1:
                border.extend(alpha.getpixel((x, height - 1)) for x in range(width))
            for y in range(1, height - 1):
                border.append(alpha.getpixel((0, y)))
                if width > 1:
                    border.append(alpha.getpixel((width - 1, y)))
            clear_border = sum(value == 0 for value in border) / len(border)
            result.update(
                status="ALPHA_PRESENT_VISUAL_REVIEW_REQUIRED",
                transparent_border_fraction=round(clear_border, 6),
                visual_review="Inspect on light, dark and actual slide backgrounds for rectangles, halos and missing detail.",
            )
            if clear_border < 0.95:
                result["warning"] = "Visible outer-edge pixels: inspect padding, clipping and background remnants."
            return result
    except (OSError, ValueError, Image.DecompressionBombError) as error:
        return {**result, "reason": str(error)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="PNG/WebP or other single-frame raster icons")
    args = parser.parse_args()
    results = [inspect_icon(path) for path in args.paths]
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 1 if any(result["status"] == "FAIL" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
