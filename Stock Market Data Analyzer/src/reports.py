def generate_report(ticker, stats):

    report = f"""
    STOCK ANALYSIS REPORT
    =====================

    Ticker: {ticker}

    Total Return:
    {stats['Total Return']:.2%}

    Sharpe Ratio:
    {stats['Sharpe Ratio']:.2f}

    Max Drawdown:
    {stats['Max Drawdown']:.2%}
    """

    with open(f"reports/{ticker}_report.txt", "w") as f:
        f.write(report)

    print("Report Generated!")