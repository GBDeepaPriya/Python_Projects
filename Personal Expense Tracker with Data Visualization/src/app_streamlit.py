import streamlit as st
import pandas as pd

from analyze import fetch_data, kpis
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
        <h1 style="color:#00C853;">
            💰 Personal Expense Tracker Dashboard
        </h1>
        <p style="color:gray;">
            Track • Analyze • Optimize Your Money
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD DATA FUNCTION
# =========================================================
def load_data():

    df = fetch_data()

    if df.empty:
        return pd.DataFrame(
            columns=[
                "tx_date",
                "description",
                "amount",
                "account",
                "category"
            ]
        )

    # SAFE CLEANING
    df["tx_date"] = pd.to_datetime(
        df["tx_date"],
        errors="coerce"
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    ).fillna(0)

    df["category"] = df["category"].fillna("Others")

    df = df.dropna(subset=["tx_date"])

    # DATE FEATURES
    df["month"] = df["tx_date"].dt.strftime("%Y-%m")

    df["date_only"] = df["tx_date"].dt.date

    return df


# =========================================================
# SESSION STATE
# =========================================================
if "live_data" not in st.session_state:

    st.session_state.live_data = load_data()

# ALWAYS USE UPDATED SESSION DATA
df = st.session_state.live_data.copy()

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("📊 Controls")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Overview",
        "📊 Analytics",
        "➕ Add Expense"
    ]
)

# =========================================================
# SAFE FILTER VALUES
# =========================================================
if not df.empty:

    valid_months = sorted(
        df["month"]
        .dropna()
        .astype(str)
        .unique(),
        reverse=True
    )

    selected_month = st.sidebar.selectbox(
        "Select Month",
        valid_months
    )

    selected_account = st.sidebar.multiselect(
        "Accounts",
        sorted(df["account"].dropna().astype(str).unique()),
        default=list(
            sorted(
                df["account"]
                .dropna()
                .astype(str)
                .unique()
            )
        )
    )

    filtered = df[
        (df["month"] == selected_month) &
        (df["account"].isin(selected_account))
    ]

else:

    filtered = pd.DataFrame()

# =========================================================
# OVERVIEW PAGE (LIVE UPDATED)
# =========================================================
if page == "🏠 Overview":

    st.subheader("📌 Financial Overview")

    live_df = st.session_state.live_data.copy()

    if live_df.empty:
        st.info("No data available")
        st.stop()

    # CLEAN DATA
    live_df["tx_date"] = pd.to_datetime(
        live_df["tx_date"],
        errors="coerce"
    )

    live_df["amount"] = pd.to_numeric(
        live_df["amount"],
        errors="coerce"
    ).fillna(0)

    live_df["date_only"] = live_df["tx_date"].dt.date

    live_df["month"] = live_df["tx_date"].dt.strftime("%Y-%m")

    # IMPORTANT FIX
    live_df["expense"] = live_df["amount"].abs()

    # FILTER
    filtered = live_df[
        (live_df["month"] == selected_month) &
        (live_df["account"].isin(selected_account))
    ]

    # KPI
    total_spend = filtered["expense"].sum()

    avg_spend = (
        filtered["expense"].mean()
        if not filtered.empty else 0
    )

    top_category = "N/A"

    if not filtered.empty:

        top_category = (
            filtered.groupby("category")["expense"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )

    # METRICS
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💸 Total Spend",
        f"₹{total_spend:.2f}"
    )

    c2.metric(
        "📊 Avg Spend",
        f"₹{avg_spend:.2f}"
    )

    c3.metric(
        "🏆 Top Category",
        top_category
    )

    c4.metric(
        "📅 Month",
        selected_month
    )

    st.divider()

    # CATEGORY GRAPH
    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📊 Category Breakdown")

        category_data = (
            filtered.groupby("category")["expense"]
            .sum()
            .sort_values(ascending=False)
        )

        if not category_data.empty:
            st.bar_chart(category_data)

    # MONTHLY TREND
    with col2:

        st.subheader("📈 Monthly Expense Trend")

        monthly_data = (
            live_df.groupby("month")["expense"]
            .sum()
            .sort_index()
        )

        if not monthly_data.empty:
            st.line_chart(monthly_data)

    
    

# =========================================================
# ANALYTICS PAGE
# =========================================================
elif page == "📊 Analytics":

    st.subheader("📊 Deep Financial Insights")

    live_df = st.session_state.live_data.copy()

    if live_df.empty:
        st.info("No analytics available")
        st.stop()

    # CLEAN
    live_df["tx_date"] = pd.to_datetime(
        live_df["tx_date"],
        errors="coerce"
    )

    live_df["amount"] = pd.to_numeric(
        live_df["amount"],
        errors="coerce"
    ).fillna(0)

    live_df["date_only"] = live_df["tx_date"].dt.date

    live_df["month"] = live_df["tx_date"].dt.strftime("%Y-%m")

    # IMPORTANT FIX
    live_df["expense"] = live_df["amount"].abs()

    # =====================================================
    # MONTHLY EXPENSES
    # =====================================================
    st.subheader("📆 Monthly Expenses")

    monthly_expense = (
        live_df.groupby("month")["expense"]
        .sum()
        .sort_index()
    )

    if not monthly_expense.empty:
        st.bar_chart(monthly_expense)

    # =====================================================
    # CUMULATIVE GROWTH
    # =====================================================
    st.divider()

    st.subheader("📈 Cumulative Expense Growth")

    cumulative_df = live_df.sort_values("tx_date")

    cumulative_df["cumulative"] = (
        cumulative_df["expense"].cumsum()
    )

    st.line_chart(
        cumulative_df.set_index("tx_date")[
            "cumulative"
        ]
    )

    # =====================================================
    # CATEGORY DISTRIBUTION
    # =====================================================
    st.divider()

    st.subheader("📊 Spending Distribution")

    category_dist = (
        live_df.groupby("category")["expense"]
        .sum()
        .sort_values(ascending=False)
    )

    if not category_dist.empty:
        st.bar_chart(category_dist)

    # =====================================================
    # DAILY ANALYTICS
    # =====================================================
    st.divider()

    st.subheader("📅 Daily Expense Analytics")

    daily_analytics = (
        live_df.groupby("date_only")["expense"]
        .sum()
        .sort_index()
    )

    if not daily_analytics.empty:
        st.area_chart(daily_analytics)

# =========================================================
# ADD EXPENSE PAGE
# =========================================================
elif page == "➕ Add Expense":

    st.subheader("➕ Add Transaction (Live Finance Tracker)")

    # =====================================================
    # INITIALIZE SESSION DATA
    # =====================================================
    if "live_data" not in st.session_state:

        st.session_state.live_data = fetch_data()

    # =====================================================
    # ALWAYS USE SESSION DATA
    # =====================================================
    live_df = st.session_state.live_data.copy()

    # =====================================================
    # CLEAN DATA
    # =====================================================
    if not live_df.empty:

        live_df["tx_date"] = pd.to_datetime(
            live_df["tx_date"],
            errors="coerce"
        )

        live_df["amount"] = pd.to_numeric(
            live_df["amount"],
            errors="coerce"
        ).fillna(0)

        live_df["date_only"] = live_df["tx_date"].dt.date

        live_df["month"] = live_df["tx_date"].dt.strftime("%Y-%m")

    # =====================================================
    # TRANSACTION FORM
    # =====================================================
    with st.form("expense_form", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:

            date = st.date_input("Date")

            desc = st.text_input("Description")

        with col2:

            amount = st.number_input(
                "Amount",
                value=0.0,
                step=1.0
            )

            account = st.selectbox(
                "Account",
                ["Cash", "Bank", "UPI", "Credit Card"]
            )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Transport",
                "Shopping",
                "Bills",
                "Entertainment",
                "Salary",
                "Others"
            ]
        )

        submit = st.form_submit_button("➕ Add Transaction")

    # =====================================================
    # SAVE TRANSACTION
    # =====================================================
    if submit:

        # SAVE TO DATABASE
        add_transaction(
            tx_date=str(date),
            description=desc,
            amount=float(amount),
            account=account,
            category=category
        )

        # CREATE NEW ROW
        new_row = pd.DataFrame([{
            "tx_date": pd.to_datetime(date),
            "description": desc,
            "amount": float(amount),
            "account": account,
            "category": category
        }])

        # UPDATE SESSION STATE
        st.session_state.live_data = pd.concat(
            [live_df, new_row],
            ignore_index=True
        )

        st.success("✔ Transaction Added Successfully!")

        st.rerun()

    # =====================================================
    # RELOAD UPDATED SESSION DATA
    # =====================================================
    live_df = st.session_state.live_data.copy()

    # =====================================================
    # SAFE CHECK
    # =====================================================
    if live_df.empty:

        st.info("No transactions available.")
        st.stop()

    # =====================================================
    # CLEAN AGAIN
    # =====================================================
    live_df["tx_date"] = pd.to_datetime(
        live_df["tx_date"],
        errors="coerce"
    )

    live_df["amount"] = pd.to_numeric(
        live_df["amount"],
        errors="coerce"
    ).fillna(0)

    live_df["date_only"] = live_df["tx_date"].dt.date

    live_df["month"] = live_df["tx_date"].dt.strftime("%Y-%m")

    # =====================================================
    # CURRENT DATE FILTERS
    # =====================================================
    today = pd.Timestamp.today().date()

    current_month = pd.Timestamp.today().strftime("%Y-%m")

    # =====================================================
    # FILTER DATA
    # =====================================================
    today_df = live_df[
        live_df["date_only"] == today
    ].copy()

    month_df = live_df[
        live_df["month"] == current_month
    ].copy()

    # =====================================================
    # FIXED SPEND LOGIC
    # =====================================================
    today_df["expense"] = today_df["amount"].abs()

    month_df["expense"] = month_df["amount"].abs()

    # =====================================================
    # TOTAL SPEND
    # =====================================================
    today_total = today_df["expense"].sum()

    month_total = month_df["expense"].sum()

    # =====================================================
    # SUMMARY METRICS
    # =====================================================
    st.divider()

    col1, col2 = st.columns(2)

    col1.metric(
        "💸 Today's Spend",
        f"₹{today_total:.2f}"
    )

    col2.metric(
        "📆 Monthly Spend",
        f"₹{month_total:.2f}"
    )

    # =====================================================
    # DAILY TRACKING GRAPH
    # =====================================================
    st.divider()

    st.subheader("📈 Daily Expense Tracking")

    daily_tracking = (
        month_df.groupby("date_only")["expense"]
        .sum()
        .sort_index()
    )

    if not daily_tracking.empty:

        st.line_chart(daily_tracking)

    else:

        st.info("No expense data available")
    

    # =====================================================
    # CATEGORY TRACKING
    # =====================================================
    st.divider()

    st.subheader("📊 Monthly Category Tracking")

    category_tracking = (
        month_df.groupby("category")["expense"]
        .sum()
        .sort_values(ascending=False)
    )

    if not category_tracking.empty:

        st.bar_chart(category_tracking)

    else:

        st.info("No category tracking data")

    # =====================================================
    # TODAY'S TRANSACTIONS
    # =====================================================
    st.divider()

    st.subheader("📋 Today's Transactions")

    if not today_df.empty:

        display_today = today_df[
            [
                "tx_date",
                "description",
                "category",
                "account",
                "amount"
            ]
        ].sort_values(
            by="tx_date",
            ascending=False
        )

        st.dataframe(
            display_today,
            use_container_width=True
        )

    else:

        st.info("No transactions today")

    # =====================================================
    # RECENT TRANSACTIONS
    # =====================================================
    st.divider()

    st.subheader("🕒 Recent Transactions")

    recent = live_df.sort_values(
        by="tx_date",
        ascending=False
    )

    st.dataframe(
        recent[
            [
                "tx_date",
                "description",
                "category",
                "account",
                "amount"
            ]
        ].head(15),
        use_container_width=True
    )