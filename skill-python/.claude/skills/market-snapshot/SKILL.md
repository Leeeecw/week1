---
name: market-snapshot
description: 현재 시장 스냅샷 확인. S&P500, 나스닥, 다우존스, 코스피, 코스닥, 미국채 10년물 금리, 금 가격, 원달러 환율을 Yahoo Finance에서 가져와 표로 정리한다. "시장 상황", "마켓 스냅샷", "지수 확인", "환율/금리/금값 알려줘" 같은 요청에 사용.
---

# Market Snapshot

Yahoo Finance(yfinance)에서 주요 시장 지표 8개를 가져와 전일 대비 변동과 함께 표로 보여주는 스킬.

## 실행 절차

1. 의존성 확인. 없으면 설치한다.
   ```bash
   python3 -c "import yfinance, pandas" 2>/dev/null || python3 -m pip install --quiet yfinance pandas
   ```
2. 스크립트 실행. 이 SKILL.md와 같은 디렉토리의 `scripts/market_summary.py`를 사용한다.
   ```bash
   python3 .claude/skills/market-snapshot/scripts/market_summary.py 2>/dev/null
   ```
   CSV 저장이 필요하면 `--csv <경로>` 옵션을 붙인다.
3. 출력된 표를 사용자에게 그대로 전달하고, 아래 요약 규칙에 따라 2~4문장의 코멘트를 덧붙인다.

## 요약 규칙

- 미국 지수 3개, 한국 지수 2개, 금리/금/환율을 묶어서 방향(상승/하락)과 변동률을 짧게 언급한다.
- 변동률 절대값이 1% 이상인 지표는 반드시 따로 언급한다.
- 미국 지표와 한국 지표는 기준일이 다를 수 있다. 표의 `기준일` 열이 서로 다르면 그 사실을 한 줄로 알린다.
- `비고` 열에 오류가 있으면 해당 지표를 가져오지 못했다고 명시하고, 나머지 지표만 요약한다.
- 투자 조언이나 전망은 하지 않는다. 데이터 설명에만 집중한다.

## 지표와 티커

| 지표 | 티커 | 단위 |
|---|---|---|
| S&P500 | ^GSPC | pt |
| 나스닥 | ^IXIC | pt |
| 다우존스 | ^DJI | pt |
| 코스피 | ^KS11 | pt |
| 코스닥 | ^KQ11 | pt |
| 미국채 10년물 금리 | ^TNX | % |
| 금 가격 | GC=F | USD/oz |
| 원달러 환율 | KRW=X | KRW/USD |

## 문제 해결

- `ModuleNotFoundError`: 1단계 설치 명령을 다시 실행한다.
- 특정 지표만 `데이터 없음`: Yahoo 쪽 일시 장애인 경우가 많다. 한 번 재실행하고, 그래도 안 되면 그대로 보고한다.
- stderr의 `NotOpenSSLWarning`은 무해하므로 무시한다.
