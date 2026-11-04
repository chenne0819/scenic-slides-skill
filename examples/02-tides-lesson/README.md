# Why does the sea go in and out?

A five-slide, 16:9 science lesson for Year 6 learners aged 10–12, designed for about 15 minutes with discussion. [Open the PowerPoint](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip) · [Original brief](brief.md)

The supplied slide order and teaching points are preserved. Short explanations, native teaching diagrams and icon-led comparisons replace dense bullets; every slide has a generated coastal scene and 3–4 sentences of speaker script.

1. **Why does the sea go in and out?** — A beach scene introduces the shoreline mystery.
2. **What is a tide?** — High and low tide, the usual daily pattern and approximate time between highs.
3. **The Moon pulls the ocean** — Editable Earth, two water bulges, Moon, beach marker and spin arrow.
4. **Spring tides and neap tides** — Side-by-side alignment diagrams explain larger and smaller tidal ranges.
5. **Be a tide detective** — Three practical beach rules and a timing quiz; the answer is in the notes.

## Visual system

Sea-glass teal `#298F91`, pale aqua `#E7F4F3`, warm sand `#F5E8CF`, navy `#183F4A`, coral and lavender accents. Aptos Display headings (36–40 pt), Aptos body (22–28 pt), diagram labels (18–22 pt) and secondary notes (14 pt). Both font families were found in the Office cloud-font cache and set in the theme. Later backgrounds reference the first scene; later icons reference the first icon. Full prompts and original generated-image paths are in [provenance.json](provenance.json).

## Checks performed

- **Visual:** Every slide exported by PowerPoint at 1920×1080 and inspected before continuing; corrected shoreline contrast, label placement, default shape shadows and panel padding. All seven icons inspected on white, navy and the actual seaside background, including a temporary PowerPoint review sheet: no backing boxes, checkerboards, white fringes or erased interior fills observed. Final slide sequence reviewed for consistency and narrative.
- **Structural:** Exactly five slides, 16:9, 54 editable text boxes, native diagrams/lines/panels and speaker notes on every slide. `check_layout.py`: **0 issues, 0 checks, no substituted fonts**. `check_icon_alpha.py`: all seven report **ALPHA_PRESENT_VISUAL_REVIEW_REQUIRED**, with alpha range 0–255; the separate visual inspection above completes that review. All chosen assets are used. PowerPoint COM operations held the shared named mutex and closed only presentations opened for this run.
- **Icon coverage:** High/low tide, spring/neap tide and all three safety points have distinct matching pictograms; the tide clock consistently represents timing. Slide 3 is a labelled scientific diagram, so its physical bodies and tide labels use native shapes rather than extra icons. The cover and single quiz need no parallel-point icons.
- **Not done:** Classroom testing, projector testing, and rendering in Keynote, Google Slides or older Office. No PDF, video or upload was produced.

## Scientific scope and known limitations

No unresolved layout or transparency findings. The tidal-bulge model is deliberately simplified and not to scale; spring-tide Moon positions are alternatives. Timing is approximate, and real visits require local tide predictions. Fonts may substitute on systems without Aptos.

Concepts were cross-checked against NOAA: [tide frequency](https://oceanservice.noaa.gov/facts/tidefrequency.html), [spring and neap tides](https://oceanservice.noaa.gov/facts/springtide.html), and [the lunar-day cycle](https://oceanservice.noaa.gov/education/tutorial_tides/tides05_lunarday.html). The original brief remains unchanged.


---

The `.pptx`, the full-resolution previews and the separate background and icon files are in [scenic-slides-examples.zip](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip) on the Releases page. `provenance.json` here has every generation prompt; its local paths were shortened before publishing.
