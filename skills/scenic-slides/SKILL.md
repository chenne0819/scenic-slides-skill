---
name: scenic-slides
description: "Create or refine polished, editable PPT/PPTX presentations with full-slide contextual backgrounds, transparent 2D icons and clear visual storytelling. Use when asked to make a slide deck, polish or redesign a presentation, add scene backgrounds, or pair icons with text (also 製作簡報、簡報美化、情境底圖). Not for application UI work or data-analysis requests without a presentation deliverable."
---

# Scenic Slides

Build professional presentations with a clear narrative, full-slide contextual backgrounds, and editable text and diagrams. A template, brand or editing scope the user specifies for the current task takes precedence over these defaults. When this skill is used alongside another presentation skill (for example Codex's built-in `presentations`), its icon rules override the other skill's defaults and layout checks that discourage decorative icons.

## Confirm the source and scope first

- Read the user's latest message, reference images and the named deck first. If a deck is open and the user has just adjusted it, inspect the current version with read-only tools; don't rebuild it from earlier previews.
- Settle the audience, language, purpose, duration, output format, and which slides are already approved. Use details you can infer from context instead of asking again.
- Keep approved slides and anything the user said not to touch. Before editing, record their text and shape positions, and keep a source copy when needed; never overwrite the user's newer adjustments with an older version.
- This skill covers only the presentation and the assets it needs. It does not change application code, upload data or edit dashboards.

## Get the story straight first

For each slide, write down one main message, the evidence that supports it, and the visual that fits. A new-project introduction usually starts with a concrete pain point and its impact, then shows how the features respond, how it works, credible evidence and next steps. Keep a good structure the user already has; don't fix the slide count or sections.

- Use real, understandable situations, such as a meeting that has started while the answer is still waiting on another department, rather than abstract phrases like "improve efficiency".
- Pair each pain point with one grounded feature and say what remains unsolved. Keep what is implemented, what is tested and what is planned separate.
- When comparing other tools, describe the presented project's concrete differences; don't claim competitors are all insecure or can't call tools. Cite numbers from sources or actual runs; never let an illustration produce fake data.
- Keep on-slide text short and readable, and put background explanation in the speaker notes. Follow the requested language, timing and length; don't carry over the language, length or slide count of an earlier or reference deck.

## Required visual elements

1. **The contextual background is a full-slide scene.** Extend the environment to every slide edge, put the main subject in its planned area, and place text in natural open space. A small corner illustration, plain colour blocks or a row of icons does not count as a background. Keep suitable backgrounds the user has already approved.
   - Choose the background's main subject from the topic and the slide's message: people and interaction, close-ups of objects or materials, empty places, a top-down desk, equipment, city or natural landscapes. Include people only when the message is about people, roles or behaviour; a deck doesn't need people on every slide. Vary the composition with the slide's purpose (left or right, top or bottom, close-up or wide shot) instead of repeating "a person on one side, an empty wall on the other" on every slide.
   - Keep the deck visually continuous. Once the first background is approved, use it as the reference image for later backgrounds, and use the first approved icon as the reference for later icons. When the generation tool accepts reference images, pass them in rather than only describing them in the prompt. When people appear, write a fixed description of each person (age, hair, clothing, colours), reuse the same characters across slides, and record the references in the asset provenance.
2. **Design icons, text and relationships together.** Use simple flat 2D icons with short labels and the arrows needed for viewers to follow features and order. Icons alone are not enough, and walls of text don't replace visuals. Avoid 3D, glossy plastic, heavy shadows and embossing.
   - When a slide has 2–5 parallel points (pain points, steps, milestones, risks, options, event days, etc.), give each point an icon that matches its meaning. One icon stands for one concept; don't reuse it for different points.
   - Code, data charts and the values in a genuine data grid don't need icons. Risks, options, partners and decisions are parallel points, not table contents: set each as a row with its icon, its name as a heading in its semantic colour and the detail beneath, with no header row. Keep native tables for grids viewers read across and down, and style them lightly instead of keeping PowerPoint's default header bar and grid. The rows-and-tables section of visual-recipes.md has the details.
3. **Icons must have truly transparent backgrounds.** New raster icons need a real alpha-transparent background, with no white box, solid backing tile, fake checkerboard or white fringe. Request transparency at generation time, and check the alpha channel and the look on real dark and light backgrounds before placing them in the deck. Don't erase white areas that belong to the symbol itself. Don't fix old icons the user explicitly asked to keep.
4. **Text and structure stay editable.** Titles, labels, descriptions, arrows, frames, tables and data charts remain native objects. Generated images carry only the scene or a standalone icon; never generate a whole slide with its text and flow baked in to replace the PPT.
5. **Professional, with colour hierarchy.** Use consistent line work, type and semantic colours so that data, tools, guidance and results are easy to tell apart; don't make the whole deck one shade of green. Journal figures can inform structure, but slides need larger type and lower information density.
   - Use the template's or brand's fonts. Without one, English decks use Aptos Display for headings and Aptos for body text (the Microsoft 365 default); switch to Arial or Calibri only when the user says the deck must open without Microsoft 365. Code uses Consolas. Avoid operating-system interface fonts such as Segoe UI. The typography section of visual-recipes.md has the details.
6. **Every text block must be readable on its background.** Fix composition, position and copy length first. Where text still sits on detailed artwork (foliage, wood grain, skylines, people, equipment) or has weak contrast, add a semi-transparent light reading panel; small labels, captions and footers count too. Decide panels per group, not per line: a list, step sequence or set of options gets no panels, a matching band behind every item, or one panel behind the whole group, never panels behind only the items that overlap busy art. Leave titles and groups that already read clearly on calm sky, wall or floor bare, and keep the rest of the scene visible rather than laying one large board over it. Data charts may use a clear local backing panel, and decoration must stay out of axes and curves. The reading-panels section of visual-recipes.md describes the four panel patterns.

Read [visual-recipes.md](references/visual-recipes.md) before generating assets or re-laying-out slides; it has composition and prompt templates.

## Build and review

- Use the native editing tools available for the existing deck. Build the file with python-pptx, or drive PowerPoint directly (COM automation on Windows) when it is installed. When editing an open deck, confirm the active presentation and its shape list first, and stay on one backend instead of overwriting it with another file model. Export previews from PowerPoint or the presentation app the audience will use.
- Use the available image generation tool for scenes and new raster icons, with its transparent-background option as the tool specifies. Inspect user-supplied images before modifying them. Don't substitute Python, SVG drawing code or HTML screenshots for the generated artwork the task asks for. Using native APIs for layout and reading alpha for verification is fine.
- State a limitation only when a genuinely required tool is missing; keep the editable target and use a suitable alternative. Never claim that an image was generated, a background removed or a target-app check done when it wasn't.
- Save the chosen assets in the project and record the generation prompts and sources. Keep the background and each icon as separate files with recognisable names. Don't put unused images or debug files in the deliverable folder.
- After each slide, export a preview from the presentation app and check text, contrast, icon transparency, arrows, charts and background. Then run `python scripts/check_layout.py DECK.pptx` for a read-only layout check (text overflow and overlap, text near the edge, table cell padding, icons over text, content crowding the footer, low contrast or busy artwork behind text, lists where only some items have a reading panel, short lists set as tables, and tables left in the default style). Fix every finding or write the reason for keeping it in the delivery notes. Fix defects before moving on, and finally review the whole deck's style and narrative.
- Review against [quality-checks.md](references/quality-checks.md), including icon coverage: when parallel points have no icon, give the reason in the delivery notes. New PNG/WebP icons can get a read-only alpha check with `python scripts/check_icon_alpha.py PATH...` (paths relative to this skill folder); this check doesn't replace visual review.
- Deliver a PPTX that actually opens, plus the necessary previews; produce notes, PDF or video only when requested. Summarise the changes and check results, and don't claim tests that weren't run.

## Packaging

Packaging follows [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills) and the [Agent Skills specification](https://agentskills.io/specification): the folder goes in `.agents/skills/`, the entry point is `SKILL.md` with `name` and `description`, details live in `references/` and load on demand, file paths are relative to the skill folder and referenced one level deep, and interface metadata is in `agents/openai.yaml`. The visual requirements above come from user feedback on real decks, not from OpenAI's official presentation guidance.
