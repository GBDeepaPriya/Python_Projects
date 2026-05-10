import yfinance as yf
import pandas as pd
import sqlite3
import datetime as dt

DB = "db/market.db"


def fetch_daily(ticker, start="2024-01-01"):

    print(f"Downloading {ticker}...")

    df = yf.download(
        ticker,
        start=start,
        end=dt.date.today().isoformat(),
        progress=False,
        auto_adjust=False
    )

    # EMPTY CHECK
    if df.empty:
        raise Exception(f"No data returned for {ticker}")

    # RESET INDEX
    df = df.reset_index()

    # HANDLE MULTIINDEX
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    # LOWERCASE
    df.columns = [str(col).lower() for col in df.columns]

    print(df.columns.tolist())

    # DATE COLUMN FIX
    if "date" not in df.columns:

        if "datetime" in df.columns:
            df.rename(columns={"datetime": "date"}, inplace=True)

        elif "index" in df.columns:
            df.rename(columns={"index": "date"}, inplace=True)

        else:
            raise Exception(
                f"Date column missing for {ticker}"
            )

    # ADJ CLOSE FIX
    if "adj close" in df.columns:
        df.rename(
            columns={"adj close": "adj_close"},
            inplace=True
        )

    # SOME TICKERS MAY MISS adj_close
    if "adj_close" not in df.columns:
        df["adj_close"] = df["close"]

    # DATE FORMAT
    df["date"] = pd.to_datetime(
        df["date"]
    ).dt.strftime("%Y-%m-%d")

    required = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume"
    ]

    df = df[required]

    # REMOVE NULLS
    df = df.dropna()

    return df


def upsert_daily(ticker):

    df = fetch_daily(ticker)

    con = sqlite3.connect(DB)

    cur = con.cursor()

    rows = [
        (ticker, *r)
        for r in df.itertuples(index=False, name=None)
    ]

    cur.executemany("""
        INSERT OR REPLACE INTO candles_daily
        (ticker,date,open,high,low,close,adj_close,volume)
        VALUES (?,?,?,?,?,?,?,?)
    """, rows)

    con.commit()

    con.close()

    print(f"{ticker} inserted successfully!")