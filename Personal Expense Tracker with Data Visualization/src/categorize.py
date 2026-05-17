import re
import sqlite3

DB_PATH = "db/expenses.db"

# =========================================================
# CATEGORY RULES
# =========================================================
RULES = {
    "Food": ["swiggy", "zomato", "restaurant", "cafe", "pizza", "burger"],
    "Transport": ["uber", "ola", "petrol", "metro", "bus", "fuel"],
    "Shopping": ["amazon", "flipkart", "myntra", "shopping"],
    "Bills": ["electric", "wifi", "recharge", "bill", "rent"],
    "Entertainment": ["netflix", "movie", "spotify", "hotstar"],
    "Salary": ["salary", "credit", "income"],
}


# =========================================================
# TEXT CLASSIFIER
# =========================================================
def classify(description, amount):

    # income handling
    if amount > 0:
        return "Income"

    text = str(description).lower()

    for category, patterns in RULES.items():

        for pattern in patterns:

            if re.search(pattern, text):
                return category

    return "Others"


# =========================================================
# ENSURE CATEGORY COLUMN EXISTS
# =========================================================
def ensure_category_column():

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    columns = cur.execute("""
        PRAGMA table_info(transactions)
    """).fetchall()

    col_names = [c[1] for c in columns]

    # add category column if missing
    if "category" not in col_names:

        cur.execute("""
            ALTER TABLE transactions
            ADD COLUMN category TEXT
        """)

        con.commit()

    con.close()


# =========================================================
# AUTO CATEGORIZE TRANSACTIONS
# =========================================================
def run(db=DB_PATH):

    ensure_category_column()

    con = sqlite3.connect(db)
    cur = con.cursor()

    # get uncategorized rows
    rows = cur.execute("""
        SELECT id, description, amount
        FROM transactions
        WHERE category IS NULL
           OR category = ''
    """).fetchall()

    updated = 0

    for row in rows:

        tx_id, desc, amount = row

        category = classify(desc, amount)

        cur.execute("""
            UPDATE transactions
            SET category = ?
            WHERE id = ?
        """, (category, tx_id))

        updated += 1

    con.commit()
    con.close()

    print(f"✔ Categorized {updated} transactions successfully")


# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    run()