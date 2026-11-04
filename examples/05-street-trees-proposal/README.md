# Cooling the street

[Open the PowerPoint deck](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip) · [Original brief](brief.md)

A five-slide, 16:9 honours research proposal for a supervisor panel. The prose abstract becomes a question → need → method → plan → contribution narrative for an intended eight-minute presentation. Sampling and dates remain explicitly planned; no results or invented effect sizes are shown. Every slide includes a short English speaker script.

1. **Question:** Do street trees make footpaths more comfortable on hot afternoons?
2. **Why it matters:** Connect heat-storing paving to the need for evidence at footpath scale.
3. **Method:** Pair canopy and exposed segments, measure consistently, and compare within streets.
4. **Plan:** Select sites in November, measure December–February, analyse and write March–May.
5. **Contribution and limits:** Offer a repeatable protocol while keeping findings indicative and local.

The closing slide distinguishes physical heat measurements from directly surveyed comfort. Speaker notes also flag the need to agree the statistical unit of analysis before fieldwork.

**Design.** Warm ivory `#F7F2E7`, forest `#264A41`, eucalyptus `#547867`, terracotta `#AD543F` and slate `#426479`; darker related tones support text contrast. Aptos Display headings (36–40 pt), Aptos body (18–24 pt), and labels (12–14 pt). Five generated editorial scenes vary from street vistas to field equipment and a notebook. Six generated pictograms have genuine alpha transparency. All text, arrows, timeline lines and reading panels are native editable PowerPoint objects. Only scenes and individual icons are raster images.

**Visual verification performed.** Every slide was exported from Microsoft PowerPoint at 1920 × 1080, inspected, corrected where needed and re-exported. The complete deck and backgrounds were reviewed together for narrative, composition and consistency. All six icons were inspected in a temporary PowerPoint review slide on white, dark and scene backgrounds, then in their actual placements; no visible backing boxes, checkerboards or fringes were found. Parallel point groups all have matching icons; the cover contains one question and needs no parallel icon group.

**Structural verification performed.** Exactly five widescreen slides; one full-slide scene per slide; editable foreground text and structure; notes on every slide; minimum type size 12 pt; five correctly sized previews. `check_icon_alpha.py` returned `ALPHA_PRESENT_VISUAL_REVIEW_REQUIRED` for all six icons, followed by the visual review above. Final `check_layout.py`: **0 issues, 0 checks, no font substitutions**. PowerPoint COM access used the shared mutex; only presentations opened by this run were closed.

**Not done.** Fieldwork, data analysis, external literature verification, timed rehearsal, or rendering tests in other applications. Fonts are not embedded; viewers without Aptos may see substitution.

**Known issues.** No unresolved visual or structural defects identified in the reviewed PowerPoint exports. The illustrations are contextual artwork, not evidence or exact instrument specifications.

Chosen assets, full prompts, source paths, reference-image lineage and checks are recorded in [provenance.json](provenance.json). Previews are in [previews/](previews/). The supplied `brief.md` is retained unchanged.


---

The `.pptx`, the full-resolution previews and the separate background and icon files are in [scenic-slides-examples.zip](https://github.com/chenne0819/scenic-slides-skill/releases/latest/download/scenic-slides-examples.zip) on the Releases page. `provenance.json` here has every generation prompt; its local paths were shortened before publishing.
