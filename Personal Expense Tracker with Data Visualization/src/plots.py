import matplotlib.pyplot as plt
import pandas as pd


# =========================================================
# CATEGORY CHART
# =========================================================
def category_chart(df):

    fig, ax = plt.subplots(figsize=(7, 4))

    # safe expense filter
    expense_df = df[df["amount"] < 0]

    # group data
    data = (
        expense_df.groupby("category")["amount"]
        .sum()
        .abs()
    )

    # =====================================================
    # EMPTY DATA SAFETY FIX
    # =====================================================
    if data.empty:

        ax.text(
            0.5,
            0.5,
            "No expense data available",
            ha="center",
            va="center",
            fontsize=12
        )

        ax.set_axis_off()

        return fig

    # =====================================================
    # NORMAL CHART
    # =====================================================
    data.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Expense by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Amount")

    plt.xticks(rotation=45)

    return fig


# =========================================================
# MONTHLY TREND CHART
# =========================================================
def monthly_chart(df):

    fig, ax = plt.subplots(figsize=(7, 4))

    expense_df = df[df["amount"] < 0]

    monthly = (
        expense_df.groupby("month")["amount"]
        .sum()
        .abs()
    )

    # =====================================================
    # EMPTY SAFETY FIX
    # =====================================================
    if monthly.empty:

        ax.text(
            0.5,
            0.5,
            "No monthly expense data",
            ha="center",
            va="center",
            fontsize=12
        )

        ax.set_axis_off()

        return fig

    # =====================================================
    # NORMAL LINE CHART
    # =====================================================
    monthly.plot(
        kind="line",
        marker="o",
        ax=ax
    )

    ax.set_title("Monthly Expense Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount")

    plt.xticks(rotation=45)

    return fig