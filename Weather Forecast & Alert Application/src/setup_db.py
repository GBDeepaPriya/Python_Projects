import sqlite3
import os

# ==========================================
# CREATE DB FOLDER
# ==========================================

os.makedirs("db", exist_ok=True)

DB = "db/weather.db"

con = sqlite3.connect(DB)

cur = con.cursor()

# ==========================================
# USERS TABLE
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS users(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    email TEXT,

    phone TEXT,

    telegram_chat_id TEXT,

    preferred_alert TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# ==========================================
# LOCATIONS TABLE
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS locations(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    city_name TEXT,

    lat REAL,

    lon REAL,

    timezone TEXT,

    FOREIGN KEY(user_id)
    REFERENCES users(id)
)
""")

# ==========================================
# WEATHER HOURLY TABLE
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS weather_hourly(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    location_id INTEGER,

    ts TEXT,

    temp_c REAL,

    humidity REAL,

    wind_ms REAL,

    precip_prob REAL
)
""")

# ==========================================
# WEATHER DAILY TABLE
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS weather_daily(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    location_id INTEGER,

    date TEXT,

    tmax_c REAL,

    tmin_c REAL,

    rain_mm REAL,

    uv_max REAL
)
""")

# ==========================================
# ALERTS TABLE
# ==========================================

cur.execute("""
CREATE TABLE IF NOT EXISTS alerts(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    location_id INTEGER,

    alert_code TEXT,

    alert_message TEXT,

    severity TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

con.commit()

con.close()

print("Database Created Successfully")