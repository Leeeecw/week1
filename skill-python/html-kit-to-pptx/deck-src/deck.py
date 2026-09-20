# -*- coding: utf-8 -*-
"""
BOK 경제연구 INSIGHT (2026.7.28) 요약 덱
 — slides-reference-apple.html 의 레이아웃/토큰을 그대로 따른다.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_lib import Slide, render_pptx, render_svg, PAD_X, PAD_Y, SLIDE_W, SLIDE_H

INK = "#1d1d1f"
PRIMARY = "#0066cc"
SKY = "#2997ff"
MUTED = "#7a7a7a"
MUTED80 = "#333333"
HAIR = "#e0e0e0"
HAIR_D = "#3d3d40"
WHITE = "#ffffff"
PARCH = "#f5f5f7"
PEARL = "#fafafc"
TILE = "#272729"
TILE3 = "#252527"
BODYMUTED = "#cccccc"

A = "assets"   # resolved by the caller


def bullets(sl, x, y, w, items, size=20, lh=30, gap=20, color=None, dot=None):
    """items: list of list-of-lines (each line str or run list)"""
    color = color or (WHITE if sl.dark else INK)
    dot = dot or (SKY if sl.dark else PRIMARY)
    cy = y
    for lines in items:
        sl.circle(x + 3.5, cy + size * 0.55, 3.5, dot)
        sl.text(x + 26, cy, w - 26, lines, size, 400, color, lh=lh)
        cy += lh * len(lines) + gap
    return cy


def card(sl, x, y, w, h, title, body_lines, no=None, size=19, dark=False):
    sl.rect(x, y, w, h, TILE if dark else WHITE, 18, HAIR_D if dark else HAIR, 1)
    ty = y + 28
    if no:
        sl.circle(x + 28 + 15, ty + 14, 15, PRIMARY)
        sl.text(x + 28, ty + 5, 30, [no], 13, 600, WHITE, lh=16, align="c")
        ty += 46
    sl.text(x + 28, ty, w - 56, [title], size, 600, WHITE if dark else INK, lh=size * 1.3)
    sl.text(x + 28, ty + size * 1.3 + 12, w - 56, body_lines, 15, 400,
            BODYMUTED if dark else MUTED, lh=23)


def build():
    S = []

    # ---------------------------------------------------------------- 01 표지
    s = Slide(WHITE)
    s.eyebrow("BOK 경제연구 INSIGHT · 2026. 7. 28.")
    s.text(PAD_X, 150, 1000,
           ["AI의 미시적 효과가", "거시적 성장으로 이어지려면?"],
           60, 600, INK, lh=74, spacing=-1.4)
    s.text(PAD_X, 330, 900, ["범용기술(GPT)의 역사에서 찾는 시사점"], 26, 400, MUTED, lh=34)
    s.rect(PAD_X, 552, 120, 3, PRIMARY)
    s.text(PAD_X, 594, 700, ["한국은행 경제연구원 거시경제연구실"], 15, 600, INK, lh=22)
    s.text(PAD_X, 622, 700, ["부연구위원 남충현 · 원문 요약 발표자료"], 15, 400, MUTED, lh=22)
    s.notes = "원문 전체 16쪽을 20장으로 압축한 발표용 요약본입니다."
    S.append(s)

    # ---------------------------------------------------------------- 02 핵심 요약
    s = Slide(PEARL, runner="핵심 요약", page="02")
    s.eyebrow("Key takeaway")
    ry = s.head(["네 문장으로 보는 결론"])
    cw, gap = (1104 - 28) / 2.0, 28
    ch = 186
    top = ry + 34
    card(s, PAD_X, top, cw, ch, "미시적 효과는 이미 확인된다",
         ["고객 문의 처리·코딩 등 개별 업무에서 효율이",
          "즉시 개선됐다. 다만 AI를 적용하기 쉬운 일부",
          "업무에서 관찰된 결과다."], no="01")
    card(s, PAD_X + cw + gap, top, cw, ch, "거시 효과는 적용 범위가 좌우한다",
         ["같은 절감률을 가정해도 그 업무가 GDP에서",
          "차지하는 비중에 따라 전망은 연 0.07%p에서",
          "2.6%p까지 벌어진다."], no="02")
    card(s, PAD_X, top + ch + gap, cw, ch, "과거 범용기술도 늦게 왔다",
         ["증기·전기·정보기술 모두 초기 기여도는 낮았고,",
          "경제 전반으로 확산된 뒤에야 성장에 본격적으로",
          "기여하기 시작했다."], no="03")
    card(s, PAD_X + cw + gap, top + ch + gap, cw, ch, "확산을 막는 한계를 넘어야 한다",
         ["연관 기술의 발전, 업무 프로세스의 재설계,",
          "그리고 생산 현장으로의 확장이 함께 이루어질 때",
          "거시적 효과가 실현된다."], no="04")
    S.append(s)

    # ---------------------------------------------------------------- 03 목차
    s = Slide(PARCH, runner="목차", page="03")
    s.eyebrow("Agenda")
    ry = s.head(["오늘 다루는 것"])
    rows = [("01", "검토배경", "미시 효과와 거시 통계 사이의 간극"),
            ("02", "AI의 생산성 효과와 전망", "업무·기업 수준 실증연구와 기관별 전망치"),
            ("03", "범용기술 확산의 역사", "증기기관·전기·정보기술이 걸린 시간"),
            ("04", "시사점과 결론", "AI가 넘어야 할 기술적·제도적 한계")]
    y = ry + 46
    for no, t, d in rows:
        s.text(PAD_X, y, 60, [no], 21, 600, PRIMARY, lh=28)
        s.text(PAD_X + 74, y - 2, 900, [t], 26, 600, INK, lh=32)
        s.text(PAD_X + 74, y + 34, 900, [d], 16, 400, MUTED, lh=22)
        s.line(PAD_X, y + 70, SLIDE_W - PAD_X, y + 70, HAIR, 1)
        y += 96
    S.append(s)

    # ---------------------------------------------------------------- 04 섹션 1
    s = Slide(TILE, runner="01 · 검토배경", page="04", dark=True)
    s.text(PAD_X, 176, 300, ["01"], 140, 600, "#3a3a3d", lh=140, spacing=-6)
    s.text(PAD_X + 250, 196, 700, ["SECTION"], 14, 600, SKY, lh=16, spacing=1.6)
    s.text(PAD_X + 250, 226, 800, ["검토배경"], 52, 600, WHITE, lh=60, spacing=-1.2)
    s.text(PAD_X, 400, 820,
           ["개별 업무에서는 이미 보이는 효과가,",
            "경제 전체의 생산성 통계에서는 아직 보이지 않는다."],
           26, 400, BODYMUTED, lh=38)
    S.append(s)

    # ---------------------------------------------------------------- 05 미시 → 거시
    s = Slide(WHITE, runner="01 · 검토배경", page="05")
    s.eyebrow("The gap")
    ry = s.head(["미시적 효과는 왜", "곧바로 거시로 가지 않는가"], y=94, lh=52)
    bullets(s, PAD_X, ry + 34, 536, [
        ["Hulten의 정리: 거시적 효과는 해당 부문의",
         "비용절감 효과에 그 부문이 경제에서 차지하는",
         "비중을 곱한 값이다."],
        ["AI를 쓰는 근로자가 효과를 체감하더라도",
         "곧바로 기업 산출 증가로 이어지지 않는다."],
        ["기업 생산성이 올라가도 그것이 GDP 성장의",
         "가속으로 연결된다는 보장은 없다."],
    ], size=20, lh=29, gap=26)
    s.svg("flow-micro-macro.svg", 672, 148, 520, 400)
    S.append(s)

    # ---------------------------------------------------------------- 06 섹션 2
    s = Slide(TILE, runner="02 · 생산성 효과와 전망", page="06", dark=True)
    s.text(PAD_X, 176, 300, ["02"], 140, 600, "#3a3a3d", lh=140, spacing=-6)
    s.text(PAD_X + 250, 196, 700, ["SECTION"], 14, 600, SKY, lh=16, spacing=1.6)
    s.text(PAD_X + 250, 226, 900, ["AI의 생산성 효과와 전망"], 52, 600, WHITE, lh=60, spacing=-1.2)
    s.text(PAD_X, 400, 860,
           ["업무 수준에서는 뚜렷하고, 기업 수준에서는 흐릿하며,",
            "경제 수준에서는 아직 전망뿐이다."],
           26, 400, BODYMUTED, lh=38)
    S.append(s)

    # ---------------------------------------------------------------- 07 task 수준
    s = Slide(WHITE, runner="02 · 생산성 효과와 전망", page="07")
    s.eyebrow("Task level")
    ry = s.head(["업무 수준에서는", "효과가 이미 나타났다"], y=94, lh=52)
    bullets(s, PAD_X, ry + 30, 500, [
        ["고객지원에 AI 에이전트를 도입하자 시간당",
         "문의 해결 건수가 23.9% 증가했고, 그 효과는",
         "도입 3개월째에 정점에 이르렀다."],
        ["국내 취업자 5,512명 설문에서는 업무시간이",
         "약 3.8% 단축되는 데 그쳤다 — 통제된 실험이",
         "아닌 실제 업무환경의 값이다."],
    ], size=19, lh=28, gap=24)
    s.svg("bars-task-gains.svg", 632, 176, 560, 360)
    S.append(s)

    # ---------------------------------------------------------------- 08 기업 수준
    s = Slide(PARCH, runner="02 · 생산성 효과와 전망", page="08")
    s.eyebrow("Firm level")
    ry = s.head(["기업 수준에서는 효과가 일관되게 확인되지 않는다"], y=94, lh=52)
    cw = (1104 - 2 * 24) / 3.0
    top = ry + 56
    ch = 244
    cards = [
        ("간접지표로 본 연구",
         ["AI 인력 채용은 생산성에 유의한 영향이",
          "없었다(Babina 2024). 반면 AI 특허출원은",
          "노동생산성과 양(+)의 상관을 보였다",
          "(Alderucci 2020; Damioli 2021)."],
         "결과가 엇갈림"),
        ("서베이 기반 연구",
         ["AI 도입 기업의 생산성이 더 높게 나왔지만,",
          "통제변수를 넣으면 유의성이 사라졌다",
          "(Acemoglu 2022). OECD 9개국에서도 ICT",
          "역량을 통제하자 계수가 크게 낮아졌다."],
         "통제하면 사라짐"),
        ("국내 연구",
         ["국내 기업의 AI 도입은 노동생산성에",
          "유의한 효과가 없었다(오삼일 외 2025).",
          "도입 이후 최대 6년까지도 유의하지 않았다",
          "(남충현 2026)."],
         "6년까지 유의하지 않음"),
    ]
    for i, (t, lines, verdict) in enumerate(cards):
        x = PAD_X + i * (cw + 24)
        card(s, x, top, cw, ch, t, lines)
        s.line(x + 28, top + ch - 62, x + cw - 28, top + ch - 62, HAIR, 1)
        s.text(x + 28, top + ch - 44, cw - 56, [verdict], 16, 600, PRIMARY, lh=22)
    s.text(PAD_X, top + ch + 40, 1104,
           [[("개인의 업무 효율이 기업의 산출로 합쳐지려면, ", INK, 400),
             ("AI가 적용된 업무가 기업 활동에서 차지하는 비중", PRIMARY, 600),
             ("이 충분히 커야 한다.", INK, 400)]], 20, 400, INK, lh=28)
    S.append(s)

    # ---------------------------------------------------------------- 09 Hulten 분해
    s = Slide(WHITE, runner="02 · 생산성 효과와 전망", page="09")
    s.eyebrow("Decomposition")
    ry = s.head(["같은 절감률, 다른 결론"], y=88, lh=52)
    s.text(PAD_X, ry + 26, 1104,
           ["두 연구 모두 노동비용 절감률을 27~40%로 높게 잡았다. 결과가 18배 갈린 이유는",
            "10년 안에 AI가 실제로 적용될 task의 GDP 비중을 각각 4.6%와 54.4%로 봤기 때문이다."],
           20, 400, MUTED80, lh=30)
    s.svg("hulten-compare.svg", PAD_X, ry + 110, 1104, 330)
    S.append(s)

    # ---------------------------------------------------------------- 10 전망치
    s = Slide(PARCH, runner="02 · 생산성 효과와 전망", page="10")
    s.eyebrow("Forecasts")
    ry = s.head(["기관별 전망은 0.03%p에서 2.6%p까지 흩어져 있다"], y=88, lh=52)
    s.svg("forecast-ranges.svg", PAD_X, ry + 40, 1104, 404)
    s.text(PAD_X, ry + 40 + 404 + 10, 1104,
           ["지표와 대상이 서로 달라 직접 비교는 어렵다. 차이의 대부분은 AI 확산 속도 전망에서 온다."],
           15, 400, MUTED, lh=22)
    S.append(s)

    # ---------------------------------------------------------------- 11 세 가지 변수
    s = Slide(WHITE, runner="02 · 생산성 효과와 전망", page="11")
    s.eyebrow("What drives the spread")
    ry = s.head(["전망을 가르는 세 가지 변수"], y=94, lh=52)
    items = [("01", "업무 간 대체탄력성",
              ["task 사이의 대체성이 낮으면 자동화가 어려운 업무가 '약한 고리'로 남아",
               "전체 생산과정을 제약한다 (Jones 2026; Anthropic 2026)."]),
             ("02", "물리적 업무의 자동화",
              ["지금 적용이 쉬운 일은 사무직·전문직의 인지적 업무에 몰려 있다. 생산직의",
               "물리적 업무까지 확대되면 효과는 더 커진다 (Filippucci et al. 2024)."]),
             ("03", "도입 비용의 하락 속도",
              ["연산 비용이 기하급수적으로 낮아진다는 낙관론과, 전력비·인건비가 남아",
               "절반으로 줄지는 않는다는 반론이 맞선다 (Aghion & Bunel 2025)."])]
    y = ry + 52
    for no, t, lines in items:
        s.rect(PAD_X, y, 1104, 1, HAIR)
        s.circle(PAD_X + 16, y + 40, 16, PRIMARY)
        s.text(PAD_X, y + 31, 32, [no], 13, 600, WHITE, lh=18, align="c")
        s.text(PAD_X + 56, y + 26, 340, [t], 22, 600, INK, lh=30)
        s.text(PAD_X + 430, y + 28, 674, lines, 17, 400, MUTED80, lh=27)
        y += 124
    S.append(s)

    # ---------------------------------------------------------------- 12 섹션 3
    s = Slide(TILE, runner="03 · 범용기술 확산의 역사", page="12", dark=True)
    s.text(PAD_X, 176, 300, ["03"], 140, 600, "#3a3a3d", lh=140, spacing=-6)
    s.text(PAD_X + 250, 196, 700, ["SECTION"], 14, 600, SKY, lh=16, spacing=1.6)
    s.text(PAD_X + 250, 226, 900, ["범용기술 확산의 역사"], 52, 600, WHITE, lh=60, spacing=-1.2)
    s.text(PAD_X, 400, 880,
           ["증기기관도, 전기도, 정보기술도 처음에는 좁은 곳에서만 쓰였다.",
            "성장에 기여하기 시작한 것은 그 다음이었다."],
           26, 400, BODYMUTED, lh=38)
    S.append(s)

    # ---------------------------------------------------------------- 13 기여도 추이
    s = Slide(WHITE, runner="03 · 범용기술 확산의 역사", page="13")
    s.eyebrow("Lagged contribution")
    ry = s.head(["기여도는 20~70년에 걸쳐 뒤늦게 올라왔다"], y=88, lh=52)
    s.svg("gpt-contribution.svg", PAD_X, ry + 44, 1104, 340)
    s.text(PAD_X, ry + 44 + 340 + 22, 1104,
           [[("증기기관은 첫 70년 동안 연 0.014%p에 그쳤다가 다음 40년에 0.30%p로 올라섰고, ", MUTED80, 400)],
            [("정보기술은 1995~2004년에 1.50%p로 정점을 찍은 뒤 다시 낮아졌다.", MUTED80, 400)]],
           18, 400, MUTED80, lh=26)
    S.append(s)

    # ---------------------------------------------------------------- 14 증기
    s = Slide(PARCH, runner="03 · 범용기술 확산의 역사", page="14")
    s.eyebrow("Steam")
    ry = s.head(["탄광 펌프에서", "가장 주된 동력원까지 70년"], y=94, lh=52)
    bullets(s, PAD_X, ry + 30, 520, [
        ["초기 증기기관은 대기압 수준의 저압 증기를",
         "써서 출력과 연료 효율이 낮았고, 탄광 배수",
         "펌프 같은 제한된 용도에만 쓰였다."],
        ["19세기 초 고압 증기기관이 나오면서 공장",
         "기계·기관차·증기선으로 쓰임이 넓어졌고,",
         "그때부터 성장 기여도가 높아졌다."],
    ], size=19, lh=28, gap=24)
    s.svg("uk-steam-share.svg", 660, 200, 520, 330)
    S.append(s)

    # ---------------------------------------------------------------- 15 전기(재조직)
    s = Slide(TILE3, runner="03 · 범용기술 확산의 역사", page="15", dark=True)
    s.eyebrow("Electricity")
    ry = s.head(["기계가 아니라 공장을 다시 설계해야 했다"], y=88, lh=52)
    s.text(PAD_X, ry + 26, 1104,
           ["증기기관 자리에 모터만 바꿔 끼웠을 때는 효율 우위가 분명하지 않았다. 동력축을 걷어내고",
            "기계마다 모터를 달고 나서야 속도 조절과 동선 재배치가 가능해졌다."],
           19, 400, BODYMUTED, lh=28)
    s.svg("shaft-to-unit.svg", PAD_X, ry + 110, 1104, 300)
    s.text(PAD_X, ry + 110 + 300 + 26, 1104,
           [[("전기가 공장의 주된 동력원이 되기까지 ", BODYMUTED, 400),
             ("30년 이상", SKY, 600),
             ("이 걸렸다 (Devine, 1983).", BODYMUTED, 400)]], 18, 400, BODYMUTED, lh=26)
    S.append(s)

    # ---------------------------------------------------------------- 16 전기 확산
    s = Slide(WHITE, runner="03 · 범용기술 확산의 역사", page="16")
    s.eyebrow("Diffusion")
    ry = s.head(["그리고 1919년, 순서가 바뀌었다"], y=94, lh=52)
    bullets(s, PAD_X, ry + 34, 520, [
        ["미국 제조업 동력원에서 전기 비중이 53.1%로",
         "증기(40.7%)를 처음 넘어섰다."],
        ["수력발전소 인근 지역에서는 10년 안에 생산성",
         "효과가 나타났지만, 전국 수준의 생산성 증가로",
         "이어지기까지는 20~30년이 더 걸렸다",
         "(Fiszbein et al., 2020)."],
    ], size=19, lh=28, gap=24)
    s.svg("us-power-mix.svg", 652, 190, 540, 340)
    S.append(s)

    # ---------------------------------------------------------------- 17 정보기술
    s = Slide(PARCH, runner="03 · 범용기술 확산의 역사", page="17")
    s.eyebrow("Information technology")
    ry = s.head(["만든 쪽보다", "쓴 쪽의 기여가 더 컸다"], y=94, lh=52)
    bullets(s, PAD_X, ry + 24, 540, [
        ["IT 자본재 가격이 떨어지며 투자가 급증했다.",
         "수량 기준 1990~95년 연 11.5%, 1995~99년",
         "연 19.4% 증가."],
        ["생산성 기여도 증가분은 IT 생산부문 +0.17%p,",
         "IT 활용부문 +0.83%p로 활용 쪽이 다섯 배",
         "가까이 컸다 (Stiroh, 2002)."],
    ], size=19, lh=28, gap=22)
    s.svg("it-producing-using.svg", 672, 172, 520, 380)
    S.append(s)

    # ---------------------------------------------------------------- 18 시사점
    s = Slide(WHITE, runner="04 · 시사점과 결론", page="18")
    s.eyebrow("Implications")
    ry = s.head(["AI가 넘어야 할 세 가지"], y=88, lh=52)
    s.text(PAD_X, ry + 26, 1104,
           ["지금의 AI는 주로 챗봇 형태로, 사무직·전문직 업무를 중심으로 쓰인다.",
            "역사적으로 범용기술이 성장에 크게 기여한 시기는 생산공정에 본격적으로 쓰이기 시작한 이후였다."],
           19, 400, MUTED80, lh=28)
    s.svg("ai-conditions.svg", PAD_X, ry + 126, 1104, 190)
    s.text(PAD_X, ry + 126 + 190 + 40, 1104,
           [[("여기에 더해, 초기 투자의 불확실성을 덜어 줄 ", MUTED80, 400),
             ("금융기법", PRIMARY, 600),
             ("도 필요하다 — 와트가 절감된 석탄 비용의 일부를", MUTED80, 400)],
            [("나눠 받는 성과연동 계약으로 증기기관을 팔았던 것처럼.", MUTED80, 400)]],
           17, 400, MUTED80, lh=25)
    S.append(s)

    # ---------------------------------------------------------------- 19 결론
    s = Slide(TILE, runner="04 · 시사점과 결론", page="19", dark=True)
    s.eyebrow("Conclusion")
    s.text(PAD_X, 220, 1000,
           [[("혁신이 일부 기업이나 산업에 머무르지 않고", WHITE, 400)],
            [("경제 전반에 걸쳐 확산될 때 비로소", WHITE, 400)],
            [("AI의 거시적 성장효과가 실현된다.", SKY, 400)]],
           40, 400, WHITE, lh=58, spacing=-0.8)
    s.rect(PAD_X, 450, 44, 2, SKY)
    s.text(PAD_X + 60, 442, 800, ["한국은행 경제연구원 거시경제연구실 · 2026. 7. 28."], 15, 400, BODYMUTED, lh=22)
    s.text(PAD_X, 512, 1104,
           ["그 확산은 다양한 연관 기술의 개발과 조직혁신, 그리고 지속적인 유·무형자산 투자로 뒷받침된다."],
           19, 400, BODYMUTED, lh=28)
    S.append(s)

    # ---------------------------------------------------------------- 20 출처
    s = Slide(PEARL, runner="부록", page="20")
    s.eyebrow("Sources")
    ry = s.head(["자료 출처"], y=88, lh=52)
    left = [
        "원문 — 남충현(2026), 「AI의 미시적 효과가 거시적",
        "성장으로 이어지려면? — 범용기술(GPT)의 역사에서",
        "찾는 시사점」, BOK 경제연구 INSIGHT, 한국은행.",
        "",
        "Acemoglu (2024), The Simple Macroeconomics of AI",
        "Aghion & Bunel (2025), AI and Growth: Where Do We Stand?",
        "Brynjolfsson, Li & Raymond (2025), Generative AI at Work",
        "Peng et al. (2023), The Impact of AI on Developer Productivity",
    ]
    right = [
        "Crafts (2004; 2021), Steam / AI as a General Purpose Technology",
        "Devine (1983), From Shafts to Wires",
        "Fiszbein et al. (2020), Powering Up Productivity",
        "Stiroh (2002), Information Technology and the U.S. Productivity Revival",
        "Jorgenson (2001), Information Technology and the U.S. Economy",
        "Jones (2026), A.I. and Our Economic Future",
        "오삼일 외(2025), 「AI와 한국경제」 · 서동현 외(2026)",
    ]
    s.text(PAD_X, ry + 40, 540, left, 16, 400, MUTED80, lh=27)
    s.text(PAD_X + 564, ry + 40, 540, right, 16, 400, MUTED80, lh=27)
    s.line(PAD_X, 560, SLIDE_W - PAD_X, 560, HAIR, 1)
    s.text(PAD_X, 580, 1104,
           ["디자인 — slides-reference-apple.html (Apple design language, Arial). 그래픽은 모두 SVG 벡터로 삽입."],
           14, 400, MUTED, lh=20)
    S.append(s)

    return S


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    assets = os.path.join(root, "deck-assets")
    out = os.path.join(root, "AI-macro-growth-deck.pptx")
    slides = build()
    render_pptx(slides, assets, out)
    print("pptx:", out, len(slides), "slides")

    # QA preview
    import cairosvg
    qa = os.path.join(here, "qa")
    os.makedirs(qa, exist_ok=True)
    for i, sl in enumerate(slides, 1):
        svg = render_svg(sl, assets)
        open(os.path.join(qa, "slide%02d.svg" % i), "w", encoding="utf-8").write(svg)
        cairosvg.svg2png(bytestring=svg.encode("utf-8"),
                         write_to=os.path.join(qa, "slide%02d.png" % i),
                         output_width=1280, output_height=720, background_color="#ffffff")
    print("qa renders:", qa)
