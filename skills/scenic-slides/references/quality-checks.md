# Pre-delivery Quality Checks

Check what the presentation app actually renders. Code that ran, a shape count or well-formed JSON is not enough.

## Required checks

- **Narrative:** the concrete problem, the matching features and the evidence are visible. Limitations and future features are labelled, and selling points don't rest on false comparisons.
- **Background:** each slide has a relevant full-slide scene, not just a corner illustration. People and equipment don't cross important text or chart axes, and the light reading area doesn't hide the whole background. Lay all of the deck's backgrounds out together: the subject changes with the topic and the slide's purpose instead of being a person on one side and an empty wall on every slide, and people appear only on slides where they relate to the message.
- **Consistency:** later backgrounds match the reference in art style, palette and proportions, and the same character keeps the same face, hair and clothing across slides. Later icons match the first icon's line weight, corner rounding and palette.
- **Icons:** truly transparent, 2D, consistent in line weight and sharp. View them at least once on the actual background, on white and on dark, and look for white boxes, checkerboards, white or black fringes, missing strokes or cut-out interior whites. A temporary review slide with different backgrounds can help; don't leave it in the delivered deck.
- **Icon coverage:** list each slide's groups of 2–5 parallel points (pain points, steps, milestones, risks, options, etc.) and confirm that every point has an icon that fits its meaning and that no icon stands for different points. Code, data charts and the values in a genuine data grid are exceptions; risks, options or partners put in a table are not. For parallel points without icons, write the slide number and the reason in the delivery notes, for example "slide 3 is a code example"; a missing reason means the check fails.
- **Text:** editable and readable at normal presentation size, with no overflow, clipping, squashing, bad line breaks or needlessly tiny footnotes. Every block, including labels, captions and footers, stands clear of the background: enough contrast and no busy detail running through it, or else a reading panel. Every item of a list, step sequence or option set is treated alike: no panels, a matching band behind each item, or one panel behind the group. Fonts follow the template or the typography section of visual-recipes.md. Essential information can't rely on the narration alone.
- **Rows and tables:** parallel items that each carry a sentence are rows with icons, not a table with a header row. A native table holds a real grid and is styled lightly: no dark header bar, banded rows or cell grid.
- **Relationships:** arrows point the right way, don't cross text and don't point at empty space, and flows can be read directly. Architecture boundaries and data movement are placed meaningfully.
- **Data:** values, units, denominators, ranges and sources agree. Native charts and their embedded data stay editable; when the data wasn't meant to change, compare it series by series against the source, not just the totals.
- **Preservation:** slides the user asked to keep and their new adjustments aren't overwritten; compare before-and-after shape lists or the source and output slide XML. When the job is only skill work, don't fix the deck on the side.

## Read-only alpha check

Run from this skill folder (or replace `scripts/` with this skill's full path):

```sh
python scripts/check_icon_alpha.py path/to/icon.png path/to/other.webp
```

It requires Pillow. The script only reads images: it doesn't remove backgrounds, overwrite files or create new images.

- `ALPHA_PRESENT_VISUAL_REVIEW_REQUIRED`: fully transparent pixels and visible artwork both exist. This only means the technical precondition is met.
- `FAIL`: there is no transparent background, no visible artwork, or the file can't be read; don't claim the file's background has been removed.
- Low transparency along the outer edge produces a warning to check the cropping or a backing tile; no pixels are deleted automatically.
- A white box surrounded by transparent edges can still pass the alpha check, so the light-and-dark visual check is still required. Don't shorten the tool's status to "background removal passed".

Without Pillow, use an existing tool that reads alpha and do the same visual check; a PNG extension or a pure white background is not evidence of transparency. For SVG, check for a background rectangle and view it in the presentation app instead of passing it to this raster checker.

## Read-only layout check

After each preview export, run from this skill folder (or replace `scripts/` with this skill's full path):

```sh
python scripts/check_layout.py path/to/deck.pptx
```

It requires python-pptx; with Pillow it estimates text width from the actual fonts (including Office cloud fonts such as Aptos), reads each icon's transparent extent and samples the background behind each text box. The script only reads the deck: it doesn't modify or save it.

- `issue`: possible overflow, overlapping text, text outside the slide, or table cells without padding. Fix these by default.
- `check`: text within 0.1 in of the slide edge, the visible part of an icon over text, content within 0.1 in of the footer or footnote, or boxed text touching its frame. Judge each from the preview, then fix it or write the reason for keeping it.
- `text_contrast` (a `check`): with any panels composited, the text colour against the worst 10% of the background behind it falls below 3:1, or below 4.5:1 where at least 12% of that area is busy detail. Move the text to a calmer area or give it a panel; when it is one item of a list, treat the whole list alike. Slide numbers are not checked.
- `partial_panel_group` (a `check`): three or more blocks with the same left edge and font size, stacked like list items, where only some sit on a reading panel. Put a matching band behind every item, one panel behind the whole group, or move the group so none needs one. If the blocks are not one list (for example a lead line above a list), say so in the delivery notes.
- `uneven_panel_bands` (a `check`): the bands behind one aligned group differ by more than 0.1 in at their left or right edge. Give them one shared left and right edge.
- `list_as_table` (a `check`): a native table of two to five items and at most three columns, with sentences in its cells. Set the items as rows (icon, the name as a heading in its colour, the detail beneath, an owner or date as a small label) with no header row, or say in the delivery notes why viewers must read it across and down.
- `default_table_style` (a `check`): a native table that keeps a built-in style's header-row or banded-row formatting, or has a dark filled header row. Switch to the No Style, No Grid style, with a small coloured header over one thin rule and thin horizontal rules between rows.
- `NO_GEOMETRY_FINDINGS_VISUAL_REVIEW_REQUIRED`: there are no findings, which doesn't mean the layout passed. Subjects over text, alignment and narrative still need visual review, and the contrast check samples only the rectangle behind each text box.
- Text size is estimated from the font, not actually rendered. The output's `fonts_substituted` lists fonts whose files weren't found and were estimated with a substitute; results for that text are less accurate.

Don't break the layout just to quiet the script, for example by shrinking text until it is hard to read.

## Fix and deliver

Name the defect's slide, shape and cause, make the smallest fix and re-render. When a full-slide scene triggers a "large raster image" warning, you can record it as intentional once you have confirmed that it is purely a scene illustration and that text and diagrams remain separate objects; this doesn't excuse text overflow or data problems.

Keep the final deck, the chosen assets, the necessary previews and the provenance; don't add unrequested PDFs, videos, voice-overs or piles of template documents. Delivery notes distinguish actual visual verification, structural verification and tests that haven't been run.

## Sanity cases for the skill itself

When writing or updating this skill, check its decisions against these different requests. You don't need to run paid generation or change existing decks to do this.

| Request | Expected behaviour |
| --- | --- |
| Make a new product introduction deck with scene backgrounds, icons and editable text | Plan the narrative and layout for the audience, generate separate backgrounds and transparent icons, and compose them with native text and diagrams |
| Slides 1 and 2 are great, redo the rest; the user has also moved things | Read the latest source first, keep the approved slides and change only the named scope |
| Don't fix the white icon boxes now, just write the rule into the skill | Write the transparency and review requirements without modifying images or the PPT |
| A different project: a three-minute talk in Chinese, five slides | Adapt to the new request without reusing an earlier deck's slide count, language or data |
| A lecture or status report that is mostly code, timelines and risks | Code stays native; risks become rows rather than a table; milestones, risks, concepts and other parallel points each get a matching icon, with any exceptions explained |
| Codex's built-in presentations skill is also loaded and its check flags "repeated decorative icons" | Keep meaningful parallel icons as this skill requires instead of deleting them to pass the other check |
| Abstract topics such as programming lessons or research methods | Backgrounds show the topic with desks, whiteboards, equipment or places instead of forcing people in, and the composition varies across slides |
| The same people appear on all three slides | Use the first background as the reference image, reuse the fixed character descriptions, and compare them side by side during review |
| An English deck with no template, audience not specified | Aptos Display and Aptos; Arial or Calibri only when the user says viewers lack Microsoft 365; not Segoe UI |
| A footer or label lands on wood grain, foliage or a skyline | Move it to a calm area or give that block its own panel, without covering the rest of the scene |
| Titles and lists already sit on a calm wall or sky | Leave them bare; don't add a box behind every block for consistency |
| Only the last two items of a five-day list overlap busy artwork | A matching band behind all five days, one panel behind the whole list, or move the list; never bands behind only Thursday and Friday |
| Three model options run across a city view, each a separate row | One band per option with shared left and right edges, white or a pale tint of each option's colour at about 80% |
| A three-step flow joined by arrows crosses a busy window | One lane panel behind the whole flow, not a box around each step's label |
| Three risks, each with a mitigation and an owner | Three rows: icon, the risk in its colour, the mitigation beneath and the owner as a small label; no header row and no dark header bar |
| Four plans compared by price, storage and support | A native table in the No Style, No Grid style: a small coloured header over one rule, thin row rules, no vertical lines |
| Fix the website login or a CSV import, with no presentation involved | Don't apply this presentation skill or trigger image generation or deck edits |
