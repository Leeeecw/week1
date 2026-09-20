# Graphics: choosing and drawing them

Slide graphics are read in seconds from across a room, so they are not
dashboards. One idea per figure, direct labels over legends, and nothing drawn
that is not carrying information.

## Pick the form from the data's job

| The slide is saying… | Form | `svgkit` |
|---|---|---|
| these categories differ in size | horizontal bars (labels have room) | `bars_h` |
| two series differ across a few periods | grouped bars | `bars_grouped` |
| this changed over time | line, 1–2 series | `lines` |
| estimates disagree about a quantity | range dots | `range_dots` |
| three cases each show the same shape | small multiples, shared scale | `small_multiples` |
| A only reaches C through B | flow diagram | `flow_steps` |
| here are the three things | card row | `cards` or native shapes |
| one number is the point | a big number in text, no chart | `Slide.text` |

Two rules that prevent most bad slide charts:

- **Never two y-axes.** Different scales go in two charts, small multiples, or
  indexed to a common base. A dual axis lets the author imply any correlation
  they like.
- **Nine bars in one chart is three panels.** Split by category into small
  multiples with a shared scale; the comparison stays honest and every label
  gets room.

## Color

Carry the subject series in the kit's accent and put comparison series in
neutral grays (`svgkit.P.series_gray`, `series_gray_light`). Blue-vs-gray
separates on lightness, so it survives color-vision deficiency, grayscale
printing and a bad projector — no validator required.

- **Color follows the entity, never its rank.** Coloring bars by whether they
  cross some threshold encodes the conclusion into the palette; if a value
  matters, label it.
- **Text wears text colors.** Values, axis labels and legends stay in ink/muted
  gray; the colored mark beside them carries the identity.
- On dark surfaces switch to the kit's on-dark accent (e.g. `#2997ff`) — a
  mid-blue disappears against near-black.

## Labels

- Direct-label the end of each line and the top of each bar. A legend is for
  two or more series that cannot be labelled in place; when you need one, keep
  it in one row above the plot.
- Label every bar's value, but not every point on a line — label the first,
  the last, and whatever the sentence in the headline refers to.
- Gridlines are recessive (`P.grid`, 1 px) and the baseline is a hairline. Axis
  ticks at 4–5 intervals; more is noise at slide scale.
- Put the source in the figure (12 px, muted) **or** in the slide text, not
  both. Duplicated sources are the most common redundancy in generated decks.
- Minimum type in a figure is 12 px at 1280 × 720. If a label needs to be
  smaller to fit, the figure is too dense — cut a series or split the slide.

## Sizing

Draw at the size the graphic will occupy. `svgkit` functions take explicit
`w, h`, so pass the hole you left in the layout (e.g. `520 × 400`). Scaling an
SVG after the fact rescales its type along with it and quietly breaks the
deck's type scale.

Leave room inside the box for what sits outside the plot: axis labels on the
left (~40–60 px), tick labels below (~30 px), a source note (~20 px), a legend
above (~30 px). Charts that "fit" until the labels appear are why previews
exist.

## Diagrams

For anything that is not a chart, compose from `svgkit` primitives (`R`, `T`,
`L`, `C`, `path`, `arrow_marker`). Diagrams earn their place when they show a
*mechanism* — a chain with a leak in it, a before/after of the same system, a
formula broken into its factors. A diagram that is three labelled boxes with no
relation between them is a bullet list wearing a costume; use bullets.

Keep diagram geometry on the same grid as the slide: the same 18 px card
radius, the same hairline, the same accent. A figure drawn to its own taste is
visible as a foreign object even when it is pretty.

## Why SVG rather than PNG or a native chart

SVG stays sharp at any zoom and on any projector, stays editable and diffable
afterwards, and matches the kit's colors exactly. `deckkit` embeds a PNG
fallback alongside it automatically for old viewers.

Use a **native PowerPoint chart** (`python-pptx`'s `add_chart`) instead when the
user needs to edit the data in PowerPoint or relink it to a spreadsheet. Use a
**raster image** only for photographs.
