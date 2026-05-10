import sqlite3
import pandas as pd

def fetch_data(db="db/expenses.db"):
    con = sqlite3.connect(db)

    df = pd.read_sql_query("""
        SELECT t.tx_date, t.description, t.amount, t.account, c.name as category
        FROM transactions t
        LEFT JOIN categories c ON t.category_id = c.id
    """, con)

    con.close()

    df["tx_date"] = pd.to_datetime(df["tx_date"])
    df["month"] = df["tx_date"].dt.to_period("M").astype(str)

    return df


def kpis(df):
    expenses = df[df.amount < 0]

    return {
        "total_spend": abs(expenses["amount"].sum()),
        "avg_spend": abs(expenses["amount"].mean()),
        "top_category": expenses.groupby("category")["amount"].sum().idxmin()
    }