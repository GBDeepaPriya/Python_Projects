import matplotlib.pyplot as plt

def category_chart(df):
    data = (-df[df.amount < 0].groupby("category")["amount"].sum())
    plt.figure()
    data.plot(kind="bar")
    plt.title("Category Spending")
    return plt


def monthly_chart(df):
    data = (-df[df.amount < 0].groupby("month")["amount"].sum())
    plt.figure()
    data.plot(marker="o")
    plt.title("Monthly Trend")
    return plt