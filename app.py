from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.providers import get_top10_tickers
from utils.backtest import run_backtest
import os


app = FastAPI(title="DCA Backtest")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/backtest", response_class=HTMLResponse)
async def backtest(
request: Request,
total_amount: float = Form(...),
freq: str = Form(...), # 'D','W','M'
n_periods: int = Form(...),
use_live_top10: bool = Form(False)
):
api_key = os.getenv("FINNHUB_API_KEY") if use_live_top10 else None
tickers = get_top10_tickers(api_key=api_key)


result = run_backtest(
tickers=tickers,
total_amount=total_amount,
freq=freq,
n_periods=n_periods,
)


return templates.TemplateResponse("index.html", {"request": request, "result": result})
