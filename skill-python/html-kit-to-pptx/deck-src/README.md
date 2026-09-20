# deck-src — PPTX 생성 스크립트

`refer.pdf`(BOK 경제연구 INSIGHT, 2026.7.28) 내용을
[slides-reference-apple.html](../slides-reference-apple.html)의 레이아웃·토큰으로 옮겨
`AI-macro-growth-deck.pptx`를 만드는 스크립트입니다.

## 구성

| 파일 | 역할 |
|---|---|
| `charts.py` | 차트·다이어그램 10종을 SVG 문자열로 생성 |
| `render_charts.py` | 위 SVG를 `../deck-assets/*.svg`로 저장 (+ `_preview/`에 PNG 미리보기) |
| `deck_lib.py` | 슬라이드 모델과 두 개의 렌더러 — python-pptx용, QA 프리뷰(SVG/PNG)용 |
| `deck.py` | 20장의 슬라이드 내용 정의. 실행하면 PPTX와 `qa/` 프리뷰를 함께 생성 |

## 재생성

```bash
cd ~/projects/week1
./.venv/bin/pip install python-pptx cairosvg      # 최초 1회
./.venv/bin/python skill-python/html-kit-to-pptx/deck-src/render_charts.py   # SVG 갱신
./.venv/bin/python skill-python/html-kit-to-pptx/deck-src/deck.py            # PPTX + QA 프리뷰
```

## 설계 메모

- **좌표계**: 레퍼런스 킷과 동일한 1280 × 720 px. `deck_lib.E()`가 px를 EMU로 환산한다
  (1 px = 9525 EMU). 슬라이드 크기는 13.333 × 7.5 in.
- **폰트**: 라틴 `Arial`, 한글 `Malgun Gothic`(Arial에 한글 글리프가 없어 `<a:ea>`로 지정).
  본문 20 px = 15 pt, 제목 44 px = 33 pt.
- **줄바꿈**: 모든 텍스트는 코드에서 손으로 줄을 나누고 PowerPoint 텍스트 상자의
  자동 줄바꿈을 꺼 둔다. 그래서 QA 프리뷰와 실제 PPTX의 줄 끊김이 정확히 일치한다.
- **SVG 삽입**: `deck_lib._add_svg_picture()`가 PNG 폴백을 먼저 넣고
  `a:blip`에 `asvg:svgBlip` 확장을 달아 원본 SVG를 함께 패키징한다.
  PowerPoint 2016 이상은 벡터 SVG를, 구형 뷰어는 PNG를 렌더링한다.
- **QA**: 이 환경에는 LibreOffice가 없어 PPTX를 직접 렌더링할 수 없다.
  대신 같은 좌표 모델에서 `render_svg()`로 슬라이드 프리뷰를 만들어 겹침·넘침을 검수했다.
  프리뷰는 `qa/slideNN.png`에 남아 있다.
