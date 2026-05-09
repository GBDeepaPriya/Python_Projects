import httpx
import json
import datetime as dt
from src.database import get_connection

OPEN_METEO = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&hourly=temperature_2m,relative_humidity_2m,"
    "precipitation_probability,precipitation,"
    "wind_speed_10m,wind_gusts_10m,"
    "cloud_cover,uv_index,pressure_msl,visibility"
    "&daily=temperature_2m_max,temperature_2m_min,"
    "precipitation_sum,precipitation_probability_max,"
    "wind_speed_10m_max,uv_index_max,sunrise,sunset"
    "&current_weather=true&timezone={tz}"
)

def fetch_open_meteo(lat, lon, tz="Asia/Kolkata"):
    url = OPEN_METEO.format(lat=lat, lon=lon, tz=tz)

    with httpx.Client(timeout=20) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.json()

def persist_raw(location_id, payload):
    con = get_connection()

    con.execute("""
        INSERT INTO weather_raw
        (location_id, fetched_at, scope, provider, payload)
        VALUES (?, ?, ?, ?, ?)
    """, (
        location_id,
        dt.datetime.utcnow().isoformat(),
        "full",
        "open-meteo",
        json.dumps(payload)
    ))

    con.commit()
    con.close()