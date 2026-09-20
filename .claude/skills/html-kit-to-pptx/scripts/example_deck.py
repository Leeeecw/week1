# -*- coding: utf-8 -*-
"""
example_deck.py — end-to-end smoke test and copy-paste starting point.

    python example_deck.py /tmp/example.pptx

Builds four slides that between them exercise every moving part: a title,
a dark section divider, a split slide with an embedded SVG chart, and a card
grid. Run it once after installing the dependencies — if the .pptx appears and
the preview PNGs look right, the environment is good and you can start writing
the real deck.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deckkit
import svgkit
from deckkit import Slide, Theme, render_pptx, write_previews

# --- 1. the theme comes from the reference kit -----------------------------
THEME = Theme(
    width=1280, height=720, pad_x=88, pad_y=64, runner_h=56,
    latin_font="Arial", ea_font="Malgun Gothic",
    colors={"accent": "#0066cc", "accent_on_dark": "#2997ff", "ink": "#1d1d1f",
            "muted": "#7a7a7a", "hairline": "#e0e0e0"},
)
INK, ACCENT, MUTED = "#1d1d1f", "#0066cc", "#7a7a7a"
PARCH, TILE, WHITE = "#f5f5f7", "#272729", "#ffffff"


def build(asset_dir):
    # --- 2. graphics are written as SVG files next to the deck -------------
    os.makedirs(asset_dir, exist_ok=True)
    open(os.path.join(asset_dir, "demo-bars.svg"), "w", encoding="utf-8").write(
        svgkit.bars_h(560, 300, [
            ("코딩 속도", "Peng et al. (2023)", 55.8, svgkit.P.accent),
            ("글쓰기 과제", "Noy & Zhang (2023)", 40.0, svgkit.P.accent),
            ("고객상담", "Brynjolfsson et al. (2025)", 23.9, svgkit.P.accent),
        ], vmax=60, bar_h=34, gap=40))

    slides = []

    # --- title ---------------------------------------------------------
    s = Slide(THEME, WHITE)
    s.eyebrow("Reference kit demo")
    s.text(THEME.pad_x, 200, 1000, ["예제 덱 제목이", "두 줄로 들어갑니다"],
           60, 600, INK, lh=74, spacing=-1.4)
    s.text(THEME.pad_x, 360, 900, ["부제는 리드 사이즈로, 한 줄."], 26, 400, MUTED, lh=34)
    s.rect(THEME.pad_x, 552, 120, 3, ACCENT)
    s.text(THEME.pad_x, 594, 700, ["작성자 / 소속"], 15, 600, INK, lh=22)
    s.notes = "발표 노트는 slide.notes 로 넣습니다."
    slides.append(s)

    # --- dark section divider -------------------------------------------
    s = Slide(THEME, TILE, runner="01 · 섹션", page="02", dark=True)
    s.text(THEME.pad_x, 176, 300, ["01"], 140, 600, "#3a3a3d", lh=140, spacing=-6)
    s.eyebrow("Section", y=196)
    s.text(THEME.pad_x + 250, 226, 800, ["섹션 제목"], 52, 600, "#ffffff", lh=60, spacing=-1.2)
    s.text(THEME.pad_x, 400, 860, ["면이 바뀌는 것 자체가 구분선입니다."], 26, 400, "#cccccc", lh=38)
    slides.append(s)

    # --- split: bullets + chart -----------------------------------------
    s = Slide(THEME, WHITE, runner="01 · 섹션", page="03")
    s.eyebrow("Evidence")
    ry = s.head(["업무 수준에서는", "효과가 이미 나타났다"], y=94, lh=52)
    s.bullets(THEME.pad_x, ry + 34, 500, [
        ["통제된 실험에서 업무 효율이 뚜렷하게",
         "개선된 것으로 나타났다."],
        ["다만 AI를 적용하기 쉬운 업무에 한정된",
         "관찰이라는 반론이 있다."],
    ], size=19, lh=28, gap=24)
    s.svg("demo-bars.svg", 632, 210, 560, 300)
    slides.append(s)

    # --- card grid ------------------------------------------------------
    s = Slide(THEME, PARCH, runner="01 · 섹션", page="04")
    s.eyebrow("Summary")
    ry = s.head(["세 가지로 정리하면"], y=94, lh=52)
    cw, gap = (THEME.content_w - 2 * 24) / 3.0, 24
    for i, (title, lines) in enumerate([
            ("적용 범위", ["효과가 나타난 업무가 전체에서", "차지하는 비중이 관건이다."]),
            ("확산 속도", ["과거 범용기술은 정점까지", "20~70년이 걸렸다."]),
            ("보완 투자", ["조직과 프로세스를 함께", "바꿀 때 효과가 커진다."])]):
        x = THEME.pad_x + i * (cw + gap)
        s.rect(x, ry + 44, cw, 190, WHITE, 18, "#e0e0e0", 1)
        s.text(x + 28, ry + 76, cw - 56, [title], 21, 600, INK, lh=28)
        s.text(x + 28, ry + 118, cw - 56, lines, 15, 400, MUTED, lh=23)
    slides.append(s)

    return slides


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "example.pptx"
    assets = os.path.join(os.path.dirname(os.path.abspath(out)) or ".", "example-assets")
    slides = build(assets)
    render_pptx(slides, out, asset_dir=assets)
    previews = write_previews(slides, os.path.join(os.path.dirname(out) or ".", "example-preview"),
                              asset_dir=assets)
    print("pptx    :", out)
    print("preview :", os.path.dirname(previews[0]), "(%d slides)" % len(previews))
