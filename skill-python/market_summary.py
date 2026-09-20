#!/usr/bin/env python3
"""
Yahoo Finance(yfinance)에서 주요 시장 지표를 가져와 표로 정리하는 스크립트.

지표: S&P500, 나스닥, 다우존스, 코스피, 코스닥, 미국채 10년물 금리, 금 가격, 원달러 환율

사용법:
    python3 market_summary.py            # 콘솔에 표 출력
    python3 market_summary.py --csv out.csv   # CSV 파일로도 저장
"""

import argparse
import sys
import warnings
from datetime import datetime

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")

# 이름, 야후 티커, 단위
INDICATORS = [
    ("S&P500",          "^GSPC",     "pt"),
    ("나스닥",           "^IXIC",     "pt"),
    ("다우존스",         "^DJI",      "pt"),
    ("코스피",           "^KS11",     "pt"),
    ("코스닥",           "^KQ11",     "pt"),
    ("미국채 10년물 금리", "^TNX",      "%"),
    ("금 가격",          "GC=F",      "USD/oz"),
    ("원달러 환율",       "KRW=X",     "KRW/USD"),
]


def fetch_indicator(name: str, ticker: str, unit: str) -> dict:
    """최근 거래일 종가와 전일 대비 변동을 가져온다."""
    row = {"지표": name, "티커": ticker, "단위": unit,
           "기준일": None, "현재값": None, "전일값": None, "변동": None, "변동률(%)": None}
    try:
        hist = yf.Ticker(ticker).history(period="10d", auto_adjust=False)
        hist = hist.dropna(subset=["Close"])
        if hist.empty:
            row["비고"] = "데이터 없음"
            return row
        last = hist.iloc[-1]
        row["기준일"] = hist.index[-1].strftime("%Y-%m-%d")
        row["현재값"] = float(last["Close"])
        if len(hist) >= 2:
            prev = float(hist.iloc[-2]["Close"])
            row["전일값"] = prev
            row["변동"] = row["현재값"] - prev
            row["변동률(%)"] = (row["현재값"] / prev - 1) * 100
        row["비고"] = ""
    except Exception as e:  # 네트워크 오류 등
        row["비고"] = f"오류: {e}"
    return row


def build_table() -> pd.DataFrame:
    rows = [fetch_indicator(*item) for item in INDICATORS]
    return pd.DataFrame(rows)


def format_for_display(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in ("현재값", "전일값"):
        out[col] = out[col].map(lambda v: f"{v:,.2f}" if pd.notna(v) else "-")
    out["변동"] = out["변동"].map(lambda v: f"{v:+,.2f}" if pd.notna(v) else "-")
    out["변동률(%)"] = out["변동률(%)"].map(lambda v: f"{v:+.2f}%" if pd.notna(v) else "-")
    out["기준일"] = out["기준일"].fillna("-")
    return out


def main():
    parser = argparse.ArgumentParser(description="주요 시장 지표 요약")
    parser.add_argument("--csv", metavar="PATH", help="결과를 CSV 파일로 저장")
    args = parser.parse_args()

    df = build_table()

    print(f"\n주요 시장 지표 요약  (조회 시각: {datetime.now():%Y-%m-%d %H:%M:%S})\n")
    display = format_for_display(df)
    with pd.option_context("display.unicode.east_asian_width", True,
                           "display.width", 200, "display.max_columns", None):
        print(display.to_string(index=False))

    if args.csv:
        df.to_csv(args.csv, index=False, encoding="utf-8-sig")
        print(f"\nCSV 저장: {args.csv}")

    if (df["비고"] != "").any():
        print("\n일부 지표를 가져오지 못했습니다. '비고' 열을 확인하세요.", file=sys.stderr)


if __name__ == "__main__":
    main()
