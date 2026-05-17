import sqlite3
import pandas as pd
import os

DB_PATH = "db/expenses.db"
OUTPUT_PATH = "data/exported_expenses.csv"


def export_to_csv():
    print("\n📤 Exporting data from SQLite database...")

    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("Database not found. Run main.py first.")

    con = sqlite3.connect(DB_PATH)

    query = """
    SELECT 
        t.tx_date,
        t.description,
        t.amount,
        t.account,
        c.name AS category
    FROM transactions t
    LEFT JOIN categories c
    ON t.category_id = c.id
    ORDER BY t.tx_date
    """

    df = pd.read_sql_query(query, con)
    con.close()

    # Ensure folder exists
    os.makedirs("data", exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print(f"✔ CSV exported successfully to: {OUTPUT_PATH}")
    print(f"✔ Total records: {len(df)}")


if __name__ == "__main__":
    export_to_csv()