import streamlit as st
import pandas as pd

from analyze import fetch_data, kpis
from plots import category_chart, monthly_chart
from ingest import add_transaction
# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="💰 Personal Expense Tracker Dashboard",
    layout="wide",
    page_icon="💰"
)

# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <div style="text-align:center;">
        <h1 style="color:#00C853;">💰 Personal Expense Tracker Dashboard </h1>
        <p style="color:gray;">Track • Analyze • Optimize Your Money</p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD DATA (SAFE)
# =========================================================
df = fetch_data()

if df.empty:
    st.warning("⚠ No transactions found. Add expenses to begin tracking.")
    st.stop()

df["tx_date"] = pd.to_datetime(df["tx_date"])
df["month"] = df["tx_date"].dt.to_period("M").astype(str)
df["date_only"] = df["tx_date"].dt.date

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("📊 Controls")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Overview", "📊 Analytics", "➕ Add Expense"]
)

selected_month = st.sidebar.selectbox(
    "Select Month",
    sorted(df["month"].unique())
)

selected_account = st.sidebar.multiselect(
    "Accounts",
    df["account"].unique(),
    default=list(df["account"].unique())
)

filtered = df[
    (df["month"] == selected_month) &
    (df["account"].isin(selected_account))
]

# =========================================================
# SAFETY CHECK
# =========================================================
if filtered.empty:
    st.warning("⚠ No data available for selected filters")
    st.stop()

k = kpis(filtered)

# =========================================================
# 🏠 OVERVIEW
# =========================================================
if page == "🏠 Overview":

    st.subheader("📌 Financial Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💸 Total Spend", f"₹{k['total_spend']:.0f}")
    c2.metric("📊 Avg Spend", f"₹{k['avg_spend']:.0f}")
    c3.metric("🏆 Top Category", k['top_category'])
    c4.metric("📅 Month", selected_month)

    st.divider()

    colA, colB = st.columns(2)

    with colA:
        st.subheader("📊 Category Breakdown")
        st.pyplot(category_chart(filtered))

    with colB:
        st.subheader("📈 Monthly Trend")
        st.pyplot(monthly_chart(df))

    # 🔥 DAILY SPENDING SNAPSHOT
    st.divider()
    st.subheader("📅 Daily Spending Tracker")

    daily = filtered[filtered.amount < 0].groupby("date_only")["amount"].sum().abs()

    if not daily.empty:
        st.line_chart(daily)
    else:
        st.info("No expense data for selected period")

# =========================================================
# 📊 ANALYTICS
# =========================================================
elif page == "📊 Analytics":

    st.subheader("📊 Deep Financial Insights")

    monthly = df[df.amount < 0].groupby("month")["amount"].sum().abs()
    st.bar_chart(monthly)

    st.divider()

    st.subheader("📈 Cumulative Spend Growth")

    df_sorted = df.sort_values("tx_date")
    df_sorted["cumulative"] = df_sorted["amount"].cumsum()

    st.line_chart(df_sorted.set_index("tx_date")["cumulative"])

    st.divider()

    st.subheader("🍩 Spending Distribution")

    cat = filtered[filtered.amount < 0].groupby("category")["amount"].sum().abs()

    if not cat.empty:
        st.pyplot(cat.plot.pie(
            autopct="%1.1f%%",
            figsize=(5, 5),
            title="Category Split"
        ).figure)

# =========================================================
# ➕ ADD EXPENSE (LIVE TRACKING ADDED)
# =========================================================
elif page == "➕ Add Expense":

    st.subheader("➕ Add Transaction (Live Finance Tracker)")

    # =====================================================
    # FORM INPUT
    # =====================================================
    with st.form("expense_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Date")
            desc = st.text_input("Description")

        with col2:
            amount = st.number_input(
                "Amount (Positive = Income, Negative = Expense)",
                value=0.0
            )
            account = st.selectbox("Account", df["account"].unique())

        category = st.selectbox(
            "Category",
            ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Others"]
        )

        submit = st.form_submit_button("➕ Add Transaction")

    # =====================================================
    # INSERT INTO DATABASE
    # =====================================================
    if submit:

        add_transaction(
            tx_date=str(date),
            description=desc,
            amount=amount,
            account=account,
            category=category
        )

        st.success("✔ Transaction added successfully!")
        st.rerun()

    # =====================================================
    # LOAD DATA
    # =====================================================
    df_live = fetch_data()

    if df_live.empty:
        st.info("No transactions yet.")
        st.stop()

    # =====================================================
    # DATA CLEANING
    # =====================================================
    df_live["tx_date"] = pd.to_datetime(df_live["tx_date"], errors="coerce")
    df_live["amount"] = pd.to_numeric(df_live["amount"], errors="coerce").fillna(0)

    df_live["date_only"] = df_live["tx_date"].dt.date
    df_live["month"] = df_live["tx_date"].dt.to_period("M").astype(str)

    df_live["expense"] = df_live["amount"].apply(lambda x: -abs(x) if x != 0 else 0)

    today = pd.Timestamp.today().date()
    current_month = pd.Timestamp.today().strftime("%Y-%m")

    today_df = df_live[df_live["date_only"] == today].copy()
    month_df = df_live[df_live["month"] == current_month].copy()

    expense_today = today_df[today_df["expense"] < 0]
    expense_month = month_df[month_df["expense"] < 0]

    # =====================================================
    # 📅 SUMMARY METRICS
    # =====================================================
    st.divider()
    st.subheader("📊 Expense Overview")

    col1, col2 = st.columns(2)

    col1.metric("💸 Today Spend", f"₹{abs(expense_today['expense'].sum()):.2f}")
    col2.metric("💸 Month Spend", f"₹{abs(expense_month['expense'].sum()):.2f}")


    st.subheader("📋 Today's Transaction Details")

    if not today_df.empty:

        display_today = today_df[[
            "tx_date",
            "description",
            "category",
            "account",
            "amount"
        ]].sort_values(by="tx_date", ascending=False)

        st.dataframe(display_today, use_container_width=True)

    else:
        st.info("No transactions today to display")