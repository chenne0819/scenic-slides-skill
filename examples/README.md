# Examples

Five editable PowerPoint decks made by `scenic-slides`. Each one started from a different kind of input, kept as `brief.md` beside the result.

| # | Deck | Type | Input given to the skill |
|---|------|------|--------------------------|
| 1 | [Write anywhere, sync later](01-offline-sync-talk/) | Developer meetup talk | Full outline with bullets, including a code slide |
| 2 | [Why does the sea go in and out?](02-tides-lesson/) | Science lesson for ages 10–12 | Full outline, including two diagrams to draw |
| 3 | [Kyoto, at our own pace](03-kyoto-family-trip/) | Family trip plan | One paragraph; the skill chose the structure |
| 4 | [Phishing can look like everyday work](04-phishing-onboarding/) | New-hire security training | Messy notes pasted as-is |
| 5 | [Cooling the street](05-street-trees-proposal/) | Honours research proposal | One prose abstract |

## What's in each folder

```
brief.md          the input, unchanged
overview.webp     the cover and the other four slides on one image
previews/         every slide, exported from PowerPoint (WebP here; full-size PNGs are in the zip)
provenance.json   full generation prompt, reference images and alpha check for every scene and icon
README.md         slide summary, palette, fonts, checks done and known limits
```

**Download:** the `.pptx` files, full-resolution previews and the separate background and icon images are in [scenic-slides-examples.zip](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip) on the Releases page.

## How they were made

Made on 2026-11-04. Each deck was made by its own `codex exec` session (Codex CLI 0.166.0-alpha.5.1, reasoning effort `high`), three at a time, using the built-in `image_gen` tool. Every session got the same instructions apart from its deck folder and brief.

| Deck | Time | Images generated (kept) |
|------|------|-------------------------|
| 1 Tech talk | 16 min | 15 (5 scenes + 10 icons) |
| 2 Tides lesson | 17 min | 12 (5 + 7) |
| 3 Kyoto trip | 20 min | 16 (5 + 9) |
| 4 Phishing training | 16 min | 13 (5 + 8) |
| 5 Research proposal | 16 min | 11 (5 + 6) |

The organisations and products in decks 1, 4 and 5 are fictional, and none of the decks contains invented statistics. Deck 3 names real Kyoto places but gives no prices, opening hours or crowd figures. The generated artwork is illustrative and doesn't depict any venue exactly.

## Independent verification

These checks were run after the Codex sessions finished, separately from each session's own review:

- **Layout:** `check_layout.py` reports 0 issues, 0 checks and no substituted fonts on all five decks.
- **Icons:** `check_icon_alpha.py` returns `ALPHA_PRESENT_VISUAL_REVIEW_REQUIRED` for all 40 icons. Every icon's outer border is at least 95.7% transparent.
- **Structure:** every deck has exactly 5 slides at 16:9, with speaker notes on every slide. Each slide has one full-slide background picture. Every other picture is byte-for-byte one of the deck's icon files.
- **Rendering:** PowerPoint 16 re-rendered all 25 slides at 1920×1080, and each matched its preview pixel for pixel.
- **Visual review:** all 25 previews were looked at.

**Not tested:** Keynote, Google Slides or LibreOffice, and projection on a real screen. Fonts are not embedded.

## Known issues

These are small things a careful reviewer would notice. They were left as generated:

- **Deck 1, slide 3:** the reading panel's lower edge cuts across the instruments on the workbench.
- **Deck 1, slide 5:** the footer says "status supplied in the brief", which speaks to whoever wrote the brief rather than to the audience.
- **Deck 2, slide 1:** the cover shows a page number.
- **Deck 3, slide 5:** the three travel rules are parallel, but arrows link them as if they were steps.
- **Deck 4, slides 1–3:** all three use nearly the same office-and-harbour scene.
- **Deck 5, slide 3:** the method panel covers the top of the field-equipment bag.
