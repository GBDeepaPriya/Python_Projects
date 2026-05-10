from fastapi import FastAPI
from src.ingest import upsert_daily
from src.indicators import compute_indicators
from src.backtest import run_backtest

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Stock Analyzer API Running"}

@app.post("/refresh/{ticker}")
def refresh(ticker: str):

    upsert_daily(ticker)

    compute_indicators(ticker)

    return {"status": "success"}

@app.get("/backtest/{ticker}")
def backtest(ticker: str):

    result = run_backtest(ticker)

    return result