import sqlite3

DB = "db/market.db"

def check_alerts():

    con = sqlite3.connect(DB)

    cur = con.cursor()

    rows = cur.execute("""
    SELECT ticker, rsi14
    FROM indicators_daily
    ORDER BY date DESC
    LIMIT 10
    """).fetchall()

    for ticker, rsi in rows:

        if rsi and rsi < 30:
            print(f"BUY ALERT: {ticker} RSI below 30")

        elif rsi and rsi > 70:
            print(f"SELL ALERT: {ticker} RSI above 70")

    con.close()

check_alerts()