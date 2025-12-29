from __future__ import annotations
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta




def _gen_schedule(n_periods: int, freq: str, end_date: pd.Timestamp | None = None) -> list[pd.Timestamp]:
"""Generate schedule of N dates ending at (or before) today.
freq: 'D' (business days), 'W' (Fridays), 'M' (month-ends)
"""
if end_date is None:
end_date = pd.Timestamp.today().normalize()


if freq == 'D':
# last n business days up to today
cal = pd.bdate_range(end=end_date, periods=n_periods)
return list(cal)
elif freq == 'W':
# last n Fridays up to today
weeks = pd.date_range(end=end_date, periods=n_periods*7, freq='D')
fridays = weeks[weeks.weekday == 4]
fridays = fridays[-n_periods:]
if len(fridays) < n_periods: # fallback
fridays = pd.date_range(end=end_date, periods=n_periods, freq='W-FRI')
return list(fridays)
elif freq == 'M':
months = pd.date_range(end=end_date, periods=n_periods, freq='M')
return list(months)
else:
raise ValueError("freq must be 'D', 'W', or 'M'")




def _nearest_prev_date(idx: pd.DatetimeIndex, date: pd.Timestamp) -> pd.Timestamp | None:
"""Return the nearest previous index date <= date, or None if none."""
pos = idx.searchsorted(date, side='right') - 1
if pos >= 0:
return idx[pos]
return None




def run_backtest(tickers: list[str], total_amount: float, freq: str, n_periods: int) -> dict:
"""DCA across tickers using close prices on scheduled dates.
Fractional shares allowed. Equal split across tickers and periods.
Returns dict with summary, table (HTML), and plotly JSON.
"""
# Build schedule and download prices
schedule = _gen_schedule(n_periods=n_periods, freq=freq)
start = schedule[0] - pd.Timedelta(days=7)
end = pd.Timestamp.today() + pd.Timedelta(days=1)


data = yf.download(tickers, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))['Close']
if isinstance(data, pd.Series): # single ticker edge
data = data.to_frame()
data = data.ffill().dropna(how='all')


# Per-period per-ticker allocation
alloc = total_amount / (len(schedule) * len(tickers))


# Track holdings
shares = {t: 0.0 for t in tickers}
cashflow_rows = []
portfolio_values = []


for d in schedule:
# actual trading date = nearest previous trading day with data
}
