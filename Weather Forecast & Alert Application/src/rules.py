def evaluate(hourly_data, daily_data):

    alerts = []

    # ==========================================
    # NEXT 12 HOURS ONLY
    # ==========================================

    rain_probs = hourly_data[
        "precipitation_probability"
    ][:12]

    wind_gusts = hourly_data[
        "wind_gusts_10m"
    ][:12]

    temps = daily_data[
        "temperature_2m_max"
    ][:3]

    uv_values = daily_data[
        "uv_index_max"
    ][:3]

    # ==========================================
    # RAIN ALERT
    # ==========================================

    max_rain = max(rain_probs)

    if max_rain >= 80:

        alerts.append({

            "severity": "WARNING",

            "label":
            f"Heavy rain likely in next 12 hours ({max_rain}%)"
        })

    elif max_rain >= 60:

        alerts.append({

            "severity": "INFO",

            "label":
            f"Possible rain expected ({max_rain}%)"
        })

    # ==========================================
    # HEAT ALERT
    # ==========================================

    max_temp = max(temps)

    if max_temp >= 42:

        alerts.append({

            "severity": "CRITICAL",

            "label":
            f"Extreme heatwave expected ({max_temp}°C)"
        })

    elif max_temp >= 38:

        alerts.append({

            "severity": "WARNING",

            "label":
            f"High temperature expected ({max_temp}°C)"
        })

    # ==========================================
    # WIND ALERT
    # ==========================================

    max_wind = max(wind_gusts)

    # realistic thresholds
    if max_wind >= 60:

        alerts.append({

            "severity": "CRITICAL",

            "label":
            f"Dangerous storm winds expected ({max_wind} km/h)"
        })

    elif max_wind >= 40:

        alerts.append({

            "severity": "WARNING",

            "label":
            f"Strong winds expected ({max_wind} km/h)"
        })

    # ==========================================
    # UV ALERT
    # ==========================================

    max_uv = max(uv_values)

    if max_uv >= 11:

        alerts.append({

            "severity": "CRITICAL",

            "label":
            f"Extreme UV radiation expected (UV {max_uv})"
        })

    elif max_uv >= 8:

        alerts.append({

            "severity": "WARNING",

            "label":
            f"High UV radiation expected (UV {max_uv})"
        })

    return alerts