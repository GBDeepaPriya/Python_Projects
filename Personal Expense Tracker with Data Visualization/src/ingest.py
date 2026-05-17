import pandas as pd
import sqlite3
import os

DB_PATH = "db/expenses.db"

STANDARD_COLS = [
    "tx_date",
    "description",
    "amount",
    "account",
    "category",
    "raw_source"
]

# =========================================================
# CREATE DATABASE + TABLE
# =========================================================
def init_db():

    os.makedirs("db", exist_ok=True)

    con = sqlite3.connect(DB_PATH)

    cur = con.cursor()

    # -----------------------------------------------------
    # DELETE OLD TABLE (IMPORTANT FIX)
    # -----------------------------------------------------
    cur.execute("DROP TABLE IF EXISTS transactions")

    # -----------------------------------------------------
    # CREATE NEW TABLE
    # -----------------------------------------------------
    cur.execute("""
        CREATE TABLE transactions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            tx_date TEXT,
            description TEXT,
            amount REAL,
            account TEXT,
            category TEXT,
            raw_source TEXT
        )
    """)

    con.commit()
    con.close()


# =========================================================
# READ CSV FILE
# =========================================================
def read_csv_file(path, account="Cash"):

    df = pd.read_csv(path)

    # -----------------------------
    # STANDARDIZE COLUMNS
    # -----------------------------
    df["tx_date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    df["description"] = df["Description"].astype(str)

    df["amount"] = pd.to_numeric(
        df["Amount"],
        errors="coerce"
    )

    df["account"] = account

    # -----------------------------
    # CATEGORY GENERATION
    # -----------------------------
    def auto_category(desc):

        desc = str(desc).lower()

        if "swiggy" in desc or "zomato" in desc or "restaurant" in desc:
            return "Food"

        elif "uber" in desc or "ola" in desc or "metro" in desc:
            return "Transport"

        elif "amazon" in desc or "flipkart" in desc:
            return "Shopping"

        elif "bill" in desc or "recharge" in desc:
            return "Bills"

        elif "movie" in desc or "netflix" in desc:
            return "Entertainment"

        elif "salary" in desc:
            return "Income"

        else:
            return "Others"

    df["category"] = df["description"].apply(auto_category)

    df["raw_source"] = path

    # -----------------------------
    # FINAL CLEAN
    # -----------------------------
    df = df[STANDARD_COLS].dropna()

    return df


# =========================================================
# BULK INSERT CSV DATA
# =========================================================
def upsert_transactions(df, db_path=DB_PATH):

    init_db()

    con = sqlite3.connect(db_path)

    cur = con.cursor()

    for row in df.itertuples(index=False):

        cur.execute("""
            INSERT INTO transactions (
                tx_date,
                description,
                amount,
                account,
                category,
                raw_source
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row.tx_date,
            row.description,
            row.amount,
            row.account,
            row.category,
            row.raw_source
        ))

    con.commit()
    con.close()


# =========================================================
# ADD TRANSACTION (FINAL FIX)
# =========================================================
def add_transaction(tx_date, description, amount, account, category):

    con = sqlite3.connect(DB_PATH)

    try:

        cur = con.cursor()

        # =================================================
        # CREATE CATEGORY COLUMN IF MISSING
        # =================================================
        columns = cur.execute("""
            PRAGMA table_info(transactions)
        """).fetchall()

        col_names = [c[1] for c in columns]

        if "category" not in col_names:

            cur.execute("""
                ALTER TABLE transactions
                ADD COLUMN category TEXT
            """)

            con.commit()

        # =================================================
        # INSERT TRANSACTION
        # =================================================
        cur.execute("""
            INSERT INTO transactions
            (
                tx_date,
                description,
                amount,
                account,
                category
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            str(tx_date),
            str(description),
            float(amount),
            str(account),
            str(category)
        ))

        # =================================================
        # COMMIT CHANGES
        # =================================================
        con.commit()

        print("✔ Transaction inserted successfully")

    except Exception as e:

        print("ERROR:", e)

    finally:

        con.close()


# =========================================================
# FETCH ALL TRANSACTIONS
# =========================================================
def fetch_transactions():

    init_db()

    con = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("""
        SELECT *
        FROM transactions
        ORDER BY tx_date DESC
    """, con)

    con.close()

    return df


# =========================================================
# TEST
# =========================================================
if __name__ == "__main__":

    init_db()

    df = read_csv_file(
        "data/sample_expenses.csv"
    )

    upsert_transactions(df)

    print("✔ Transactions inserted successfully")