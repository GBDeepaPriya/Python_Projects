import pandas as pd
import sqlite3

from ta.trend import SMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

DB = "db/market.db"

def compute_indicators(ticker):

    con = sqlite3.connect(DB)

    df = pd.read_sql_query(
        """
        SELECT date, close
        FROM candles_daily
        WHERE ticker=?
        ORDER BY date
        """,
        con,
        params=[ticker]
    )

    s = df["close"]

    sma20 = SMAIndicator(s, window=20).sma_indicator()
    sma50 = SMAIndicator(s, window=50).sma_indicator()

    rsi14 = RSIIndicator(s, window=14).rsi()

    macd_obj = MACD(s)

    bb = BollingerBands(s)

    out = pd.DataFrame({
        "date": df["date"],
        "sma20": sma20,
        "sma50": sma50,
        "rsi14": rsi14,
        "macd": macd_obj.macd(),
        "macd_signal": macd_obj.macd_signal(),
        "macd_hist": macd_obj.macd_diff(),
        "bb_upper": bb.bollinger_hband(),
        "bb_mid": bb.bollinger_mavg(),
        "bb_lower": bb.bollinger_lband()
    }).dropna()

    cur = con.cursor()

    cur.executemany(
        """
        INSERT OR REPLACE INTO indicators_daily
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        [(ticker, *r) for r in out.itertuples(index=False, name=None)]
    )

    con.commit()
    con.close()

    print(f"{ticker} indicators computed")