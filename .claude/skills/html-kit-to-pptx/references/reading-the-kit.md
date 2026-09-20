# Reading the reference kit

The goal of this step is a filled-in `Theme` plus a list of slide archetypes you
can name. Fifteen minutes here saves an hour of nudging boxes later.

## 1. Canvas and margins

Grep the kit's CSS for the slide frame. Most kits declare it directly:

```css
.slide { width: 1280px; height: 720px; }
.stage { padding: 64px 88px; }
.runner { height: 56px; }
```

Those four numbers become `Theme(width, height, pad_x, pad_y, runner_h)`.
If the kit uses custom properties (`--slide-w`, `--pad-x`), read the `:root`
block. If nothing is declared, measure from a slide's outermost element.

Common canvases and their PowerPoint equivalents:

| px | inches | Notes |
|---|---|---|
| 1280 × 720 | 13.333 × 7.5 | 16:9, the default for new decks |
| 1920 × 1080 | 20 × 11.25 | Same ratio; set the canvas, don't scale coordinates |
| 1024 × 768 | 10.667 × 8 | 4:3, older corporate templates |

Conversion is always `px ÷ 96 = inches`, `px × 9525 = EMU`. `deckkit.E()` does it.

## 2. Type scale

Pull every text class the kit defines, with size / weight / line-height /
letter-spacing. A kit usually has 6–10 steps; write them down as a table and use
only those steps. Inventing an in-between size is the fastest way to make a deck
look unlike its kit.

Watch for:

- **Negative letter-spacing on display sizes.** Many kits tighten headlines by
  −0.5 to −1.5 px. `Slide.text(spacing=...)` takes kit pixels and converts to
  the `spc` attribute (1/100 pt).
- **Weights the kit deliberately skips.** If the ladder is 300/400/600/700, do
  not emit 500 — PowerPoint will render it and it will look wrong next to the kit.
- **Line-height as a multiple vs px.** `deckkit` wants px (`lh=`), so multiply
  out: 20 px at 1.5 → `lh=30`.

## 3. Colors

Take the token names as well as the values, and keep the kit's semantics:
which color is *the* accent, which grays are text vs hairlines, what the dark
surface is. A kit with a single accent color is making a point — every
interactive or emphasized element uses it and nothing else. Respect that in the
deck and it reads as one system.

Fill `Theme.colors` with at least `accent`, `accent_on_dark`, `ink`, `muted`,
`hairline`. `svgkit.P` holds the same roles for graphics; override its fields
once at the top of the build script.

## 4. Archetypes

List the slide patterns the kit ships, by the markup you find. Typical set:

| Archetype | Tell-tale markup | Use for |
|---|---|---|
| Title | hero-size text, no runner | cover |
| Section divider | dark surface, large numeral | chapter breaks |
| Bullets | eyebrow + title + rule + `ul` | the default content slide |
| Split | two-column grid, one side a figure | claim + evidence |
| Card grid | 2–4 rounded rects with hairline | parallel items |
| Stat row | oversized numerals + labels | headline numbers |
| Table | horizontal hairlines only | comparisons |
| Quote | dark surface, large light text | one sentence worth pausing on |
| Full-bleed | image to the edges, caption overlay | photography |

If the kit annotates its own slides (many do, in comments or a caption block),
read those notes — they usually state the intended use and the constraint
("불릿 5개 이하", "table 7행 이내"). Honor them; they came from the designer.

## 5. What the kit deliberately forbids

Most kits carry a do/don't list. Transcribe the "don't" items into your build
rules, because they are what keeps the deck coherent: no second accent color, no
shadows on cards, no decorative gradients, no rounding on full-bleed tiles. When
a slide feels flat, the kit's own answer is usually "change the surface color",
not "add chrome".
