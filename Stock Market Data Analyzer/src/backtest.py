import pandas as pd
import numpy as np
import sqlite3

DB = "db/market.db"

def run_backtest(ticker):

    con = sqlite3.connect(DB)

    df = pd.read_sql_query("""
    SELECT c.date,c.close,i.sma20,i.sma50
    FROM candles_daily c
    JOIN indicators_daily i
    ON c.ticker=i.ticker
    AND c.date=i.date
    WHERE c.ticker=?
    ORDER BY c.date
    """, con, params=[ticker])

    con.close()

    signal = (df["sma20"] > df["sma50"]).astype(int)

    position = signal.shift(1).fillna(0)

    returns = df["close"].pct_change().fillna(0)

    strategy_returns = position * returns

    equity_curve = (1 + strategy_returns).cumprod()

    sharpe = np.sqrt(252) * (
        strategy_returns.mean() /
        strategy_returns.std()
    )

    max_dd = (
        equity_curve /
        equity_curve.cummax() - 1
    ).min()

    return {
        "Total Return": equity_curve.iloc[-1] - 1,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd
    }