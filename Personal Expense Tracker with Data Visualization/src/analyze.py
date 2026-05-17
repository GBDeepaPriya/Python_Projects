import sqlite3
import pandas as pd

import streamlit as st

@st.cache_data(ttl=1)
def fetch_data(db="db/expenses.db"):

    con = sqlite3.connect(db)

    # -----------------------------------------------------
    # DIRECTLY FETCH CATEGORY FROM transactions TABLE
    # -----------------------------------------------------
    df = pd.read_sql_query("""
        SELECT
            tx_date,
            description,
            amount,
            account,
            category
        FROM transactions
        ORDER BY tx_date DESC
    """, con)

    con.close()

    # -----------------------------------------------------
    # EMPTY SAFE RETURN
    # -----------------------------------------------------
    if df.empty:
        return pd.DataFrame(columns=[
            "tx_date",
            "description",
            "amount",
            "account",
            "category",
            "month"
        ])

    # -----------------------------------------------------
    # DATA CLEANING
    # -----------------------------------------------------
    df["tx_date"] = pd.to_datetime(
        df["tx_date"],
        errors="coerce"
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    ).fillna(0)

    df["category"] = df["category"].fillna("Others")

    # -----------------------------------------------------
    # EXTRA FEATURES
    # -----------------------------------------------------
    df["month"] = df["tx_date"].dt.strftime("%Y-%m")

    df["date_only"] = df["tx_date"].dt.date

    return df


# =========================================================
# KPI CALCULATIONS
# =========================================================
def kpis(df):

    # -----------------------------------------------------
    # EXPENSE FILTER
    # -----------------------------------------------------
    expenses = df[df["amount"] < 0].copy()

    # -----------------------------------------------------
    # SAFE RETURN
    # -----------------------------------------------------
    if expenses.empty:

        return {
            "total_spend": 0,
            "avg_spend": 0,
            "top_category": "No Data",
            "transaction_count": 0
        }

    # -----------------------------------------------------
    # CALCULATIONS
    # -----------------------------------------------------
    total_spend = abs(expenses["amount"].sum())

    avg_spend = abs(expenses["amount"].mean())

    category_spend = (
        expenses.groupby("category")["amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )

    top_category = category_spend.index[0]

    transaction_count = len(expenses)

    # -----------------------------------------------------
    # RETURN KPIs
    # -----------------------------------------------------
    return {
        "total_spend": round(total_spend, 2),
        "avg_spend": round(avg_spend, 2),
        "top_category": top_category,
        "transaction_count": transaction_count
    }