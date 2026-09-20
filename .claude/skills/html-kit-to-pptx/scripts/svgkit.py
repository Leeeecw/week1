# -*- coding: utf-8 -*-
"""
svgkit — small SVG drawing helpers plus a handful of chart forms.

Charts here are plain SVG strings. That matters for two reasons: PowerPoint
renders embedded SVG as vector art (no blur at any zoom), and an SVG stays
diffable and editable afterwards, unlike a rendered PNG or a native chart part.

The chart functions are deliberately few and boring — horizontal bars, grouped
bars, lines, range dots, small multiples. They cover most of what a slide needs.
When a graphic is a diagram rather than a chart (a flow, a before/after, a
formula breakdown), compose it from the primitives; `flow_steps` and `cards`
show the pattern.

Every function takes explicit width/height and draws inside that box, so you can
size a graphic to the hole you left for it in the layout instead of scaling
afterwards.

Palette rule of thumb: carry the subject series in the kit's accent color and
put every comparison series in neutral grays. Blue-vs-gray separates on
lightness, so it survives color-vision deficiency and grayscale printing without
needing a validator.
"""


class Palette(object):
    def __init__(self, accent="#0066cc", ink="#1d1d1f", muted="#7a7a7a",
                 muted_strong="#333333", hairline="#e0e0e0", grid="#f0f0f0",
                 series_gray="#86868b", series_gray_light="#b0b0b5",
                 on_dark="#ffffff", muted_on_dark="#cccccc", accent_on_dark="#2997ff"):
        self.accent = accent
        self.ink = ink
        self.muted = muted
        self.muted_strong = muted_strong
        self.hairline = hairline
        self.grid = grid
        self.series_gray = series_gray
        self.series_gray_light = series_gray_light
        self.on_dark = on_dark
        self.muted_on_dark = muted_on_dark
        self.accent_on_dark = accent_on_dark


P = Palette()

LATIN = "Arial, sans-serif"
CJK = "Malgun Gothic, Arial, sans-serif"      # override for other locales


def has_cjk(s):
    return any(
        "぀" <= ch <= "ヿ" or "㐀" <= ch <= "鿿"
        or "가" <= ch <= "힣" or "㄰" <= ch <= "㆏"
        for ch in str(s)
    )


# ------------------------------------------------------------------ primitives
def T(x, y, s, size=15, weight=400, fill=None, anchor="start", spacing=None, family=None):
    """Text. y is the baseline. Font family is picked per string so CJK labels
    do not fall back to tofu when the SVG is rasterized for the PNG fallback."""
    fill = fill or P.ink
    fam = family or (CJK if has_cjk(s) else LATIN)
    sp = ' letter-spacing="%s"' % spacing if spacing else ""
    s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%s" font-weight="%d" '
            'fill="%s" text-anchor="%s"%s>%s</text>'
            % (x, y, fam, size, weight, fill, anchor, sp, s))


def R(x, y, w, h, fill, rx=0, stroke=None, sw=1):
    st = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"%s/>'
            % (x, y, w, h, rx, fill, st))


def L(x1, y1, x2, y2, stroke=None, sw=1, dash=None):
    stroke = stroke or P.hairline
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, stroke, sw, d))


def C(cx, cy, r, fill, stroke=None, sw=2):
    st = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
    return '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"%s/>' % (cx, cy, r, fill, st)


def path(d, stroke, sw=2.5, fill="none"):
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linejoin="round"/>'
            % (d, fill, stroke, sw))


def arrow_marker(color, name="ah"):
    return ('<defs><marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            'markerHeight="7" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/></marker></defs>' % (name, color))


def svg(w, h, body, bg=None):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">'
            % (w, h, w, h)
            + (R(0, 0, w, h, bg) if bg else "")
            + body + "</svg>")


def legend(x, y, entries, size=13, gap=150):
    """entries: [(label, color), ...]. Two or more series always need one."""
    out = []
    for i, (label, color) in enumerate(entries):
        ox = x + i * gap
        out.append(R(ox, y - 10, 11, 11, color, 2))
        out.append(T(ox + 18, y, label, size, 400, P.muted_strong))
    return "".join(out)


# ------------------------------------------------------------------ charts
def bars_h(w, h, rows, vmax=None, unit="%", label_w=160, top=48, bar_h=34, gap=42,
           ticks=4, note=None):
    """Horizontal bars — the safe default when categories have long text labels.

    rows: [(label, sublabel, value, color)] — sublabel may be "" (a source, a
    date, whatever the reader needs to trust the number).
    """
    body = []
    vmax = vmax or max(r[2] for r in rows) * 1.1
    left = label_w
    plot_w = w - left - 70
    bottom = top + len(rows) * (bar_h + gap) - gap
    # the tick row and the note live below the last bar; if they do not fit they
    # would silently overlap, so say so while the size is still easy to change
    needed = bottom + 34 + (26 if note else 0)
    if needed > h:
        raise ValueError(
            "bars_h: %d rows need height >= %d (got %d). Raise h, or shrink "
            "bar_h/gap/top." % (len(rows), int(needed), int(h)))
    for i in range(ticks + 1):
        v = vmax * i / ticks
        x = left + plot_w * v / vmax
        body.append(L(x, top - 10, x, bottom + 6, P.hairline))
        body.append(T(x, bottom + 26, ("%g" % round(v, 2)) + unit, 13, 400, P.muted, "middle"))
    for i, (label, sub, v, color) in enumerate(rows):
        y = top + i * (bar_h + gap)
        bw = plot_w * v / vmax
        body.append(R(left, y, max(bw, 2), bar_h, color or P.accent, 4))
        body.append(T(left + bw + 12, y + bar_h - 10, ("%g" % v) + unit, 17, 600, P.ink))
        body.append(T(left - 16, y + 16, label, 16, 600, P.ink, "end"))
        if sub:
            body.append(T(left - 16, y + 34, sub, 13, 400, P.muted, "end"))
    if note:
        body.append(T(0, h - 8, note, 12, 400, P.muted))
    return svg(w, h, "".join(body))


def bars_grouped(w, h, groups, series_names, colors=None, vmax=None, fmt="%.2f",
                 left=58, top=66, bottom_pad=70, bar_w=66, note=None):
    """groups: [(group_label, [v1, v2, ...])]. One value per series per group."""
    colors = colors or [P.accent, P.series_gray, P.series_gray_light]
    body = []
    vmax = vmax or max(max(v) for _, v in groups) * 1.15
    right = w - 20
    base = h - bottom_pad
    for i in range(4):
        v = vmax * i / 3.0
        y = base - (base - top) * v / vmax
        body.append(L(left, y, right, y, P.grid))
        body.append(T(left - 10, y + 4, fmt % v, 12, 400, P.muted, "end"))
    gw = (right - left) / float(len(groups))
    n = len(series_names)
    for gi, (name, values) in enumerate(groups):
        cx = left + gw * gi + gw / 2
        span = n * bar_w + (n - 1) * 8
        for j, v in enumerate(values):
            x = cx - span / 2 + j * (bar_w + 8)
            bh = (base - top) * v / vmax
            body.append(R(x, base - bh, bar_w, max(bh, 2), colors[j % len(colors)], 4))
            body.append(T(x + bar_w / 2, base - bh - 10, fmt % v, 14, 600, P.ink, "middle"))
        body.append(T(cx, base + 24, name, 13, 400, P.muted, "middle"))
    if len(series_names) > 1:
        body.append(legend(left, 30, list(zip(series_names, colors)), gap=130))
    if note:
        body.append(T(0, h - 8, note, 12, 400, P.muted))
    return svg(w, h, "".join(body))


def lines(w, h, x_labels, series, colors=None, vmax=100, unit="%", title=None,
          note=None, left=56, top=52, bottom_pad=58, mark_index=None, mark_text=None):
    """series: [(name, [values])]. Two lines max before it gets noisy;
    direct-label the ends instead of leaning on the legend."""
    colors = colors or [P.accent, P.series_gray]
    body = []
    right = w - 20
    base = h - bottom_pad
    n = len(x_labels)
    for i in range(5):
        v = vmax * i / 4.0
        y = base - (base - top) * v / vmax
        body.append(L(left, y, right, y, P.grid))
        body.append(T(left - 10, y + 4, ("%g" % round(v, 2)) + unit, 12, 400, P.muted, "end"))

    def px(i):
        return left + (right - left) * i / float(max(n - 1, 1))

    def py(v):
        return base - (base - top) * v / float(vmax)

    if mark_index is not None:
        body.append(L(px(mark_index), top - 6, px(mark_index), base, P.muted, 1, "4 4"))
        if mark_text:
            for k, line in enumerate(mark_text if isinstance(mark_text, (list, tuple)) else [mark_text]):
                body.append(T(px(mark_index) + 8, top + 4 + k * 18, line,
                              13 if k == 0 else 12, 600 if k == 0 else 400,
                              P.ink if k == 0 else P.muted))
    for si, (name, values) in enumerate(series):
        color = colors[si % len(colors)]
        d = " ".join(("M" if i == 0 else "L") + " %.1f %.1f" % (px(i), py(v))
                     for i, v in enumerate(values))
        body.append(path(d, color))
        for i, v in enumerate(values):
            body.append(C(px(i), py(v), 4.5, color, "#ffffff", 2))
        end = len(values) - 1
        body.append(T(px(end), py(values[end]) - 14, name, 14, 600, color, "end"))
    for i, lab in enumerate(x_labels):
        body.append(T(px(i), base + 22, lab, 12, 400, P.muted, "middle"))
    if title:
        body.append(T(0, 20, title, 15, 600, P.ink))
    if note:
        body.append(T(0, h - 8, note, 12, 400, P.muted))
    return svg(w, h, "".join(body))


def range_dots(w, h, rows, vmax, label_w=250, top=46, row_h=43, ticks=5, unit="", note=None):
    """rows: [(label, sublabel, lo, hi)]. The right form for "estimates
    disagree" — a bar chart of midpoints would hide exactly what matters."""
    body = []
    left = label_w
    right = w - 150
    plot_w = right - left
    for i in range(ticks + 1):
        v = vmax * i / ticks
        x = left + plot_w * v / vmax
        body.append(L(x, top - 14, x, top + len(rows) * row_h - 6, P.hairline))
        body.append(T(x, top - 24, "%.1f" % v, 13, 400, P.muted, "middle"))
    if unit:
        body.append(T(right + 10, top - 24, unit, 12, 400, P.muted))
    for i, (label, sub, lo, hi) in enumerate(rows):
        y = top + i * row_h + 8
        x1 = left + plot_w * lo / vmax
        x2 = left + plot_w * hi / vmax
        body.append(T(left - 20, y + 5, label, 15, 600, P.ink, "end"))
        if sub:
            body.append(T(left - 20, y + 22, sub, 12, 400, P.muted, "end"))
        if hi > lo:
            body.append(R(x1, y - 4, max(x2 - x1, 2), 8, P.accent, 4))
            body.append(C(x1, y, 5, P.accent))
            body.append(C(x2, y, 5, P.accent))
            body.append(T(x2 + 14, y + 5, "%.2f~%.2f" % (lo, hi), 14, 600, P.muted_strong))
        else:
            body.append(C(x1, y, 5, P.accent))
            body.append(T(x1 + 14, y + 5, "%.2f" % lo, 14, 600, P.muted_strong))
    if note:
        body.append(T(0, h - 8, note, 12, 400, P.muted))
    return svg(w, h, "".join(body))


def small_multiples(w, h, panels, vmax, fmt="%g", axis_w=42, panel_gap=48,
                    top=60, bottom_pad=56, bar_w=56, note=None):
    """panels: [(panel_title, [(bar_label, value)])]. Use this instead of one
    chart with nine bars — a shared scale plus separate panels keeps the
    comparison honest and the labels readable."""
    body = []
    pw = (w - axis_w - (len(panels) - 1) * panel_gap) / float(len(panels))
    base = h - bottom_pad
    for pi, (title, series) in enumerate(panels):
        ox = axis_w + pi * (pw + panel_gap)
        body.append(T(ox, 22, title, 17, 600, P.ink))
        body.append(L(ox, base, ox + pw, base, P.hairline))
        for i in range(1, 4):
            v = vmax * i / 3.0
            y = base - (base - top) * v / vmax
            body.append(L(ox, y, ox + pw, y, P.grid))
            if pi == 0:
                body.append(T(ox - 10, y + 4, fmt % v, 12, 400, P.muted, "end"))
        step = pw / float(len(series))
        for i, (label, v) in enumerate(series):
            x = ox + step * i + (step - bar_w) / 2
            bh = (base - top) * v / vmax
            body.append(R(x, base - bh, bar_w, max(bh, 2), P.accent, 4))
            body.append(T(x + bar_w / 2, base - bh - 10, fmt % v, 14, 600, P.ink, "middle"))
            body.append(T(x + bar_w / 2, base + 22, label, 12, 400, P.muted, "middle"))
    if note:
        body.append(T(0, h - 8, note, 12, 400, P.muted))
    return svg(w, h, "".join(body))


# ------------------------------------------------------------------ diagrams
def flow_steps(w, h, steps, vertical=True, note_gap=40, box_h=104):
    """steps: [(title, description, status, color)] joined by arrows.

    A stacked flow explains a mechanism ("this only reaches that if…") far
    better than three bullets, and it costs ten lines of data.
    """
    body = [arrow_marker(P.muted, "flow_ah")]
    for i, step in enumerate(steps):
        title, desc, status, color = (list(step) + [None] * 4)[:4]
        color = color or P.muted_strong
        if vertical:
            top = i * (box_h + note_gap)
            body.append(R(0, top, w, box_h, "#ffffff", 18, P.hairline, 1))
            body.append(R(0, top, 4, box_h, color, 2))
            body.append(T(28, top + 38, title, 21, 600, P.ink))
            if desc:
                body.append(T(28, top + 66, desc, 15, 400, P.muted))
            if status:
                body.append(T(w - 28, top + 38, status, 15, 600, color, "end"))
            if i < len(steps) - 1:
                cx = w / 2.0
                body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                            'stroke-width="2" marker-end="url(#flow_ah)"/>'
                            % (cx, top + box_h + 6, cx, top + box_h + note_gap - 8, P.muted))
    return svg(w, h, "".join(body))


def cards(w, card_h, items, cols=3, gap=28, numbered=True):
    """items: [(title, [desc lines])]. card_h is the height of ONE card; the
    returned SVG grows downward as rows are added. Numbered cards read as
    "here are the three things" without any extra words."""
    body = []
    h = card_h
    cw = (w - (cols - 1) * gap) / float(cols)
    for i, (title, lines) in enumerate(items):
        x = (i % cols) * (cw + gap)
        y = (i // cols) * (h + gap)
        body.append(R(x, y, cw, h, "#ffffff", 18, P.hairline, 1))
        ty = y + 40
        if numbered:
            body.append(C(x + 41, y + 45, 17, P.accent))
            body.append(T(x + 41, y + 50, "%02d" % (i + 1), 14, 600, "#ffffff", "middle"))
            ty = y + 100
        body.append(T(x + 24, ty, title, 19, 600, P.ink))
        for j, line in enumerate(lines):
            body.append(T(x + 24, ty + 32 + j * 24, line, 14, 400, P.muted))
    rows = (len(items) + cols - 1) // cols
    return svg(w, h * rows + gap * (rows - 1), "".join(body))
