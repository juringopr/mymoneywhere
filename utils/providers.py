
import os
import requests


# Default curated top-10 by market cap (approx):
DEFAULT_TOP10 = [
"AAPL", "MSFT", "NVDA", "GOOGL", "AMZN",
"META", "BRK-B", "TSM", "LLY", "AVGO"
]


FINNHUB_SYMBOLS_URL = "https://finnhub.io/api/v1/stock/symbol"
FINNHUB_METRIC_URL = "https://finnhub.io/api/v1/stock/metric"




def get_top10_tickers(api_key: str | None = None, exchange: str = "US") -> list[str]:
"""Return top-10 tickers by market cap. If api_key is None, return DEFAULT_TOP10.
For Finnhub users, we query a set of large-cap symbols and pick top-10 by "marketCapitalization".
"""
if not api_key:
return DEFAULT_TOP10


try:
# 1) Pull a broad universe (US)
params = {"exchange": exchange, "token": api_key}
r = requests.get(FINNHUB_SYMBOLS_URL, params=params, timeout=15)
r.raise_for_status()
symbols = r.json()


# Filter to common stocks only and limit to ~200 mega/large caps for speed (heuristic: exclude OTC, etc.)
tickers = [s["symbol"] for s in symbols if s.get("type") == "Common Stock" and "." not in s.get("symbol", "")]
tickers = tickers[:200]


# 2) Fetch market cap metric in batches; Finnhub metric per symbol
mktcaps = []
for sym in tickers:
try:
r2 = requests.get(
FINNHUB_METRIC_URL,
params={"symbol": sym, "metric": "price", "token": api_key},
timeout=8,
)
r2.raise_for_status()
data = r2.json()
mc = data.get("metric", {}).get("marketCapitalization")
if mc:
mktcaps.append((sym, float(mc)))
except Exception:
continue


mktcaps.sort(key=lambda x: x[1], reverse=True)
top10 = [t for t, _ in mktcaps[:10]]
return top10 if top10 else DEFAULT_TOP10


except Exception:
return DEFAULT_TOP10
