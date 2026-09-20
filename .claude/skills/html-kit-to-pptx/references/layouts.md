# Layout recipes

Worked geometry for a 1280 × 720 canvas with 88 px side padding, 64 px top
padding and a 56 px runner — the content column is 1104 px wide and the usable
band runs from y=64 to y=664. Scale proportionally for other canvases.

All coordinates are kit pixels. `ry` below is whatever `Slide.head()` returned:
the y just under the accent rule.

## Title

```python
s.eyebrow("Eyebrow text")                                  # y = pad_y
s.text(pad_x, 200, 1000, ["첫 줄", "둘째 줄"], 60, 600, INK, lh=74, spacing=-1.4)
s.text(pad_x, 360, 900, ["부제 한 줄"], 26, 400, MUTED, lh=34)
s.rect(pad_x, 552, 120, 3, ACCENT)                         # meta anchored low
s.text(pad_x, 594, 700, ["작성자 / 소속"], 15, 600, INK, lh=22)
```

Left-align rather than center: a centered cover wobbles as soon as the title
runs to two lines, and the meta block has nowhere stable to sit. No runner on
the cover.

## Section divider

```python
s = Slide(THEME, TILE, runner="01 · 섹션", page="04", dark=True)
s.text(pad_x, 176, 300, ["01"], 140, 600, "#3a3a3d", lh=140, spacing=-6)
s.eyebrow("Section", y=196)
s.text(pad_x + 250, 226, 800, ["섹션 제목"], 52, 600, "#ffffff", lh=60, spacing=-1.2)
s.text(pad_x, 400, 860, ["한 줄 요약."], 26, 400, "#cccccc", lh=38)
```

The ghost numeral (same color family as the surface, a few steps lighter) gives
the slide weight without adding an element the reader has to process.

## Bullets

```python
ry = s.head(["헤드라인은 주장을", "한 문장으로"], y=94, lh=52)
s.bullets(pad_x, ry + 34, 900, [
    ["항목 한 줄", "이어지는 둘째 줄"],
    ["다음 항목"],
], size=20, lh=30, gap=26)
```

Five bullets is the ceiling; two lines each. Cap the text column at ~900 px even
though 1104 is available — a full-width line at 20 px is too long to scan
comfortably.

## Split (claim + evidence)

Two workable divisions, both with a 48 px gutter:

| Left (text) | Right (graphic) |
|---|---|
| x=88, w=536 | x=672, w=520 |
| x=88, w=496 | x=632, w=560 |

```python
ry = s.head(["헤드라인", "두 줄"], y=94, lh=52)
s.bullets(pad_x, ry + 34, 536, [...], size=19, lh=28, gap=24)
s.svg("chart.svg", 672, 148, 520, 400)
```

Keep the graphic's vertical center near the text block's — a figure that starts
at the headline and a text block that starts 100 px lower reads as two unrelated
halves. Keep the text/figure order the same across the deck.

## Card grid

```python
cw = (1104 - 2 * 24) / 3            # three columns, 24 px gutters → 352 px
for i, (title, lines) in enumerate(items):
    x = pad_x + i * (cw + 24)
    s.rect(x, top, cw, 190, WHITE, 18, HAIRLINE, 1)
    s.text(x + 28, top + 32, cw - 56, [title], 21, 600, INK, lh=28)
    s.text(x + 28, top + 74, cw - 56, lines, 15, 400, MUTED, lh=23)
```

**Compute the card height from its content**, don't guess: `padding + title +
gap + lines × line-height + padding`. Guessed heights are the most common defect
in generated decks — either the text spills past the border or the card ends
100 px below its last line and the grid looks hollow.

If cards come out short and the slide bottom looks empty, add a closing line of
information per card (a verdict, a number, a source) rather than inflating the
box. Two columns: `cw = (1104 - 28) / 2 = 538`.

## Table

Horizontal hairlines only — no vertical rules, no zebra striping, no cell
borders. Header in 15 px uppercase muted with a 1 px ink rule under it; rows
separated by 1 px hairlines; numeric columns right-aligned.

```python
y = ry + 40
s.text(pad_x, y, 300, ["항목"], 15, 600, MUTED)             # header cells
s.rect(pad_x, y + 26, 1104, 1, INK)
for row in rows:
    s.text(pad_x, y + 46, 300, [row[0]], 18, 400, INK, lh=26)
    s.text(pad_x + 700, y + 46, 200, [row[1]], 18, 400, INK, lh=26, align="r")
    s.rect(pad_x, y + 82, 1104, 1, HAIRLINE)
    y += 56
```

Seven rows is the practical ceiling at 56 px per row. More than that belongs in
an appendix or a chart.

## Quote / one sentence

Dark surface, 40–44 px at weight 400 (not bold — size carries it), max three
lines, attribution in 15 px after a short accent rule. Nothing else on the
slide. Use it where the talk should pause.

## Full-bleed figure

Graphic at (0, 0, 1280, 664) with the caption overlaid in the lower band. If
the figure is photographic, put the text over its darkest region or lay a
single-color scrim behind the text — never a decorative gradient across the
whole image.

## Vertical rhythm cheat-sheet

| From | To | Gap |
|---|---|---|
| eyebrow baseline | headline top | 30 px |
| headline bottom | accent rule | 22 px |
| accent rule | body/lead | 26–34 px |
| body block | figure or card grid | 40 px |
| last element | runner line | ≥ 40 px |

When a slide feels cramped, cut a sentence before shrinking the type — the kit's
scale is the one thing that must not drift.
