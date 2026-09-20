# -*- coding: utf-8 -*-
"""
SVG graphics for the BOK AI/GPT deck, drawn in the Apple reference design language.

Palette rules applied (dataviz skill):
  - one accent hue (#0066cc) carries the "subject" series; comparison series use
    neutral grays that separate from it on lightness alone, so the pairs stay
    legible under any CVD simulation. (validate_palette.js needs node, which is
    not installed here, so the palette is kept to blue-vs-neutral by construction.)
  - one axis per chart, never two scales
  - thin marks, recessive gridlines, direct labels instead of a value on every tick
  - legend present whenever two series share a panel
"""

PRIMARY = "#0066cc"
SKY = "#2997ff"
INK = "#1d1d1f"
MUTED = "#7a7a7a"
MUTED80 = "#333333"
HAIRLINE = "#e0e0e0"
PARCHMENT = "#f5f5f7"
GRAY_SERIES = "#b0b0b5"      # neutral counterpart series on light surfaces
GRAY_SERIES_D = "#86868b"
TILE = "#272729"
ON_DARK = "#ffffff"
BODY_MUTED = "#cccccc"
HAIRLINE_D = "rgba(255,255,255,0.18)"

KO = "Malgun Gothic, Arial, sans-serif"   # Korean-bearing labels
EN = "Arial, sans-serif"


def _has_hangul(s):
    return any("가" <= ch <= "힣" or "㄰" <= ch <= "㆏" for ch in str(s))


def T(x, y, s, size=15, weight=400, fill=INK, anchor="start", spacing=None, family=None):
    fam = family or (KO if _has_hangul(s) else EN)
    sp = ' letter-spacing="%s"' % spacing if spacing else ""
    s = (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%d" font-weight="%d" '
            'fill="%s" text-anchor="%s"%s>%s</text>' % (x, y, fam, size, weight, fill, anchor, sp, s))


def R(x, y, w, h, fill, rx=0, stroke=None, sw=1):
    st = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"%s/>'
            % (x, y, w, h, rx, fill, st))


def L(x1, y1, x2, y2, stroke=HAIRLINE, sw=1, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            % (x1, y1, x2, y2, stroke, sw, d))


def svg(w, h, body, bg=None):
    head = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d">' % (w, h, w, h))
    back = R(0, 0, w, h, bg) if bg else ""
    return head + back + body + "</svg>"


def arrow_defs(color=PRIMARY, name="ah"):
    return ('<defs><marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
            'markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" '
            'fill="%s"/></marker></defs>' % (name, color))


# ---------------------------------------------------------------- 1. micro → macro
def flow_micro_macro(w=520, h=400):
    """왜 미시 효과가 거시로 바로 이어지지 않는가 — 3단 전달 경로."""
    b = [arrow_defs(PRIMARY, "ah1"), arrow_defs(MUTED, "ah2")]
    steps = [
        ("업무(task)", "AI 적용 업무의 효율 개선", "이미 관측됨", PRIMARY),
        ("기업(firm)", "여러 업무가 결합되어 산출로", "아직 불분명", MUTED80),
        ("경제(GDP)", "기업의 성과가 경제 전체로", "확인되지 않음", MUTED80),
    ]
    y = 8
    bh = 104
    gap = 40
    for i, (title, desc, state, color) in enumerate(steps):
        top = y + i * (bh + gap)
        b.append(R(0, top, w, bh, "#ffffff", 18, HAIRLINE, 1))
        b.append(R(0, top, 4, bh, color, 2))
        b.append(T(28, top + 38, title, 21, 600, INK))
        b.append(T(28, top + 66, desc, 15, 400, MUTED))
        b.append(T(w - 28, top + 38, state, 15, 600, color, anchor="end"))
        if i < 2:
            cx = w / 2
            b.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" '
                     'marker-end="url(#ah2)"/>' % (cx, top + bh + 6, cx, top + bh + gap - 8, MUTED))
            note = "기업 활동에서 차지하는 비중" if i == 0 else "경제 전체에서 차지하는 비중"
            b.append(T(cx + 16, top + bh + gap / 2 + 5, "× " + note, 14, 400, MUTED))
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- 2. task-level gains
def bars_task_gains(w=560, h=360):
    rows = [
        ("코딩 속도", "Peng et al.(2023)", 55.8, PRIMARY),
        ("글쓰기 과제", "Noy & Zhang(2023)", 40.0, PRIMARY),
        ("고객상담 해결건수", "Brynjolfsson et al.(2025)", 23.9, PRIMARY),
        ("업무시간 단축", "서동현 외(2026), 설문", 3.8, GRAY_SERIES_D),
    ]
    left, top = 168, 54
    plot_w = w - left - 60
    bh, gap = 34, 42
    mx = 60.0
    b = []
    for gx in (0, 20, 40, 60):
        x = left + plot_w * gx / mx
        b.append(L(x, top - 10, x, top + len(rows) * (bh + gap) - gap + 6, HAIRLINE, 1))
        b.append(T(x, top + len(rows) * (bh + gap) - gap + 26, "%d%%" % gx, 13, 400, MUTED, anchor="middle"))
    for i, (label, src, v, color) in enumerate(rows):
        y = top + i * (bh + gap)
        bw = plot_w * v / mx
        b.append(R(left, y, bw, bh, color, 4))
        b.append(T(left + bw + 12, y + bh - 10, "%.1f%%" % v, 17, 600, INK))
        b.append(T(left - 16, y + 16, label, 16, 600, INK, anchor="end"))
        b.append(T(left - 16, y + 34, src, 13, 400, MUTED, anchor="end"))
    # legend
    b.append(R(left, 8, 11, 11, PRIMARY, 2))
    b.append(T(left + 18, 18, "통제된 실험 환경", 13, 400, MUTED80))
    b.append(R(left + 160, 8, 11, 11, GRAY_SERIES_D, 2))
    b.append(T(left + 178, 18, "실제 업무환경 설문", 13, 400, MUTED80))
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- 3. Hulten decomposition
def hulten_compare(w=1104, h=330):
    b = [arrow_defs(PRIMARY, "ah3")]
    # formula band
    b.append(R(0, 0, w, 68, PARCHMENT, 11))
    b.append(T(28, 42, "AI에 의한 거시 TFP 증가율  =", 20, 600, INK))
    b.append(T(298, 42, "AI가 실제 적용될 task의 GDP 비중", 20, 400, PRIMARY))
    b.append(T(660, 42, "×", 20, 400, INK))
    b.append(T(688, 42, "해당 task의 총비용 절감률", 20, 400, PRIMARY))
    rows = [
        ("Acemoglu (2024)", 4.6, 14.4, "0.66%", "연 0.07%p", GRAY_SERIES_D),
        ("Aghion & Bunel (2025) 상한", 54.4, 22.8, "12.4%", "연 1.24%p", PRIMARY),
    ]
    top = 104
    rh = 96
    barx, barw = 330, 300
    for i, (name, a, bb, tot, ann, color) in enumerate(rows):
        y = top + i * (rh + 16)
        b.append(T(0, y + 30, name, 17, 600, INK))
        b.append(T(0, y + 56, "GDP 비중 %.1f%%  ×  절감률 %.1f%%" % (a, bb), 14, 400, MUTED))
        # proportional bar for the GDP share
        b.append(R(barx, y + 14, barw, 26, "#ffffff", 4, HAIRLINE, 1))
        b.append(R(barx, y + 14, barw * a / 100.0, 26, color, 4))
        b.append(T(barx + barw + 12, y + 33, "%.1f%%" % a, 15, 600, color))
        b.append(T(barx, y + 62, "AI가 적용될 task의 GDP 비중", 13, 400, MUTED))
        # result
        rx = barx + barw + 150
        b.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" '
                 'marker-end="url(#ah3)"/>' % (rx, y + 27, rx + 46, y + 27, MUTED))
        b.append(T(rx + 62, y + 22, "향후 10년 TFP 이득", 14, 400, MUTED))
        b.append(T(rx + 62, y + 52, tot, 28, 600, color))
        b.append(T(rx + 152, y + 52, "(%s)" % ann, 15, 400, MUTED80))
        if i == 0:
            b.append(L(0, y + rh + 8, w, y + rh + 8, HAIRLINE, 1))
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- 4. forecast ranges
def forecast_ranges(w=1000, h=404):
    rows = [
        ("Anthropic (2026)", 0.7, 2.6, "노동생산성 · 미국"),
        ("Goldman Sachs (2023)", 1.5, 1.5, "노동생산성 · 미국"),
        ("Aghion & Bunel (2025)", 0.07, 1.24, "TFP · 미국"),
        ("OECD (2026)", 0.03, 1.2, "1인당 실질소득 · OECD"),
        ("OECD (2024)", 0.24, 0.97, "TFP · OECD"),
        ("ECB (2026)", 0.2, 0.6, "TFP · 유로존"),
        ("McKinsey (2023)", 0.1, 0.6, "노동생산성 · 세계"),
        ("Acemoglu (2024)", 0.07, 0.07, "TFP · 미국"),
    ]
    left = 250
    right = w - 150
    plot_w = right - left
    top = 46
    rh = 43
    mx = 2.8
    b = []
    for gx in (0, 0.5, 1.0, 1.5, 2.0, 2.5):
        x = left + plot_w * gx / mx
        b.append(L(x, top - 14, x, top + len(rows) * rh - 6, HAIRLINE, 1))
        b.append(T(x, top - 24, "%.1f" % gx, 13, 400, MUTED, anchor="middle"))
    b.append(T(right + 10, top - 24, "%p", 12, 400, MUTED))
    for i, (name, lo, hi, meta) in enumerate(rows):
        y = top + i * rh + 8
        x1 = left + plot_w * lo / mx
        x2 = left + plot_w * hi / mx
        b.append(T(left - 20, y + 5, name, 15, 600, INK, anchor="end"))
        if hi > lo:
            b.append(R(x1, y - 4, max(x2 - x1, 2), 8, PRIMARY, 4))
            b.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (x1, y, PRIMARY))
            b.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (x2, y, PRIMARY))
            b.append(T(x2 + 14, y + 5, "%.2f~%.2f" % (lo, hi), 14, 600, MUTED80))
        else:
            b.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (x1, y, PRIMARY))
            b.append(T(x1 + 14, y + 5, "%.2f" % lo, 14, 600, MUTED80))
        b.append(T(left - 20, y + 22, meta, 12, 400, MUTED, anchor="end"))
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- 5. GPT contribution small multiples
def gpt_contribution(w=1040, h=340):
    panels = [
        ("증기 (영국)", [("1760–1830", 0.014), ("1830–1870", 0.30), ("1870–1910", 0.31)]),
        ("전기 (미국)", [("1899–1919", 0.10), ("1919–1929", 0.14), ("1929–1941", 0.20)]),
        ("정보기술 (미국)", [("1974–1995", 0.77), ("1995–2004", 1.50), ("2004–2012", 0.64)]),
    ]
    axis_w = 42
    pw = (w - axis_w - 2 * 48) / 3.0
    base = h - 56
    top = 60
    mx = 1.6
    b = []
    for pi, (name, series) in enumerate(panels):
        ox = axis_w + pi * (pw + 48)
        b.append(T(ox, 22, name, 17, 600, INK))
        b.append(L(ox, base, ox + pw, base, HAIRLINE, 1))
        for gy in (0.5, 1.0, 1.5):
            y = base - (base - top) * gy / mx
            b.append(L(ox, y, ox + pw, y, "#f0f0f0", 1))
            if pi == 0:
                b.append(T(ox - 10, y + 4, "%.1f" % gy, 12, 400, MUTED, anchor="end"))
        bw = 56
        step = pw / 3.0
        for i, (era, v) in enumerate(series):
            x = ox + step * i + (step - bw) / 2
            bh = (base - top) * v / mx
            b.append(R(x, base - bh, bw, max(bh, 2), PRIMARY, 4))
            b.append(T(x + bw / 2, base - bh - 10, ("%.3f" % v).rstrip("0").rstrip("."), 14, 600, INK, anchor="middle"))
            b.append(T(x + bw / 2, base + 22, era, 12, 400, MUTED, anchor="middle"))
    b.append(T(0, h - 8, "경제 전체의 노동생산성 증가율에 대한 기여도 (연평균, %p) · 자료: Crafts(2021)", 12, 400, MUTED))
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- 6. UK power sources
def uk_steam_share(w=520, h=330):
    pts = [(1760, 5.9), (1800, 20.6), (1830, 47.1), (1870, 89.6), (1907, 98.1)]
    left, right = 58, w - 24
    top, base = 46, h - 56
    b = []
    for gy in (0, 25, 50, 75, 100):
        y = base - (base - top) * gy / 100.0
        b.append(L(left, y, right, y, "#f0f0f0", 1))
        b.append(T(left - 10, y + 4, "%d%%" % gy, 12, 400, MUTED, anchor="end"))

    def px(year):
        return left + (right - left) * (year - 1760) / (1907 - 1760.0)

    def py(v):
        return base - (base - top) * v / 100.0

    d = " ".join(("M" if i == 0 else "L") + " %.1f %.1f" % (px(y), py(v)) for i, (y, v) in enumerate(pts))
    b.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (d, PRIMARY))
    for i, (year, v) in enumerate(pts):
        b.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="#ffffff" stroke-width="2"/>'
                 % (px(year), py(v), PRIMARY))
        if i == 0:   # keep the first label clear of the 0% tick and the axis
            b.append(T(px(year) + 14, py(v) + 5, "%.1f%%" % v, 13, 600, INK))
        else:
            b.append(T(px(year), py(v) - 14, "%.1f%%" % v, 13, 600, INK, anchor="middle"))
        b.append(T(px(year), base + 22, str(year), 12, 400, MUTED, anchor="middle"))
    b.append(T(0, 18, "영국 총 설치 마력 중 증기기관 비중", 15, 600, INK))
    b.append(T(0, h - 8, "자료: Crafts(2004)", 12, 400, MUTED))
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- 7. shaft vs unit drive
def shaft_to_unit(w=1040, h=300):
    b = [arrow_defs(SKY, "ah4")]
    panel_w = 420
    gap = 200
    # --- left: line shaft
    ox = 0
    b.append(T(ox, 22, "① 기존 방식 — 중앙 동력 + 천장 동력축", 17, 600, ON_DARK))
    b.append(T(ox, 46, "동력축 하나에 모든 기계가 물려 있어 배치와 속도를 바꿀 수 없음", 13, 400, BODY_MUTED))
    b.append(R(ox, 70, panel_w, 180, "#2a2a2c", 11, "rgba(255,255,255,0.14)", 1))
    b.append(R(ox + 18, 150, 70, 76, SKY, 5))
    b.append(T(ox + 53, 194, "엔진", 14, 600, "#101013", anchor="middle"))
    b.append(L(ox + 18, 108, ox + panel_w - 18, 108, "#8a8a90", 5))
    b.append(T(ox + panel_w - 18, 98, "동력축(shaft)", 12, 400, BODY_MUTED, anchor="end"))
    for i in range(5):
        mx_ = ox + 116 + i * 60
        b.append(L(mx_, 108, mx_, 176, "#6a6a70", 2))
        b.append(R(mx_ - 20, 176, 40, 50, "#3a3a3e", 5, "rgba(255,255,255,0.16)", 1))
    b.append(L(ox + 88, 188, ox + 116, 188, "#8a8a90", 3))
    # --- arrow
    ax = panel_w + 40
    b.append('<line x1="%.1f" y1="160" x2="%.1f" y2="160" stroke="%s" stroke-width="2.5" '
             'marker-end="url(#ah4)"/>' % (ax, ax + gap - 80, SKY))
    b.append(T(ax + (gap - 80) / 2, 140, "분산형 동력", 14, 600, SKY, anchor="middle"))
    b.append(T(ax + (gap - 80) / 2, 186, "동력축 제거", 13, 400, BODY_MUTED, anchor="middle"))
    # --- right: unit drive
    ox = panel_w + gap
    b.append(T(ox, 22, "② 재조직 이후 — 기계마다 개별 모터", 17, 600, ON_DARK))
    b.append(T(ox, 46, "속도를 따로 조절하고 작업 동선에 맞춰 재배치할 수 있게 됨", 13, 400, BODY_MUTED))
    b.append(R(ox, 70, panel_w, 180, "#2a2a2c", 11, "rgba(255,255,255,0.14)", 1))
    for i in range(5):
        mx_ = ox + 46 + i * 66
        my = 118 if i % 2 == 0 else 158
        b.append(R(mx_ - 22, my, 44, 54, "#3a3a3e", 5, "rgba(255,255,255,0.16)", 1))
        b.append('<circle cx="%.1f" cy="%.1f" r="9" fill="%s"/>' % (mx_, my - 14, SKY))
    b.append(T(ox + panel_w / 2, 238, "천장을 가로지르는 동력축이 사라짐", 13, 400, BODY_MUTED, anchor="middle"))
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- 8. US manufacturing power mix
def us_power_mix(w=540, h=340):
    years = [1889, 1899, 1909, 1919, 1929, 1939]
    steam = [78.3, 81.4, 65.3, 40.7, 18.5, 11.4]
    elec = [0.3, 4.8, 24.7, 53.1, 78.4, 86.1]
    left, right = 54, w - 20
    top, base = 52, h - 58
    b = []
    for gy in (0, 25, 50, 75, 100):
        y = base - (base - top) * gy / 100.0
        b.append(L(left, y, right, y, "#f0f0f0", 1))
        b.append(T(left - 10, y + 4, "%d%%" % gy, 12, 400, MUTED, anchor="end"))

    def px(i):
        return left + (right - left) * i / (len(years) - 1.0)

    def py(v):
        return base - (base - top) * v / 100.0

    for series, color, name in ((steam, GRAY_SERIES_D, "증기"), (elec, PRIMARY, "전기")):
        d = " ".join(("M" if i == 0 else "L") + " %.1f %.1f" % (px(i), py(v)) for i, v in enumerate(series))
        b.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.5" stroke-linejoin="round"/>' % (d, color))
        for i, v in enumerate(series):
            b.append('<circle cx="%.1f" cy="%.1f" r="4" fill="%s" stroke="#ffffff" stroke-width="2"/>'
                     % (px(i), py(v), color))
    # crossover marker at 1919
    b.append(L(px(3), top - 6, px(3), base, MUTED, 1, "4 4"))
    b.append(T(px(3) + 8, top + 4, "1919년 역전", 13, 600, INK))
    b.append(T(px(3) + 8, top + 22, "전기 53.1% > 증기 40.7%", 12, 400, MUTED))
    for i, y in enumerate(years):
        b.append(T(px(i), base + 22, str(y), 12, 400, MUTED, anchor="middle"))
    b.append(T(px(0), py(steam[0]) - 14, "증기", 14, 600, GRAY_SERIES_D))
    b.append(T(px(5), py(elec[5]) - 14, "전기", 14, 600, PRIMARY, anchor="end"))
    b.append(T(0, 20, "미국 제조업 동력원 비중", 15, 600, INK))
    b.append(T(0, h - 8, "자료: Devine(1983)", 12, 400, MUTED))
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- 9. IT producing vs using
def it_producing_using(w=520, h=380):
    groups = [("1987–1995", 0.37, 0.75), ("1995–2000", 0.54, 1.58)]
    left, right = 58, w - 20
    top, base = 66, h - 96
    mx = 1.8
    b = []
    for gy in (0, 0.5, 1.0, 1.5):
        y = base - (base - top) * gy / mx
        b.append(L(left, y, right, y, "#f0f0f0", 1))
        b.append(T(left - 10, y + 4, "%.1f" % gy, 12, 400, MUTED, anchor="end"))
    gw = (right - left) / 2.0
    bw = 66
    for gi, (name, prod, use) in enumerate(groups):
        cx = left + gw * gi + gw / 2
        for j, (v, color) in enumerate(((prod, GRAY_SERIES_D), (use, PRIMARY))):
            x = cx - bw - 4 + j * (bw + 8)
            bh = (base - top) * v / mx
            b.append(R(x, base - bh, bw, bh, color, 4))
            b.append(T(x + bw / 2, base - bh - 10, "%.2f" % v, 14, 600, INK, anchor="middle"))
        b.append(T(cx, base + 24, name, 13, 400, MUTED, anchor="middle"))
    b.append(R(left, 20, 11, 11, GRAY_SERIES_D, 2))
    b.append(T(left + 18, 30, "IT 생산부문", 13, 400, MUTED80))
    b.append(R(left + 130, 20, 11, 11, PRIMARY, 2))
    b.append(T(left + 148, 30, "IT 활용부문", 13, 400, MUTED80))
    b.append(T(0, h - 40, "기여도 증감:  생산부문 +0.17%p   ·   활용부문 +0.83%p", 13, 600, INK))
    b.append(T(0, h - 8, "미국 연평균 노동생산성 성장 기여도(%p) · 자료: Stiroh(2002)", 12, 400, MUTED))
    return svg(w, h, "".join(b))


# ---------------------------------------------------------------- 10. conditions for AI diffusion
def ai_conditions(w=1040, h=190):
    items = [
        ("01", "연관 기술의 발전", "고압증기가 증기기관의 쓰임을 넓혔듯,\nAI 활용의 문턱을 낮추는 기술이 필요"),
        ("02", "업무 프로세스의 재설계", "확률적 산출을 전제로 한 검증 절차 —\n기존 소프트웨어와 같은 방식으로 쓸 수 없음"),
        ("03", "현장으로의 확장", "사무직 챗봇을 넘어 생산공정까지.\n피지컬 AI가 그 계기가 될 수 있음"),
    ]
    cw = (w - 2 * 28) / 3.0
    b = []
    for i, (no, title, desc) in enumerate(items):
        x = i * (cw + 28)
        b.append(R(x, 0, cw, h, "#ffffff", 18, HAIRLINE, 1))
        b.append('<circle cx="%.1f" cy="%.1f" r="17" fill="%s"/>' % (x + 41, 45, PRIMARY))
        b.append(T(x + 41, 50, no, 14, 600, "#ffffff", anchor="middle"))
        b.append(T(x + 24, 100, title, 19, 600, INK))
        for j, line in enumerate(desc.split("\n")):
            b.append(T(x + 24, 132 + j * 24, line, 14, 400, MUTED))
    return svg(w, h, "".join(b))


ALL = {
    "flow-micro-macro": flow_micro_macro,
    "bars-task-gains": bars_task_gains,
    "hulten-compare": hulten_compare,
    "forecast-ranges": forecast_ranges,
    "gpt-contribution": gpt_contribution,
    "uk-steam-share": uk_steam_share,
    "shaft-to-unit": shaft_to_unit,
    "us-power-mix": us_power_mix,
    "it-producing-using": it_producing_using,
    "ai-conditions": ai_conditions,
}
