"""
💰 Personal Expense Tracker - MASTER RUNNER (PRODUCTION VERSION)

Pipeline:
1. Initialize DB
2. Auto-generate REALISTIC dataset (if missing)
3. Ingest CSV into SQLite
4. Categorize transactions
5. Run analysis
6. Show summary
7. Launch Streamlit dashboard (optional)
"""

import os
import subprocess

from src.models import init_db
from src.ingest import read_csv_file, upsert_transactions
from src.categorize import run as categorize_run
from src.analyze import fetch_data, kpis


# ----------------------------
# 🔥 IMPORT NEW REALISTIC GENERATOR
# ----------------------------
def generate_sample_csv():
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta

    print("\n📊 Generating REALISTIC 12-MONTH DATASET...")

    start_date = datetime(2024, 1, 1)
    days = 365

    categories = [
        "Food", "Transport", "Shopping",
        "Bills", "Entertainment", "Health", "Income"
    ]

    descriptions = {
        "Food": ["Swiggy", "Zomato", "Cafe"],
        "Transport": ["Uber", "Ola", "Metro"],
        "Shopping": ["Amazon", "Flipkart", "Myntra"],
        "Bills": ["Electric Bill", "Wifi Bill", "Mobile Recharge"],
        "Entertainment": ["Netflix", "Movie", "Spotify"],
        "Health": ["Hospital", "Pharmacy", "Clinic"],
        "Income": ["Salary Credit"]
    }

    data = []

    salary_day = 28

    for i in range(days):
        date = start_date + timedelta(days=i)

        # Income cycle (monthly salary)
        if date.day == salary_day:
            amount = np.random.randint(30000, 70000)
            desc = "Salary Credit"
            category = "Income"
        else:
            if date.weekday() >= 5:
                probs = [0.3, 0.2, 0.2, 0.1, 0.1, 0.1]
            else:
                probs = [0.25, 0.2, 0.2, 0.15, 0.1, 0.1]

            category = np.random.choice(categories[:-1], p=probs)
            desc = np.random.choice(descriptions[category])

            base = {
                "Food": (100, 800),
                "Transport": (50, 500),
                "Shopping": (200, 3000),
                "Bills": (500, 5000),
                "Entertainment": (100, 1500),
                "Health": (100, 2000)
            }

            amount = -np.random.randint(*base[category])

        data.append([date.strftime("%Y-%m-%d"), desc, amount])

    df = pd.DataFrame(data, columns=["Date", "Description", "Amount"])

    os.makedirs("data", exist_ok=True)

    path = "data/sample_expenses.csv"
    df.to_csv(path, index=False)

    print("✔ REALISTIC DATASET CREATED (12 MONTHS)")
    print(f"✔ Total records: {len(df)}")


# ----------------------------
# STEP 1
# ----------------------------
def step_init_db():
    print("\n[STEP 1] Initializing database...")
    init_db()
    print("✔ Database ready.")


# ----------------------------
# STEP 2
# ----------------------------
def step_ingest():
    print("\n[STEP 2] Loading CSV data...")

    csv_path = "data/sample_expenses.csv"

    # 🔥 AUTO FIX: GENERATE IF MISSING
    if not os.path.exists(csv_path):
        print("⚠ CSV not found. Generating realistic dataset...")
        generate_sample_csv()

    df = read_csv_file(csv_path, account="Manual")
    upsert_transactions(df)

    print(f"✔ Ingested {len(df)} transactions.")


# ----------------------------
# STEP 3
# ----------------------------
def step_categorize():
    print("\n[STEP 3] Categorizing transactions...")
    categorize_run()
    print("✔ Categorization completed.")


# ----------------------------
# STEP 4
# ----------------------------
def step_analysis():
    print("\n[STEP 4] Running analytics...")

    df = fetch_data()
    result = kpis(df)

    print("\n📊 FINANCIAL SUMMARY")
    print("-" * 40)
    print(f"Total Spending : ₹{result['total_spend']:.2f}")
    print(f"Average Spend  : ₹{result['avg_spend']:.2f}")
    print(f"Top Category   : {result['top_category']}")
    print("-" * 40)

    return df


# ----------------------------
# STEP 5
# ----------------------------
def launch_dashboard():
    print("\n[STEP 5] Launching Streamlit Dashboard...")

    subprocess.run(
        ["streamlit", "run", "src/app_streamlit.py"],
        check=True
    )


# ----------------------------
# MAIN
# ----------------------------
def main():

    print("\n===================================")
    print("💰 PERSONAL EXPENSE TRACKER SYSTEM")
    print("===================================\n")

    step_init_db()
    step_ingest()
    step_categorize()
    step_analysis()

    print("\n✔ Pipeline completed successfully!")

    choice = input("\nLaunch Streamlit dashboard? (y/n): ")

    if choice.lower() == "y":
        launch_dashboard()
    else:
        print("✔ Done. Data ready for analysis.")


# ----------------------------
if __name__ == "__main__":
    main()