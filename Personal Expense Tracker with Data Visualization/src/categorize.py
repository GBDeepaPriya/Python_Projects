import re
import sqlite3

RULES = {
    "Food": ["swiggy", "zomato", "restaurant", "cafe"],
    "Transport": ["uber", "ola", "petrol", "metro"],
    "Shopping": ["amazon", "flipkart", "myntra"],
    "Bills": ["electric", "wifi", "recharge"],
    "Entertainment": ["netflix", "movie", "spotify"],
}

def classify(text):
    text = text.lower()
    for cat, patterns in RULES.items():
        for p in patterns:
            if re.search(p, text):
                return cat
    return "Others"


def run(db="db/expenses.db"):
    con = sqlite3.connect(db)
    cur = con.cursor()

    rows = cur.execute("""
        SELECT id, description, amount FROM transactions
        WHERE category_id IS NULL
    """).fetchall()

    for r in rows:
        tx_id, desc, amt = r
        category = "Income" if amt > 0 else classify(desc)

        cat_id = cur.execute(
            "SELECT id FROM categories WHERE name=?",
            (category,)
        ).fetchone()

        if not cat_id:
            cur.execute("INSERT INTO categories(name) VALUES (?)", (category,))
            cat_id = cur.lastrowid
        else:
            cat_id = cat_id[0]

        cur.execute("""
            UPDATE transactions
            SET category_id=?
            WHERE id=?
        """, (cat_id, tx_id))

    con.commit()
    con.close()


if __name__ == "__main__":
    run()