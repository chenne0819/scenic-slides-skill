# Harbourline Phishing Basics

A five-slide, 16:9 new-hire security onboarding deck for **Harbourline Logistics, a fictional company**. The [raw brief](brief.md) becomes a friendly 15-minute teaching sequence: recognise, inspect, report, handle MFA prompts, then practise. Four English speaker-note sentences per slide provide facilitation cues and the exercise answers.

[Download the PowerPoint](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip) · [PNG previews](previews/) · [Asset provenance and checks](provenance.json)

1. **Everyday disguise:** an ordinary-looking email or chat is a reason to pause before acting.
2. **Five warning signs:** urgency, look-alike senders, mismatched links, requests for secrets and unexpected attachments.
3. **A supportive response:** use Report; if already clicked, call IT on extension 4400 immediately, with no blame.
4. **Unexpected MFA prompts:** deny and report; IT never asks for a password or MFA code.
5. **Spot the fake:** inspect a fictional, fully editable email and discuss the next action.

The visual direction is a warm harbour dispatch office, with contextual scenes on every slide and a consistent recurring character. Palette: ivory `#F5F0E6`, navy `#183743`, teal `#226F70`, coral `#AE4E3D`, ochre `#9A641E`. Typography: **Aptos Display** headings and **Aptos** body, confirmed in the local Office font cache; titles 36–40 pt, body and supporting headings 18–24 pt, metadata 12–17 pt. Text, rules, panels, the flow arrow and phone interface remain native PowerPoint objects. Only the five scene backgrounds and eight standalone icons are raster images.

**Visual verification:** reviewed every slide exported by PowerPoint 16 at 1920×1080, re-rendered corrections, and reviewed all scenes and slides together against the skill's quality checklist. Reviewed all icons on white, dark navy and actual artwork in a temporary PowerPoint review deck, plus their final placements. No white boxes, checkerboards, fringes or erased interior fills were observed. The temporary review deck is not included.

**Structural verification:** exactly five slides, 16:9, native editable text and shapes, notes on every slide, and five 1920×1080 previews. Final `check_layout.py`: **0 issues, 0 checks, no font substitutions**. `check_icon_alpha.py` returned `ALPHA_PRESENT_VISUAL_REVIEW_REQUIRED` for all eight icons; all then received the visual review described above. Every parallel teaching point has a matching icon. PowerPoint COM work used the shared named mutex and closed only this run's presentations.

**Not done:** testing in other presentation applications, a live delivery rehearsal, or production mail-app integration. Session timing is a facilitation plan, not a measured result. Company procedures, extension 4400 and all exercise addresses belong to the fictional brief; the example contains no live hyperlinks.

**Known issues:** no unresolved layout or transparency defects found. Fonts are not embedded, so viewers without Aptos may see substitutions. No claims of training effectiveness or invented statistics are included.



---

The `.pptx`, the full-resolution previews and the separate background and icon files are in [scenic-slides-examples.zip](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip) on the Releases page. `provenance.json` here has every generation prompt; its local paths were shortened before publishing.
