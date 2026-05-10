import pandas as pd
import sqlite3

STANDARD_COLS = ["tx_date", "description", "amount", "account", "raw_source"]
DB_PATH = "db/expenses.db"

def read_csv_file(path, account="Cash"):
    df = pd.read_csv(path)

    df["tx_date"] = pd.to_datetime(df["Date"]).dt.date.astype(str)
    df["description"] = df["Description"].astype(str)
    df["amount"] = pd.to_numeric(df["Amount"], errors="coerce")
    df["account"] = account
    df["raw_source"] = path

    return df[STANDARD_COLS].dropna()


def upsert_transactions(df, db_path="db/expenses.db"):
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    for row in df.itertuples(index=False):
        cur.execute("""
        INSERT OR IGNORE INTO transactions
        (tx_date, description, amount, account, raw_source)
        VALUES (?, ?, ?, ?, ?)
        """, row)

    con.commit()
    con.close()

# =========================================================
def add_transaction(tx_date, description, amount, account, category):

    con = sqlite3.connect(DB_PATH)

    try:
        cur = con.cursor()

        # try new schema (with category)
        try:
            cur.execute("""
                INSERT OR IGNORE INTO transactions 
                (tx_date, description, amount, account, category)
                VALUES (?, ?, ?, ?, ?)
            """, (tx_date, description, amount, account, category))

        # fallback old schema
        except Exception:
            cur.execute("""
                INSERT OR IGNORE INTO transactions 
                (tx_date, description, amount, account)
                VALUES (?, ?, ?, ?)
            """, (tx_date, description, amount, account))

        con.commit()

    finally:
        # ALWAYS SAFE CLOSE (even if error happens)
        con.close()

if __name__ == "__main__":
    df = read_csv_file("data/sample_expenses.csv")
    upsert_transactions(df)