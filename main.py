import os
import sys
from google import genai
from dotenv import load_dotenv

load_dotenv()


def analyze_stock_with_gemini(ticker: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません。.env ファイルを確認してください。")

    client = genai.Client(api_key=api_key)

    prompt = f"""
株式ティッカー「{ticker.upper()}」について、以下の項目を含む詳細な分析を日本語で提供してください。

1. 企業概要（社名・セクター・主要事業）
2. 現在の株価水準と最近のトレンド
3. バリュエーション（PER・時価総額など）
4. 52週の高値・安値と現在地
5. 主要リスクと注目ポイント
6. 総合的な所見

※ 情報はあなたの学習データに基づくものであり、リアルタイムではありません。投資判断の参考として使用してください。
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text


def main():
    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"

    print(f"\n{ticker.upper()} の株式分析を Gemini に依頼中...\n")
    analysis = analyze_stock_with_gemini(ticker)

    print("=" * 60)
    print(f"  {ticker.upper()} 株式分析レポート (Powered by Gemini)")
    print("=" * 60)
    print(analysis)
    print("=" * 60)
    print("※ 本情報は投資アドバイスではありません。")


if __name__ == "__main__":
    main()
