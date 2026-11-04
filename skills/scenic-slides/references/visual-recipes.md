# Scene Composition and Generation Templates

Read this before generating assets or substantially re-laying-out slides. These are adjustable compositions, not a layout every slide must use.

## Allocate the canvas before generating

For each slide, pick one main message and scene first, then mark the subject area (people, objects or a place), the text area and the diagram area. Common starting points are 16:9, an outer margin of about 4–6%, titles at 32–40 pt and body text at 18–24 pt; fit the actual sizes to the template and viewing distance. Don't keep shrinking type to fit more words.

| Slide purpose | Background scene and open space (the subject can be people, objects or a place) | Editable foreground |
| --- | --- | --- |
| Pain point | Where the problem happens: the affected people, or objects and places such as piled-up paperwork or an idle counter, with the subject on one side | 2–3 pain points, each with a transparent icon, a short heading and its concrete impact |
| Feature response | A close-up of a workbench, tool or finished output, with detail kept away from text | How the feature answers the problem, in short lines beside transparent icons |
| Deployment architecture | An empty server room, equipment or space, with a quiet architecture area | Native system boundaries, nodes, data flows and labels |
| Agent or tool flow | A scene with a manual, tools or a workbench | Transparent icons, real function names, short descriptions and native connectors |
| Data evidence | The research or operations setting or equipment, kept out of the chart reading area | Native charts and exact figures, with a local light backing if needed |
| Model choice | A work environment, computer or server | Each option's name, where it runs and its trade-offs, without confusing model and mode |
| Closing or sources | A desk, filing cabinet or retrospective scene | A few key points or readable sources, without forcing the same row of icons |

The background must relate to the message causally or situationally; don't swap in a random office picture on every slide. Before generating, write down each slide's subject and composition, and check whether every slide has the same kind of subject (for example, a person standing on one side). Abstract topics such as code, methods or processes can be shown with desks, whiteboards, equipment or places; they don't need people. Keep one set of line work, colours and character proportions while varying the composition. Don't cram "journal-style" slides with many tiny boxes, tiny text and crossing arrows.

## Typography

Use the template's or brand's fonts when there are any. Otherwise:

| Deck | Headings | Body | Code |
| --- | --- | --- | --- |
| English, default | Aptos Display | Aptos | Consolas |
| English, when the user says it must open without Microsoft 365 (older Office, Keynote, Google Slides) | Arial or Calibri, bold | Arial or Calibri | Consolas or Courier New |
| Traditional Chinese | Microsoft JhengHei, bold | Microsoft JhengHei | Consolas |

- Aptos has been the Microsoft 365 default since 2023, so it is what most new PowerPoint decks use. It is an Office cloud font, so viewers without Microsoft 365 see a substitute. Still default to Aptos: an unspecified audience is not a reason to switch. Use Arial (installed almost everywhere) or Calibri (installed with Office) only when the user names such a viewer, and state the font in the delivery notes either way.
- Keep to one family, or two at most (for example a serif such as Georgia for display headings when the tone calls for it). Set the heading and body fonts in the theme so new text inherits them.
- Don't use operating-system interface fonts such as Segoe UI or San Francisco, which exist only on one platform, or decorative fonts for body text.
- Confirm a font is installed (Windows Fonts or Office cloud fonts) before relying on it; the layout check's `fonts_substituted` lists fonts it could not find.

## Background prompt template

Replace the bracketed parts with the slide's plan; don't hard-code a specific project, slide count or data.

```text
Purpose: a full-bleed 16:9 background for an editable professional presentation.
Scene: [one continuous scene that supports this slide's message].
Main subject: [people / objects / place / landscape chosen for this slide].
Include people only when the message is about people or their behaviour.
Style: refined flat 2D editorial illustration, consistent with [approved reference].
Composition: keep [main subject] in [the planned area]. Keep [text/diagram area]
quiet and naturally light. The environment extends to every edge of the canvas.
Palette: [coherent base and a few semantic accents].
Do not include text, letters, numbers, logos, charts, interface panels or diagram arrows.
This is contextual artwork, not a flattened slide. No 3D CGI or glossy icon rendering.
```

If a reference image contains text, icons or data, say explicitly that only its style and composition should be borrowed and that its foreground content must not be burned into the background. After generating, look at where people and details actually landed before placing native text; don't blindly reuse the ideal coordinates.

## Cross-slide consistency

Once the first background is approved, pass it in as a reference image when generating later backgrounds (when the tool supports it), and say in the prompt what to keep and what to change. When people appear, first write a one-line fixed description of each person and reuse it word for word on every slide:

```text
Use the attached approved background only as the style reference: same line quality,
palette, lighting and proportions. Do not copy its layout or objects.
[If people appear] Same characters as before: [person A: age, hair, clothing, colours];
[person B: ...]. Keep their faces, hair and clothing unchanged.
New scene: [this slide's scene, main subject and planned areas].
```

Later icons likewise use the first approved icon as the reference image, asking for the same line weight, corner rounding and palette. The provenance records which reference each image used.

## Transparent 2D icon prompt template

```text
Create one flat 2D pictogram representing [one concept].
Front-facing, consistent rounded line weight, simple solid fills,
[specified semantic colour] matching the approved icon family.
Use a genuinely transparent background with an alpha channel.
No white rectangle, coloured tile, checkerboard pattern, shadow, glow, bevel,
3D perspective, text or embedded label. Keep the whole symbol inside the canvas
with clean padding and crisp anti-aliased edges. Preserve intentional white fills
inside the symbol; only the area around the symbol should be transparent.
```

Use the image tool's `transparent_background: true` when it is available; writing "transparent" in the prompt is not enough. If the output still has a solid background, ask the generation tool for a local fix that removes only the background and keeps the shapes, lines, colours and interior whites. Don't apply a "delete every white pixel" rule that breaks documents, eyes or the inside of symbols.

Prefer one asset per icon. If the source is an icon sheet, split it into standalone, truly transparent files before inserting them one by one; never treat a whole icon sheet as an editable flowchart.

## Plan icons for parallel points

Before layout, list each slide's parallel points and the concept behind each one, then decide which icons to generate. Don't generate a few icons first and then hand them out to the points.

| Content | Icon approach |
| --- | --- |
| Milestones or timeline | One icon per node representing that stage's work, placed beside the node |
| Risks and mitigations | One icon per risk at the start of its row; the risk, its mitigation and its owner stay native text (see Rows and tables) |
| Teaching concepts or code-block roles | Icons for concepts (for example error types or each block's role), not one per line of code |
| Daily or weekly activities | One icon per day representing that day's theme; no two days share an icon |

Put all of a deck's icons on one temporary review slide to check them together on white, on dark and on the actual background.

## Foreground layout

- Keep each icon visually next to its heading, with text on a shared baseline or left edge; icons have no backing tile.
- Bind native connectors to their nodes and leave room for arrowheads. After moving nodes, re-render to catch lines that cross text, hide behind the background or point the wrong way.
- A single scene background can be a raster image; text, boundaries, arrows, legends and data charts must not be merged into an image for convenience.
- True proportions and readability of data charts come before decoration. Never use the generator to produce fake curves or text data that simulate evidence.
- Keep a recognisable part of the background visible. If the reading area is too small, first shorten the copy, change the composition or split the slide.

## Reading panels

A reading panel is a fix for text that still sits on detailed artwork (foliage, wood grain, skylines, people, equipment) or reads at low contrast, including eyebrows, captions and footers. A bare label over leaves or a grey footer on a wooden table is a defect. A box behind text that already reads well on calm sky, wall or floor is clutter: a slide where every block has its own box reads as a form, not a scene.

Decide panels per group, not per line. A group is a title, a list, a step sequence, a set of options, a diagram or a footer note, and every item in a group is treated alike. Four patterns cover most cases:

| Pattern | Use it when | Example |
| --- | --- | --- |
| No panel | The whole group sits on calm sky, wall or floor | Every title and subtitle; the pain-point list, the feature list and the sources list |
| A band behind every item | Separate items (options, steps, risks, days) with space between them run across busy art | Four tool steps, one band each: 8.6 in wide, 0.92 in tall, each a pale tint of its step's colour at 82%. Three model options, one white band each at 80% |
| One panel for the group | The group reads as one unit: a flow joined by arrows, a diagram, a pair of charts, or tightly spaced rows | Each three-step workflow on its own lane (white and pale purple, 75%); one white surface behind two charts (92%); a dashed system boundary (white, 55–75%) |
| A slim note panel | A footer or scope note crosses busy art | The note's own text box filled white at 80–90% |

- If any item of a group needs a panel, the whole group gets one treatment: a band behind every item, one panel behind all of them, or a move to a calm area. Never panel only the items that happen to overlap busy art. A band behind only the third of three options looks like a patch; give all three a band.
- Bands in one group share their left edge (the margin or the icon column) and their right edge (past the longest line), hold each item's icon, heading and detail together, and keep even gaps. Their heights may follow the content.
- Use white or a pale tint of each item's semantic colour, at about 75–92% opacity (55–75% for a dashed diagram boundary). Use square or slightly rounded corners, no heavy shadow, 0.15–0.25 in of padding around the text, and never one board over half the slide.
- Several groups on one slide can each have their own panel, as with the two workflow lanes. Titles stay bare; if a title lands on busy art, change the composition.

## Rows and tables

Where a slide lists items that each carry a sentence (options, steps, risks), every item is a row: an icon, the item's name as a heading in its semantic colour, and one or two lines of detail in body colour beneath it, with a band behind every row only where the background needs one. A table with a dark header bar, a white cell grid and banded rows is PowerPoint's default style and reads as generated rather than designed.

| Content | Layout |
| --- | --- |
| 2–5 items, each a name plus a sentence or two (risks and mitigations, options and trade-offs, partners and commitments, decisions and owners) | Rows, not a table: icon, coloured heading, detail beneath, and any owner, date or status as a small muted label |
| Values compared across and down: three or more columns of short values, numbers, a schedule, a yes/no comparison, or more than five rows | A native table, styled lightly |
| Code inputs and outputs, or "avoid / use instead" pairs | A small native table, styled lightly |

- Rows have no header row: the slide title already says what the items are, so labels like "Risk | Mitigation and owner" repeat it. Put the main detail first and the owner, date or status after it in a smaller, muted style (for example "Owner: store operations"), not as a second line in the same weight.
- Rows follow the reading-panel rules: bare on a calm area, or a matching band behind every row with shared left and right edges.
- Style a native table lightly. Start from the "No Style, No Grid" table style (`{2D5ABB26-0587-4C30-8999-92F81FD0307C}`) rather than python-pptx's or PowerPoint's default, and turn off banded rows. Set the header in small bold text in a muted or semantic colour over one thin rule, separate rows with thin horizontal rules only (no vertical lines or full grid), right-align numbers, keep about 0.1–0.15 in of cell padding, and add no card around the table unless the background is busy (then one panel, as for any group).
- If risks or options must stay in a table, each row still gets its icon in the first column.
