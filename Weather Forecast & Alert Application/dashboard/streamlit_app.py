# dashboard/streamlit_app.py

import streamlit as st
import sqlite3
import sys
import os
import pandas as pd
import plotly.express as px

# ======================================================
# FIX IMPORT ISSUES
# ======================================================

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

# ======================================================
# IMPORTS
# ======================================================

from src.ingest import fetch_open_meteo
from src.utils import get_coordinates
from src.rules import evaluate
from notify.email_alert import send_email

# ======================================================
# DATABASE
# ======================================================

DB = "db/weather.db"

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Weather Forecast & Email Alert System",
    layout="wide"
)

# ======================================================
# TITLE
# ======================================================

st.title("🌦 Weather Forecast & Email Alert Application")

st.markdown("""
### Real-Time Weather Monitoring System

Features:
- Live Weather Forecast
- Smart Weather Alerts
- Email Notifications
- Interactive Dashboard
- Auto Location Detection
""")

# ======================================================
# USER DETAILS
# ======================================================

st.header("👤 User Details")

name = st.text_input(
    "Enter Your Name"
)

email = st.text_input(
    "Enter Your Email Address"
)

# ======================================================
# LOCATION DETAILS
# ======================================================

st.header("📍 Location")

city = st.text_input(
    "Enter City Name"
)

timezone = st.text_input(
    "Timezone",
    value="Asia/Kolkata"
)

# ======================================================
# BUTTON
# ======================================================

if st.button("🚀 Fetch Weather Forecast"):

    # ==================================================
    # VALIDATION
    # ==================================================

    if not name:

        st.error("Please enter your name")

        st.stop()

    if not email:

        st.error("Please enter email address")

        st.stop()

    if not city:

        st.error("Please enter city name")

        st.stop()

    # ==================================================
    # GET COORDINATES
    # ==================================================

    st.info("Detecting Location Coordinates...")

    coords = get_coordinates(city)

    if not coords:

        st.error("Invalid city name")

        st.stop()

    lat = coords["latitude"]
    lon = coords["longitude"]

    st.success("Location Detected Successfully")

    st.write(f"Latitude: {lat}")
    st.write(f"Longitude: {lon}")

    # ==================================================
    # DATABASE CONNECTION
    # ==================================================

    con = sqlite3.connect(DB)

    cur = con.cursor()

    # ==================================================
    # SAVE USER
    # ==================================================

    cur.execute("""
    INSERT INTO users(
        name,
        email
    )
    VALUES(?,?)
    """, (
        name,
        email
    ))

    user_id = cur.lastrowid

    # ==================================================
    # SAVE LOCATION
    # ==================================================

    cur.execute("""
    INSERT INTO locations(
        user_id,
        city_name,
        lat,
        lon,
        timezone
    )
    VALUES(?,?,?,?,?)
    """, (
        user_id,
        city,
        lat,
        lon,
        timezone
    ))

    location_id = cur.lastrowid

    con.commit()

    st.success("User & Location Saved Successfully")

    # ==================================================
    # FETCH WEATHER DATA
    # ==================================================

    st.info("Fetching Weather Forecast...")

    try:

        data = fetch_open_meteo(
            lat,
            lon,
            timezone
        )

    except Exception as e:

        st.error(f"Weather API Error: {e}")

        st.stop()

    # ==================================================
    # CURRENT WEATHER
    # ==================================================

    st.header("🌤 Current Weather")

    current_weather = data["current_weather"]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Temperature",
        f"{current_weather['temperature']} °C"
    )

    col2.metric(
        "Wind Speed",
        f"{current_weather['windspeed']} km/h"
    )

    col3.metric(
        "Weather Code",
        current_weather["weathercode"]
    )

    # ==================================================
    # HOURLY DATA
    # ==================================================

    hourly_data = data["hourly"]

    hourly_df = pd.DataFrame({

        "time":
        hourly_data["time"][:24],

        "temperature":
        hourly_data["temperature_2m"][:24],

        "rain_probability":
        hourly_data["precipitation_probability"][:24],

        "wind_speed":
        hourly_data["wind_speed_10m"][:24]
    })

    # ==================================================
    # TEMPERATURE CHART
    # ==================================================

    st.header("🌡 24 Hour Temperature Forecast")

    temp_chart = px.line(
        hourly_df,
        x="time",
        y="temperature",
        markers=True,
        title="Temperature Forecast"
    )

    st.plotly_chart(
        temp_chart,
        use_container_width=True
    )

    # ==================================================
    # RAIN CHART
    # ==================================================

    st.header("🌧 Rain Probability Forecast")

    rain_chart = px.bar(
        hourly_df,
        x="time",
        y="rain_probability",
        title="Rain Probability Forecast"
    )

    st.plotly_chart(
        rain_chart,
        use_container_width=True
    )

    # ==================================================
    # WIND CHART
    # ==================================================

    st.header("💨 Wind Speed Forecast")

    wind_chart = px.line(
        hourly_df,
        x="time",
        y="wind_speed",
        markers=True,
        title="Wind Speed Forecast"
    )

    st.plotly_chart(
        wind_chart,
        use_container_width=True
    )

    # ==================================================
    # DAILY DATA
    # ==================================================

    daily_data = data["daily"]

    daily_df = pd.DataFrame({

        "date":
        daily_data["time"],

        "max_temp":
        daily_data["temperature_2m_max"],

        "min_temp":
        daily_data["temperature_2m_min"],

        "uv_index":
        daily_data["uv_index_max"]
    })

    # ==================================================
    # 7 DAY FORECAST
    # ==================================================

    st.header("📅 7 Day Forecast")

    forecast_chart = px.line(
        daily_df,
        x="date",
        y=["max_temp", "min_temp"],
        markers=True,
        title="7 Day Temperature Forecast"
    )

    st.plotly_chart(
        forecast_chart,
        use_container_width=True
    )

    # ==================================================
    # ALERT ENGINE
    # ==================================================

    alerts = evaluate(
        hourly_data,
        daily_data
    )

    # ==================================================
    # DISPLAY ALERTS
    # ==================================================

    st.header("⚠ Weather Alerts")

    if alerts:

        alert_message = ""

        for alert in alerts:

            severity = alert["severity"]

            label = alert["label"]

            alert_message += f"{severity}: {label}\n"

            if severity == "CRITICAL":

                st.error(label)

            elif severity == "WARNING":

                st.warning(label)

            else:

                st.info(label)

    else:

        st.success("No Critical Weather Alerts")

    # ==================================================
    # SEND EMAIL ALERT
    # ==================================================

    if alerts:

        try:

            subject = f"Weather Alert for {city}"

            body = f"""
Hello {name},

Weather Alerts for {city}

{alert_message}

Stay Safe.

Weather Forecast Application
"""

            send_email(
                email,
                subject,
                body
            )

            st.success(
                "Weather Alert Email Sent Successfully"
            )

        except Exception as e:

            st.error(
                f"Email Notification Error: {e}"
            )

    else:

        st.info(
            "No alerts generated, email not sent"
        )

    # ==================================================
    # SAVE WEATHER DATA
    # ==================================================

    st.info("Saving Weather Data...")

    for i in range(24):

        cur.execute("""
        INSERT INTO weather_hourly(
            location_id,
            ts,
            temp_c,
            humidity,
            wind_ms,
            precip_prob
        )
        VALUES(?,?,?,?,?,?)
        """, (

            location_id,

            hourly_data["time"][i],

            hourly_data["temperature_2m"][i],

            hourly_data["relative_humidity_2m"][i],

            hourly_data["wind_speed_10m"][i],

            hourly_data["precipitation_probability"][i]
        ))

    for i in range(len(daily_data["time"])):

        cur.execute("""
        INSERT INTO weather_daily(
            location_id,
            date,
            tmax_c,
            tmin_c,
            rain_mm,
            uv_max
        )
        VALUES(?,?,?,?,?,?)
        """, (

            location_id,

            daily_data["time"][i],

            daily_data["temperature_2m_max"][i],

            daily_data["temperature_2m_min"][i],

            daily_data["precipitation_sum"][i],

            daily_data["uv_index_max"][i]
        ))

    con.commit()

    con.close()

    st.success("Weather Data Saved Successfully")