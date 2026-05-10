import sqlite3

with open("db/schema.sql", "r") as f:
    schema = f.read()

con = sqlite3.connect("db/market.db")
con.executescript(schema)
con.commit()
con.close()

print("Database initialized successfully!")