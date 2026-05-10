import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_csv():

    print("\n📊 Generating REALISTIC 12-month finance dataset...")

    # =========================
    # CONFIGURATION
    # =========================
    start_date = datetime(2024, 1, 1)
    days = 365   # 🔥 1 YEAR DATA (IMPORTANT UPGRADE)

    categories = [
        "Food", "Transport", "Shopping",
        "Bills", "Entertainment", "Health", "Income"
    ]

    descriptions = {
        "Food": ["Swiggy", "Zomato", "Cafe Coffee Day", "Restaurant", "Dominos"],
        "Transport": ["Uber", "Ola", "Metro", "Petrol Pump", "Bus Ticket"],
        "Shopping": ["Amazon", "Flipkart", "Myntra", "Ajio", "Ikea"],
        "Bills": ["Electricity Bill", "Wifi Bill", "Mobile Recharge", "Water Bill"],
        "Entertainment": ["Netflix", "Spotify", "Movie Ticket", "BookMyShow"],
        "Health": ["Pharmacy", "Hospital", "Clinic Visit", "Medicine"],
        "Income": ["Salary Credit", "Freelance Payment", "Bonus"]
    }

    data = []

    salary_day = 28  # monthly salary cycle

    for i in range(days):

        date = start_date + timedelta(days=i)
        day = date.day

        # =========================
        # INCOME PATTERN (REALISTIC)
        # =========================
        if day == salary_day:
            amount = np.random.randint(30000, 70000)
            desc = np.random.choice(descriptions["Income"])
            category = "Income"

        else:
            # Weekend spending boost (real behavior)
            if date.weekday() >= 5:  # Saturday/Sunday
                weights = [0.3, 0.2, 0.2, 0.1, 0.1, 0.1]
            else:
                weights = [0.25, 0.2, 0.2, 0.15, 0.1, 0.1]

            category = np.random.choice(categories[:-1], p=weights)

            desc = np.random.choice(descriptions[category])

            # realistic expense variation
            base = {
                "Food": (100, 800),
                "Transport": (50, 500),
                "Shopping": (200, 3000),
                "Bills": (500, 5000),
                "Entertainment": (100, 1500),
                "Health": (100, 2000)
            }

            amount = -np.random.randint(*base[category])

        data.append([
            date.strftime("%Y-%m-%d"),
            desc,
            amount
        ])

    df = pd.DataFrame(data, columns=["Date", "Description", "Amount"])

    # =========================
    # SAVE FILE
    # =========================
    os.makedirs("data", exist_ok=True)

    file_path = "data/sample_expenses.csv"
    df.to_csv(file_path, index=False)

    print("✔ 1 YEAR REALISTIC DATASET CREATED!")
    print(f"✔ Total records: {len(df)}")
    print(f"✔ File saved at: {file_path}")


if __name__ == "__main__":
    generate_csv()