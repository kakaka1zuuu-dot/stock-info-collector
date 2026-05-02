import os
import sys
import yfinance as yf
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def fetch_stock_info(ticker: str) -> dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    hist = stock.history(period="5d")
    recent_closes = hist["Close"].tolist() if not hist.empty else []

    return {
        "ticker": ticker.upper(),
        "name": info.get("longName", "N/A"),
        "current_price": info.get("currentPrice") or info.get("regularMarketPrice", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
        "dividend_yield": info.get("dividendYield", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "recent_closes": [round(p, 2) for p in recent_closes],
    }


def analyze_with_gemini(stock_data: dict) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません。.env ファイルを確認してください。")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
以下の株式情報を分析して、日本語で簡潔なサマリーを提供してください。

銘柄: {stock_data['ticker']} ({stock_data['name']})
現在価格: {stock_data['current_price']}
時価総額: {stock_data['market_cap']}
PER: {stock_data['pe_ratio']}
52週高値: {stock_data['52w_high']}
52週安値: {stock_data['52w_low']}
配当利回り: {stock_data['dividend_yield']}
セクター: {stock_data['sector']}
業種: {stock_data['industry']}
直近5日間の終値: {stock_data['recent_closes']}

分析内容:
1. 現在の株価水準（52週レンジに対する位置）
2. バリュエーション（PERの評価）
3. 直近のトレンド（終値の推移）
4. 総合的な所見
"""

    response = model.generate_content(prompt)
    return response.text


def main():
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"

    print(f"\n{ticker.upper()} の株式情報を取得中...")
    stock_data = fetch_stock_info(ticker)

    print("\n--- 株式基本情報 ---")
    print(f"銘柄:     {stock_data['ticker']} ({stock_data['name']})")
    print(f"現在価格: {stock_data['current_price']}")
    print(f"時価総額: {stock_data['market_cap']}")
    print(f"PER:      {stock_data['pe_ratio']}")
    print(f"52週高値: {stock_data['52w_high']}")
    print(f"52週安値: {stock_data['52w_low']}")
    print(f"配当利回り: {stock_data['dividend_yield']}")
    print(f"セクター: {stock_data['sector']}")
    print(f"直近5日終値: {stock_data['recent_closes']}")

    print("\nGemini API で分析中...")
    analysis = analyze_with_gemini(stock_data)

    print("\n--- Gemini による分析 ---")
    print(analysis)


if __name__ == "__main__":
    main()
