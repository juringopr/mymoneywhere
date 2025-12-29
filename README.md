## README.md
```markdown
# DCA Backtest Webapp


Enter a total amount (the money you could have saved), choose D/W/M and N periods, and backtest dollar-cost-averaging into Top‑10 megacap stocks using close prices.


## Features
- ✅ Input: total investable amount, frequency (day/week/month), number of periods
- ✅ Universe: Top‑10 market cap US megacaps (static default), optional **live Finnhub** ranking if you set an API key
- ✅ Prices: yfinance daily close
- ✅ Fractional shares for accurate math
- ✅ Plotly interactive portfolio‑value chart


## Deploy to Render
1. Push this repo to GitHub.
2. On Render, **New > Web Service** → Connect repo.
3. Set **Runtime**: Python 3.x
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. (Optional) Set env var `FINNHUB_API_KEY` for live market‑cap ranking.


## Local run
```bash
python -m venv .venv && source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload
```


## Notes
- If `FINNHUB_API_KEY` is not set, the app uses a curated static Top‑10 list close to current rankings:
`['AAPL','MSFT','NVDA','GOOGL','AMZN','META','BRK-B','TSM','LLY','AVGO']`
- You can switch region/universe logic in `utils/providers.py`.
