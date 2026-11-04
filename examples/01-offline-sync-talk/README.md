# Driftnote — Write anywhere, sync later

A five-slide, 16:9 English technical talk for web and mobile developers, designed for an approximately ten-minute meetup slot. Driftnote is fictional. The supplied [brief](brief.md) is preserved, including its slide order and shipped / testing / planned distinctions.

[Download the editable PowerPoint](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip)

The outline becomes a railway journey: an opening landscape, a disconnected train ride, a device workbench, a concrete merge example and an arrival-station close. Scene artwork and individual icons are generated; typography, panels, connected diagrams and Python code are native editable PowerPoint objects. Each slide has a three- or four-sentence speaker script.

1. **Write anywhere, sync later** — introduces the fictional app and offline-edit promise.
2. **Offline is normal** — phone and laptop edits expose the cost of whole-note last-write-wins.
3. **Save now. Sync when ready.** — four connected steps separate local writing from later synchronization.
4. **Two edits. One repeatable result.** — independent append operations converge through a seven-line deterministic replay example.
5. **Status and next steps** — distinguishes shipped, testing and planned work; closes with questions and a fictional beta invitation.

**Visual system.** Warm ivory `#F5F0E5`, ink `#233747`, teal `#286F70`, blue `#3B618D` and rust `#A34B2F` (artwork accent `#B65735`). Aptos Display headings, Aptos body and Consolas code; 34–40 pt titles, 18–24 pt body, 16 pt code and 12–14 pt supporting labels. Later scenes reference the first background; later icons reference the first phone icon. Full prompts, source paths, reference images and check results are recorded in [provenance.json](provenance.json).

**Visual verification performed.** All slides were exported from Microsoft PowerPoint at 1920×1080 and inspected individually and together. All ten icons were reviewed on white, dark and an actual illustrated background in a temporary PowerPoint review slide, then in the final deck. No visible white boxes, checkerboards, fringes or damaged interior fills were found. A shared translucent lane protects the four-step flow; the closing footer was moved off the station trim. The temporary review deck is not included.

**Structural verification performed.** Exactly five slides; native text, code, panels and bound connectors; full-slide scene on each slide; speaker notes on every slide; minimum type size 12 pt. `check_layout.py`: **0 issues, 0 checks, no font substitutions**. `check_icon_alpha.py`: all ten icons reported `ALPHA_PRESENT_VISUAL_REVIEW_REQUIRED`, followed by the visual checks above. The Python snippet was executed with both arrival orders of the illustrative operations and produced the displayed merged note. PowerPoint COM used the shared mutex throughout, closed only this run's presentations and never quit PowerPoint.

**Not performed.** Production sync or performance tests, a timed talk rehearsal, and compatibility checks in other presentation apps. Aptos availability outside Microsoft 365 was not tested. No real beta service or URL is supplied.

**Known issues.** No unresolved visual or structural findings. The merge sketch deliberately assumes a common starting state, deduplicated operations, unique sort keys and deterministic application; it is not a complete text-conflict algorithm. Same-paragraph merging remains in testing, as requested by the brief. No benchmark or adoption data is invented.

Previews: [1](previews/01.webp) · [2](previews/02.webp) · [3](previews/03.webp) · [4](previews/04.webp) · [5](previews/05.webp)


---

The `.pptx`, the full-resolution previews and the separate background and icon files are in [scenic-slides-examples.zip](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip) on the Releases page. `provenance.json` here has every generation prompt; its local paths were shortened before publishing.
