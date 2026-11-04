# Kyoto, at our own pace

A five-slide family trip plan for a dinner-table conversation, created with `scenic-slides`. The short [brief](brief.md) became a flexible four-day itinerary, three packing kits and a memorable travel-day pact. The original brief is unchanged.

[Open the PowerPoint](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip) · [Slide previews](previews/) · [Asset prompts and provenance](provenance.json)

1. **Kyoto, at our own pace** — four autumn days with room for everyone.
2. **Ease in. Then chase the leaves.** — arrival snacks at Nishiki Market, then Tenryu-ji and Arashiyama.
3. **Animals first. A gentle finish.** — Kyoto City Zoo, followed by an optional aquarium visit before departure.
4. **Pack light. Stay comfortable.** — clothing, a day bag and adult-held essentials.
5. **Our travel-day pact** — stay together, ride calmly and stop for snacks.

## Design

Warm ivory `#F6EEDC`, maple rust `#9B4A35`, moss `#4E6652`, ochre `#946824`, dusty blue `#466E78` and ink `#303D36`. Aptos Display headings, Aptos body; titles 36–40 pt, body 20–23 pt, labels 13–16 pt. Both fonts were available in the Office cloud-font cache.

Five full-bleed scenes and nine individual pictograms were generated with built-in `image_gen`. Later scenes reference the first scene; later icons reference the first icon. Text, reading panels and connected arrows remain editable. Composition varies between a landscape cover, day-plan bands, open-wall rows, a packing scene and a native travel sequence. Generated artwork is illustrative, not a precise depiction of each venue.

## Checks actually performed

- **Visual verification:** every slide exported by PowerPoint at 1920 × 1080 and inspected; final deck and background contact sheets reviewed. Corrected band padding, a title crossing the station roof and default shape shadows. All nine icons inspected on white, dark and scene backgrounds, then in the final slides. A hazy first giraffe was rejected and regenerated; only the chosen clean version is included.
- **Structural verification:** `check_layout.py` reports **0 issues, 0 checks, no substituted fonts**. `check_icon_alpha.py` reports `ALPHA_PRESENT_VISUAL_REVIEW_REQUIRED` for all nine icons; visual inspection was also completed. Five 16:9 slides, speaker scripts on every slide, native text throughout, and all ten parallel points have matching icons. Shared PowerPoint mutex used for every COM operation; only presentations opened for this task were closed.
- **Not done:** bookings, live transport routing, exact-date weather/foliage checks, physical projection, or compatibility testing outside PowerPoint. No PDF or video produced; nothing uploaded.

## Planning limits and sources

Exact dates, lodging and arrival/departure details were not supplied. The day order is provisional; the aquarium is optional, and a late arrival moves the market visit. Garden quietness and peak leaf colour cannot be guaranteed. No prices, opening-hour claims or crowd statistics appear on the slides. No unresolved rendering defects were found; viewers without Aptos may substitute fonts.


Place and etiquette references checked on 4 November 2026: [Tenryu-ji garden](https://kyoto.travel/en/destinations/tenryuji-temple/), [Nishiki Market visitor requests](https://www.kyoto-nishiki.or.jp/en/manner/), [Kyoto City Zoo visitor information](https://zoo.city.kyoto.lg.jp/zoo/lang/en/visitor/) and [Kyoto Aquarium](https://kyoto.travel/en/destinations/kyoto-aquarium/). Relevant links also appear in speaker notes.


---

The `.pptx`, the full-resolution previews and the separate background and icon files are in [scenic-slides-examples.zip](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip) on the Releases page. `provenance.json` here has every generation prompt; its local paths were shortened before publishing.
