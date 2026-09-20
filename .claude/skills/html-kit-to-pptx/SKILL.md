---
name: html-kit-to-pptx
description: Build a .pptx deck whose slides match an existing HTML slide kit / reference deck / design-token file, with diagrams and charts embedded as vector SVG. Use this skill whenever the user has a reference HTML slide collection, a design system markdown (DESIGN-*.md), a style guide or an existing deck they want new slides to look like, and wants PowerPoint out — including when they just say "make a pptx from this report/PDF/doc in our slide style", "turn these slides into PowerPoint", "이 레퍼런스대로 pptx 만들어줘", or ask for deck graphics as SVG rather than images. Also use it when a PPTX must be generated programmatically with exact pixel-level control over layout, fonts and CJK text.
---

# HTML slide kit → PPTX

A reference HTML deck already settles the questions that make slides look
designed: canvas size, margins, type scale, one accent color, how a section
break is signalled, where the page number sits. The job here is transcription,
not design. Keep working in the kit's pixel grid, convert to EMU at the very
end, and the PowerPoint comes out looking like the kit rather than like
PowerPoint.

The bundled `scripts/deckkit.py` does the pixel→EMU work and, importantly,
renders the same slide model twice: once as the real .pptx and once as preview
PNGs you can actually look at. That second renderer is what makes this
reliable — PowerPoint is not installed in most sandboxes, so without it you are
shipping a file you have never seen.

## Setup

```bash
pip install python-pptx cairosvg
python scripts/example_deck.py /tmp/example.pptx    # smoke test, ~4s
```

If the preview PNGs show boxes instead of CJK text, cairosvg cannot find a
CJK font — see `references/environment.md`. This affects only the PNG fallback
inside the .pptx and your preview, never the text on the slides.

## Workflow

### 1. Read the kit, write down the theme

Open the reference HTML (and any DESIGN-*.md beside it) and extract the numbers
into a `Theme`: canvas, padding, runner height, fonts, colors. Note the type
scale and the slide archetypes the kit offers — title, section divider, bullets,
split, card grid, table, quote, full-bleed. `references/reading-the-kit.md` has
a checklist and shows what to grep for.

Tell the user the theme you extracted in two or three lines before building.
A wrong accent color or padding is cheap to fix now and expensive to fix across
twenty slides.

### 2. Outline the deck against the kit's archetypes

Map the source content onto layouts *before* writing code. Write the outline as
a numbered list — slide number, archetype, headline, what the graphic is — and
keep it visible while you build. Two habits that carry most of the quality:

- **Vary the archetype.** Consecutive bullet slides are the signature of a deck
  nobody wants to read. Alternate light and dark surfaces the way the kit does;
  a section divider every 4–6 slides gives the reader a place to breathe.
- **Give every slide one job.** The headline should state the finding
  ("기여도는 20~70년에 걸쳐 뒤늦게 올라왔다"), not the topic ("기여도 추이").
  If you cannot write that sentence, the slide is carrying two ideas — split it.

### 3. Draw the graphics as SVG

Write each chart or diagram to its own `.svg` file in an assets directory next
to the deck. `scripts/svgkit.py` has the common forms (`bars_h`,
`bars_grouped`, `lines`, `range_dots`, `small_multiples`, `flow_steps`,
`cards`) plus primitives for diagrams that are not charts.

Size each graphic to the hole you left for it in the layout — pass the target
width and height — rather than drawing it at some default size and scaling.
Scaling changes the apparent font size and breaks the deck's type scale.

`references/graphics.md` covers form selection, the palette rule, and the label
rules that keep a chart readable at the back of a room.

### 4. Build the slides

```python
from deckkit import Slide, Theme, render_pptx, write_previews

s = Slide(THEME, bg="#ffffff", runner="01 · 섹션", page="04")
s.eyebrow("Evidence")
ry = s.head(["업무 수준에서는", "효과가 이미 나타났다"])   # returns y below the rule
s.bullets(THEME.pad_x, ry + 34, 500, [["첫 줄", "둘째 줄"], ["다음 항목"]])
s.svg("bars.svg", 632, 210, 560, 300)
```

**Break every line of text yourself.** `deckkit` turns off PowerPoint's word
wrap, so a text block is exactly the lines you passed. This is the single
highest-leverage habit in the whole workflow: browser and PowerPoint line
breaking differ, so auto-wrapped text is where decks sprout orphan words and
overflowing boxes — and it is why the preview can be trusted to match the real
file. Aim for ~40 CJK characters per line at 20 px in a 900 px column, ~26 in a
520 px column.

`references/layouts.md` has worked geometry for each archetype (split columns,
card grids, tables, dividers) with the numbers already solved.

### 5. Look at every slide, then fix what you see

```python
render_pptx(slides, "deck.pptx", asset_dir=assets)
write_previews(slides, "preview", asset_dir=assets)
```

Then actually open the preview PNGs — all of them, not a sample. Reading the
code you just wrote tells you what you intended; the image tells you what
happened. What turns up in practice, roughly in order of frequency:

- text overflowing a card or running past the right margin
- a chart's axis label colliding with its title or first tick
- a card whose content stops 100 px above its bottom edge (height guessed, not computed)
- a graphic 150 px narrower than the content column, so the slide looks off-center
- the same source or number stated twice, once in the SVG and once in the slide text

Fix, re-render, look again. Two or three rounds is normal.

### 6. Check the file

```bash
python scripts/check_deck.py deck.pptx --expect-svg 10
```

This catches what a preview cannot: shapes off the canvas, SVG parts that are
present but unreferenced (PowerPoint would quietly show the PNG fallback),
missing text. Read the text dump once end to end — it is the last chance to
catch a typo or a slide that lost its body copy.

### 7. Hand over

Report what you built, where the SVG sources live, and how to regenerate. Keep
the generator script with the deck: the next request is almost always "change
slide 12", and a script makes that a one-line edit instead of a rebuild.

Say plainly that the .pptx itself was not rendered if LibreOffice was not
available, and that QA was done on the geometry-identical preview. Suggest the
user open it once in PowerPoint.

## Things that will bite you

- **Arial (and most Latin fonts) have no CJK glyphs.** `Theme.ea_font` sets the
  `<a:ea>` typeface so Korean/Japanese/Chinese runs render in a face you chose
  instead of whatever PowerPoint picks. Set it whenever the deck is not purely
  Latin.
- **SVG needs a raster fallback.** OOXML has no bare SVG picture: the shape
  carries a PNG blip plus an `svgBlip` extension pointing at the SVG part.
  `deckkit` does both; `check_deck.py` verifies they stay paired.
- **Rounded-rectangle "radius" is a fraction, not pixels.** python-pptx takes
  `adjustments[0]` as a share of the shorter side; `deckkit.rect(radius=18)`
  converts for you.
- **Shapes arrive with a preset shadow.** Every shape sets `shadow.inherit =
  False`; if you add shapes outside `deckkit`, do the same or they will bloom
  drop shadows the kit never had.
- **Text boxes have built-in padding.** All four margins are zeroed so text
  aligns with shapes at the same x. Keep that if you extend the renderer.
- **Native PowerPoint charts are a different tool.** If the user wants a chart
  they can edit in PowerPoint or relink to data, use `python-pptx`'s
  `add_chart` instead of an SVG. SVG is the right default when the chart is
  final artwork and must match the kit exactly.

## Files

| Path | What it is |
|---|---|
| `scripts/deckkit.py` | Theme, Slide model, PPTX renderer, preview renderer, SVG embedding |
| `scripts/svgkit.py` | SVG primitives and chart/diagram builders |
| `scripts/check_deck.py` | Structural validation + text dump |
| `scripts/example_deck.py` | Four-slide worked example; also the environment smoke test |
| `references/reading-the-kit.md` | How to pull a Theme and archetypes out of a reference HTML kit |
| `references/layouts.md` | Worked geometry for each slide archetype |
| `references/graphics.md` | Choosing a chart form, palette and labelling rules |
| `references/environment.md` | Dependencies, fonts, WSL/sandbox notes, rendering options |
