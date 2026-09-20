# -*- coding: utf-8 -*-
"""
AI 개요 덱 (10장) — html-kit-to-pptx 스킬 워크플로로 생성.
레퍼런스 킷: skill-python/html-kit-to-pptx/slides-reference-apple.html
"""
import os
import sys

SKILL = os.path.expanduser("~/projects/week1/.claude/skills/html-kit-to-pptx/scripts")
sys.path.insert(0, SKILL)

import svgkit as sk
from svgkit import T, R, L, C, path, arrow_marker, svg
from deckkit import Slide, Theme, render_pptx, write_previews

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

# ---------------------------------------------------------------- 1. 테마 (킷에서 추출)
THEME = Theme(
    width=1280, height=720, pad_x=88, pad_y=64, runner_h=56,
    latin_font="Arial", ea_font="Malgun Gothic",
    colors={"accent": "#0066cc", "accent_on_dark": "#2997ff", "ink": "#1d1d1f",
            "muted": "#7a7a7a", "hairline": "#e0e0e0"},
)
INK, ACCENT, SKY = "#1d1d1f", "#0066cc", "#2997ff"
MUTED, MUTED80, HAIR = "#7a7a7a", "#333333", "#e0e0e0"
WHITE, PARCH, PEARL, TILE, TILE3 = "#ffffff", "#f5f5f7", "#fafafc", "#272729", "#252527"
ON_DARK, BODYMUTED = "#ffffff", "#cccccc"
PAD = THEME.pad_x


# ---------------------------------------------------------------- 2. 그래픽 (SVG)
def svg_timeline(w=1104, h=230):
    """규칙 기반 → 통계적 학습 → 딥러닝 → 생성형·에이전트"""
    steps = [
        ("~1990년대", "규칙 기반", ["사람이 규칙을 직접 작성.", "규칙 밖의 상황은 처리 불가."]),
        ("2000년대", "통계적 학습", ["데이터에서 패턴을 학습.", "특징은 여전히 사람이 설계."]),
        ("2010년대", "딥러닝", ["특징 설계까지 학습이 대체.", "이미지·음성 인식이 실용화."]),
        ("2020년대", "생성형 · 에이전트", ["언어로 지시하고 결과를 생성.", "도구를 쓰고 작업을 수행."]),
    ]
    b = []
    cw = (w - 3 * 24) / 4.0
    line_y = 46
    b.append(L(0, line_y, w, line_y, HAIR, 2))
    for i, (era, title, lines) in enumerate(steps):
        x = i * (cw + 24)
        last = i == len(steps) - 1
        color = ACCENT if last else sk.P.series_gray
        b.append(C(x + 18, line_y, 9, color, "#ffffff", 3))
        b.append(T(x, 24, era, 13, 400, MUTED))
        b.append(T(x, line_y + 42, title, 21, 600, ACCENT if last else INK))
        for j, ln in enumerate(lines):
            b.append(T(x, line_y + 74 + j * 23, ln, 14, 400, MUTED))
        if last:
            b.append(R(x, line_y + 128, cw - 20, 3, ACCENT))
            b.append(T(x, line_y + 158, "지금 여기", 14, 600, ACCENT))
    return svg(w, h, "".join(b))


def svg_pipeline(w=1104, h=300):
    """LLM이 답을 만드는 경로 — 확률적 산출이라는 점을 드러낸다."""
    b = [arrow_marker(sk.P.muted, "pipe")]
    boxes = [
        ("입력", ["질문 + 맥락", "(문서 · 데이터)"]),
        ("토큰화", ["글자를 조각으로", "나누어 숫자로"]),
        ("모델", ["다음 조각의", "확률을 예측"]),
        ("출력", ["가장 그럴듯한", "문장을 생성"]),
        ("검증", ["사람 또는 도구가", "결과를 확인"]),
    ]
    bw, gap, top, bh = 184, 46, 40, 132
    for i, (title, lines) in enumerate(boxes):
        x = i * (bw + gap)
        accent_box = i in (2, 4)
        b.append(R(x, top, bw, bh, WHITE, 18, ACCENT if accent_box else HAIR,
                   2 if accent_box else 1))
        b.append(T(x + 24, top + 40, title, 19, 600, ACCENT if accent_box else INK))
        for j, ln in enumerate(lines):
            b.append(T(x + 24, top + 68 + j * 22, ln, 14, 400, MUTED))
        if i < len(boxes) - 1:
            ax = x + bw + 10
            b.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                     'stroke-width="2" marker-end="url(#pipe)"/>'
                     % (ax, top + bh / 2, ax + gap - 22, top + bh / 2, sk.P.muted))
    # 확률적 산출을 아래에 명시 (왼쪽 정렬해 슬라이드 본문 기준선과 맞춘다)
    y = top + bh + 44
    b.append(R(0, y, 56, 3, ACCENT))
    b.append(T(0, y + 34, "같은 질문에도 매번 같은 답이 나오지 않는다.", 18, 600, INK))
    b.append(T(0, y + 62,
               "정해진 규칙이 아니라 확률에 따라 문장을 고르기 때문 — 그래서 마지막 검증 단계가 선택이 아니라 필수다.",
               15, 400, MUTED))
    return svg(w, h, "".join(b))


def svg_task_gains(w=560, h=364):
    return sk.bars_h(w, h, [
        ("코딩 속도", "Peng et al. (2023)", 55.8, sk.P.accent),
        ("글쓰기 과제", "Noy & Zhang (2023)", 40.0, sk.P.accent),
        ("고객상담 처리량", "Brynjolfsson et al. (2025)", 23.9, sk.P.accent),
        ("업무시간 단축", "서동현 외 (2026), 설문", 3.8, sk.P.series_gray),
    ], vmax=60, label_w=178, top=54, bar_h=32, gap=40,
        note="통제된 실험(파랑)과 실제 업무환경 설문(회색)은 성격이 다른 수치다.")


def svg_roadmap(w=1104, h=290):
    """도입 4단계 — 화살표 대신 번호 배지 + 상단 라인으로 방향을 암시."""
    steps = [
        ("업무 선정", ["성과를 숫자로 잴 수 있고", "틀렸을 때 확인이 가능한 업무부터."]),
        ("파일럿 · 측정", ["도입 전후를 같은 지표로 비교.", "체감이 아니라 데이터로 판단한다."]),
        ("프로세스 재설계", ["사람이 검토하는 지점을 새로 설계.", "도구만 바꾸면 효과는 작다."]),
        ("확산 · 역량", ["성공 사례를 다른 팀으로.", "교육과 가이드라인을 함께."]),
    ]
    b = []
    cw = (w - 3 * 28) / 4.0
    for i, (title, lines) in enumerate(steps):
        x = i * (cw + 28)
        b.append(R(x, 0, cw, 3, ACCENT))
        b.append(C(x + 18, 46, 18, ACCENT))
        b.append(T(x + 18, 52, "%d" % (i + 1), 15, 600, WHITE, "middle"))
        b.append(T(x, 108, title, 20, 600, INK))
        for j, ln in enumerate(lines):
            b.append(T(x, 142 + j * 24, ln, 15, 400, MUTED))
    b.append(L(0, h - 44, w, h - 44, HAIR, 1))
    b.append(T(0, h - 16, "앞의 두 단계를 건너뛰면 세 번째 단계에서 근거가 없어 멈추게 된다.", 15, 400, MUTED80))
    return svg(w, h, "".join(b))


GRAPHICS = {
    "timeline.svg": svg_timeline,
    "pipeline.svg": svg_pipeline,
    "task-gains.svg": svg_task_gains,
    "roadmap.svg": svg_roadmap,
}


# ---------------------------------------------------------------- 3. 슬라이드
def build():
    S = []

    # 01 표지 -------------------------------------------------------
    s = Slide(THEME, WHITE)
    s.eyebrow("AI briefing · 2026")
    s.text(PAD, 190, 1000, ["AI, 무엇이 달라졌고", "무엇을 준비해야 하나"],
           60, 600, INK, lh=74, spacing=-1.4)
    s.text(PAD, 350, 900, ["기술의 변화, 실제 효과, 그리고 도입의 순서"], 26, 400, MUTED, lh=34)
    s.rect(PAD, 552, 120, 3, ACCENT)
    s.text(PAD, 594, 700, ["일반 비즈니스 청중용 개요 · 10장"], 15, 600, INK, lh=22)
    s.text(PAD, 622, 700, ["수치는 공개된 실증연구에서 인용 (10장 출처 참조)"], 15, 400, MUTED, lh=22)
    s.notes = "10분 발표 기준. 4·5장에서 원리, 6장에서 근거, 8·9장에서 실행을 다룬다."
    S.append(s)

    # 02 아젠다 -----------------------------------------------------
    s = Slide(THEME, PARCH, runner="개요", page="02")
    s.eyebrow("Agenda")
    ry = s.head(["오늘 다루는 것"])
    rows = [("01", "무엇이 달라졌나", "규칙을 쓰던 시대에서 생성하는 시대로"),
            ("02", "실제로 무엇을 하나", "업무 단위에서 확인된 효과와 그 한계"),
            ("03", "무엇을 조심해야 하나", "잘하는 일과 아직 못 미더운 일"),
            ("04", "어떻게 도입하나", "네 단계로 나눈 현실적인 순서")]
    y = ry + 46
    for no, t, d in rows:
        s.text(PAD, y, 60, [no], 21, 600, ACCENT, lh=28)
        s.text(PAD + 74, y - 2, 900, [t], 26, 600, INK, lh=32)
        s.text(PAD + 74, y + 34, 900, [d], 16, 400, MUTED, lh=22)
        s.line(PAD, y + 70, THEME.width - PAD, y + 70, HAIR, 1)
        y += 96
    S.append(s)

    # 03 섹션 구분 ---------------------------------------------------
    s = Slide(THEME, TILE, runner="01 · 무엇이 달라졌나", page="03", dark=True)
    s.text(PAD, 176, 300, ["01"], 140, 600, "#3a3a3d", lh=140, spacing=-6)
    s.text(PAD + 250, 196, 700, ["SECTION"], 14, 600, SKY, lh=16, spacing=1.6)
    s.text(PAD + 250, 226, 900, ["무엇이 달라졌나"], 52, 600, ON_DARK, lh=60, spacing=-1.2)
    s.text(PAD, 400, 880,
           ["오래된 기술이 갑자기 유용해진 것이 아니라,",
            "지시하는 방법과 만들어 내는 범위가 달라졌다."],
           26, 400, BODYMUTED, lh=38)
    S.append(s)

    # 04 타임라인 ---------------------------------------------------
    s = Slide(THEME, WHITE, runner="01 · 무엇이 달라졌나", page="04")
    s.eyebrow("What changed")
    ry = s.head(["규칙을 쓰던 시대에서 생성하는 시대로"], y=88, lh=52)
    s.text(PAD, ry + 26, 1104,
           ["세 번의 전환이 있었다. 사람이 규칙을 쓰던 시대, 데이터에서 패턴을 학습하던 시대,",
            "그리고 언어로 지시하면 결과물 자체를 만들어 내는 지금이다."],
           20, 400, MUTED80, lh=30)
    s.svg("timeline.svg", PAD, ry + 118, 1104, 230)
    s.text(PAD, ry + 118 + 230 + 26, 1104,
           [[("달라진 것은 정확도만이 아니라 ", MUTED80, 400),
             ("쓰는 방법", ACCENT, 600),
             ("이다. 전문가가 모델을 설계하던 일을, 이제는 누구나 문장으로 지시한다.", MUTED80, 400)]],
           18, 400, MUTED80, lh=26)
    S.append(s)

    # 05 동작 방식 ---------------------------------------------------
    s = Slide(THEME, PARCH, runner="01 · 무엇이 달라졌나", page="05")
    s.eyebrow("How it works")
    ry = s.head(["답을 아는 것이 아니라, 그럴듯한 말을 고른다"], y=88, lh=52)
    s.svg("pipeline.svg", PAD, ry + 46, 1104, 300)
    s.text(PAD, ry + 46 + 300 + 34, 1104,
           ["이 구조를 이해하면 왜 자신 있게 틀린 답을 내놓는지, 왜 검증 절차가 업무 설계의 일부여야 하는지가 설명된다."],
           18, 400, MUTED80, lh=26)
    S.append(s)

    # 06 효과 -------------------------------------------------------
    s = Slide(THEME, WHITE, runner="02 · 어디에 쓰이나", page="06")
    s.eyebrow("Evidence")
    ry = s.head(["업무 단위에서는", "효과가 확인됐다"], y=94, lh=52)
    s.bullets(PAD, ry + 30, 500, [
        ["코딩, 글쓰기, 고객상담처럼 결과를 바로",
         "확인할 수 있는 업무에서 효율이 크게",
         "개선됐다."],
        ["다만 실제 업무환경을 설문한 결과는",
         "훨씬 작았다. 적용하기 쉬운 업무에",
         "한정된 효과라는 뜻이다."],
    ], size=19, lh=28, gap=24)
    s.svg("task-gains.svg", 632, 176, 560, 364)
    S.append(s)

    # 07 도입 형태 ---------------------------------------------------
    s = Slide(THEME, PEARL, runner="02 · 어디에 쓰이나", page="07")
    s.eyebrow("Three modes")
    ry = s.head(["쓰는 방식은 세 가지로 나뉜다"], y=94, lh=52)
    cw, gap = (1104 - 2 * 24) / 3.0, 24
    top = ry + 76
    ch = 252
    modes = [
        ("보조", "사람이 하고, AI가 돕는다",
         ["초안 작성, 요약, 번역, 코드 자동완성.",
          "결과를 사람이 그대로 검토하므로",
          "위험이 가장 낮고 도입도 가장 빠르다."], "지금 대부분의 조직"),
        ("자동화", "정해진 절차를 맡긴다",
         ["문서 분류, 1차 응대, 데이터 정리.",
          "예외 처리와 품질 기준을 먼저",
          "정의해 두어야 작동한다."], "파일럿 단계"),
        ("에이전트", "도구를 쓰며 작업을 수행한다",
         ["검색·실행·수정을 스스로 반복.",
          "권한 범위와 되돌리기 방법을",
          "설계하는 일이 핵심이 된다."], "초기 실험 단계"),
    ]
    for i, (name, sub, lines, stage) in enumerate(modes):
        x = PAD + i * (cw + gap)
        s.rect(x, top, cw, ch, WHITE, 18, HAIR, 1)
        s.text(x + 28, top + 34, cw - 56, [name], 24, 600, INK, lh=30)
        s.text(x + 28, top + 70, cw - 56, [sub], 15, 600, ACCENT, lh=22)
        s.text(x + 28, top + 104, cw - 56, lines, 15, 400, MUTED, lh=23)
        s.line(x + 28, top + ch - 56, x + cw - 28, top + ch - 56, HAIR, 1)
        s.text(x + 28, top + ch - 38, cw - 56, [stage], 14, 600, MUTED80, lh=20)
    s.text(PAD, top + ch + 44, 1104,
           [[("오른쪽으로 갈수록 효과는 커지지만, ", MUTED80, 400),
             ("틀렸을 때 되돌리는 비용도 함께 커진다", ACCENT, 600),
             (". 순서대로 넘어가는 편이 안전하다.", MUTED80, 400)]],
           18, 400, MUTED80, lh=26)
    S.append(s)

    # 08 한계 -------------------------------------------------------
    s = Slide(THEME, WHITE, runner="03 · 무엇을 조심해야 하나", page="08")
    # 좌우 면 전환으로 대비 (킷의 comparison 아키타입)
    s.rect(0, 0, 640, THEME.height - THEME.runner_h, WHITE)
    s.rect(640, 0, 640, THEME.height - THEME.runner_h, TILE)
    RX = 640 + PAD          # 오른쪽 면도 같은 88px 여백을 쓴다
    COL = 640 - 2 * PAD     # 464
    s.text(PAD, 108, COL, ["JUST WORKS"], 14, 600, MUTED, lh=16, spacing=1.6)
    s.text(PAD, 142, COL, ["잘하는 일"], 30, 600, INK, lh=38, spacing=-0.6)
    s.bullets(PAD, 216, COL, [
        ["형식이 정해진 글을 빠르게 초안화"],
        ["긴 문서에서 필요한 부분 찾아 정리"],
        ["코드 작성과 오류 설명"],
        ["번역, 말투 변환, 분류"],
    ], size=18, lh=26, gap=20)
    s.line(PAD, 508, PAD + COL, 508, HAIR, 1)
    s.text(PAD, 530, COL, ["공통점 — 결과가 맞는지 사람이", "곧바로 확인할 수 있다."],
           16, 400, MUTED, lh=24)

    s.text(RX, 108, COL, ["NOT YET"], 14, 600, SKY, lh=16, spacing=1.6)
    s.text(RX, 142, COL, ["아직 못 미더운 일"], 30, 600, ON_DARK, lh=38, spacing=-0.6)
    s.bullets(RX, 216, COL, [
        ["출처가 필요한 사실 확인 — 그럴듯한", "오답을 자신 있게 내놓는다"],
        ["최신 정보나 사내 데이터 — 알려준", "범위 밖은 알지 못한다"],
        ["책임이 따르는 최종 판단"],
        ["민감 정보 처리 — 무엇을 보내는지", "먼저 정해야 한다"],
    ], size=18, lh=26, gap=16, color=BODYMUTED, dot=SKY)
    s.line(RX, 508, RX + COL, 508, "#3d3d40", 1)
    s.text(RX, 530, COL, ["공통점 — 틀렸을 때 확인 비용이", "크고, 확인 자체가 어렵다."],
           16, 400, BODYMUTED, lh=24)
    S.append(s)

    # 09 로드맵 -----------------------------------------------------
    s = Slide(THEME, PARCH, runner="04 · 어떻게 도입하나", page="09")
    s.eyebrow("Roadmap")
    ry = s.head(["네 단계로 나누어 시작한다"], y=88, lh=52)
    s.text(PAD, ry + 26, 1104,
           ["도구를 먼저 사는 것이 아니라 업무를 먼저 고른다. 효과를 잴 수 없는 업무에서 시작하면",
            "도입이 성공했는지 아무도 답하지 못한다."],
           20, 400, MUTED80, lh=30)
    s.svg("roadmap.svg", PAD, ry + 140, 1104, 290)
    S.append(s)

    # 10 결론 + 출처 -------------------------------------------------
    s = Slide(THEME, TILE3, runner="맺음", page="10", dark=True)
    s.eyebrow("In one line")
    s.text(PAD, 180, 1020,
           [[("도구를 도입하는 일이 아니라,", ON_DARK, 400)],
            [("일하는 방식을 다시 설계하는 일이다.", SKY, 400)]],
           40, 400, ON_DARK, lh=58, spacing=-0.8)
    s.bullets(PAD, 330, 900, [
        ["확인 가능한 업무부터 고른다 — 효과를 숫자로 말할 수 있어야 한다."],
        ["검증 단계를 업무 절차에 넣는다 — 확률적 산출이라는 성질은 사라지지 않는다."],
        ["사람의 역할을 다시 정의한다 — 도구만 바꾸면 효과는 작다."],
    ], size=19, lh=28, gap=16, color=BODYMUTED, dot=SKY)
    s.line(PAD, 556, THEME.width - PAD, 556, "#3d3d40", 1)
    s.text(PAD, 578, 1104,
           ["출처 — Peng et al.(2023) · Noy & Zhang(2023) · Brynjolfsson, Li & Raymond(2025) ·",
            "서동현 외(2026), 한국은행 BOK 이슈노트. 디자인 — slides-reference-apple.html (Arial)."],
           14, 400, BODYMUTED, lh=21)
    S.append(s)

    return S


if __name__ == "__main__":
    os.makedirs(ASSETS, exist_ok=True)
    for name, fn in GRAPHICS.items():
        open(os.path.join(ASSETS, name), "w", encoding="utf-8").write(fn())
    print("graphics:", len(GRAPHICS))

    slides = build()
    out = os.path.join(HERE, "AI-overview-deck.pptx")
    render_pptx(slides, out, asset_dir=ASSETS)
    write_previews(slides, os.path.join(HERE, "preview"), asset_dir=ASSETS)
    print("pptx:", out, len(slides), "slides")
