# 🌦 Weather Forecast & Email Alert Application

A real-time Weather Forecast & Smart Email Alert System built using Python, Streamlit, SQLite, and Open-Meteo API.

This application fetches live weather data based on user-entered city names, visualizes forecasts using interactive charts, generates smart weather alerts, and sends automated email notifications.

---

# 🚀 Features

✅ Real-Time Weather Forecast  
✅ Auto Location Detection using City Name  
✅ Smart Weather Alert System  
✅ Automated Email Notifications  
✅ Interactive Streamlit Dashboard  
✅ SQLite Database Integration  
✅ 24-Hour Weather Forecast  
✅ 7-Day Forecast Analysis  
✅ Rain Probability Monitoring  
✅ Wind Speed Monitoring  
✅ UV Index Monitoring  
✅ Interactive Plotly Charts  
✅ Modular Python Architecture

---

# 🛠 Tech Stack

## Frontend

- Streamlit
- Plotly

## Backend

- Python
- SQLite

## APIs

- Open-Meteo API
- OpenStreetMap Geocoding API

## Libraries

- streamlit
- pandas
- plotly
- requests
- sqlite3
- smtplib
- python-dotenv

---

# 📂 Project Structure

```text
Weather Forecast & Alert Application/

│── dashboard/
│   └── streamlit_app.py

│── notify/
│   └── email_alert.py

│── src/
│   ├── ingest.py
│   ├── rules.py
│   ├── setup_db.py
│   └── utils.py

│── db/
│   └── weather.db

│── .env
│── requirements.txt
│── README.md
│── main.py
```

---

# ⚙️ Application Workflow

```text
User Inputs City Name
        ↓
Auto Detect Coordinates
        ↓
Fetch Weather Forecast
        ↓
Analyze Weather Conditions
        ↓
Generate Smart Alerts
        ↓
Display Interactive Charts
        ↓
Send Email Notifications
        ↓
Store Data in SQLite Database
```

---

# 🌍 Weather API Used

## Open-Meteo API

Free weather forecasting API:
https://open-meteo.com/

### Features Used

- Current Weather
- Hourly Forecast
- Daily Forecast
- UV Index
- Rain Probability
- Wind Speed

---

# 📧 Email Notification System

The application automatically sends weather alert emails to users.

## Example Alerts

- Heavy Rain Warning
- High Temperature Alert
- Strong Wind Warning
- High UV Radiation Alert

---

# 🧠 Smart Alert Engine

The alert engine intelligently evaluates:

- Rain Probability
- Wind Speed
- Temperature
- UV Index

and generates meaningful alerts based on thresholds.

---

# 📊 Dashboard Features

## Current Weather

- Temperature
- Wind Speed
- Weather Code

## Forecast Charts

- 24-Hour Temperature Forecast
- Rain Probability Forecast
- Wind Speed Forecast
- 7-Day Temperature Forecast

---

# 🗄 Database Tables

## users

Stores user information.

## locations

Stores location details.

## weather_hourly

Stores hourly forecast data.

## weather_daily

Stores daily forecast data.

## alerts

Stores generated alerts.

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

## .env

```env
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
```

---

# 🔑 Gmail Setup

## Step 1 — Enable 2-Step Verification

https://myaccount.google.com/security

## Step 2 — Generate App Password

https://myaccount.google.com/apppasswords

Use generated password inside `.env`

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Setup Database

Run:

```bash
python main.py
```

Expected Output:

```text
Database Created Successfully
```

---

# ▶️ Run Streamlit Application

```bash
streamlit run dashboard/streamlit_app.py
```

---

# 🌐 Streamlit URL

```text
http://localhost:8501
```

---

# 📸 Screenshots

## Dashboard
- Current Weather
- Temperature Forecast
- Rain Forecast
- Wind Forecast
<img width="1527" height="758" alt="Dashboard1" src="https://github.com/user-attachments/assets/c51885ee-4941-4aa5-a7d2-20ea8413edb9" />
<img width="1781" height="716" alt="Dashboard2" src="https://github.com/user-attachments/assets/4b23b452-9981-48db-9fa8-009f75ee78dc" />
<img width="1817" height="698" alt="Dashboard3" src="https://github.com/user-attachments/assets/896aac86-7cf9-44b3-9907-d06af1923c8b" />
<img width="1817" height="633" alt="Dashboard4" src="https://github.com/user-attachments/assets/427f3b81-0887-4898-8b86-238f876d1a39" />
<img width="1212" height="722" alt="Dashboard5" src="https://github.com/user-attachments/assets/03811bd1-441e-44e9-9e7d-eb6a56ba45d4" />
<img width="1340" height="632" alt="Dashboard6" src="https://github.com/user-attachments/assets/09d1a37a-8b7e-419a-80d0-e57261ee3a8a" />

## Email Alerts

- Automated Weather Warning Emails
<img width="1255" height="488" alt="Email Alert 1" src="https://github.com/user-attachments/assets/41ed2373-01bc-4a1d-bb98-5a4621c93ea1" />
<img width="1237" height="498" alt="Email Alert 2" src="https://github.com/user-attachments/assets/80d4cdbf-25a3-4ab5-9fbd-b2fced8429fe" />

---

# 📚 Learning Outcomes

This project demonstrates:

- Python Development
- API Integration
- Email Automation
- Database Management
- Real-Time Data Processing
- Data Visualization
- Dashboard Development
- Alert System Design

---

# 💼 Use Cases

- Weather Monitoring
- Travel Planning
- Agriculture Support
- Outdoor Event Planning
- Smart City Applications
- Disaster Preparedness

---

# 🎯 Skills Demonstrated

## Python Skills

- Modular Programming
- Exception Handling
- API Handling

## Backend Skills

- SQLite Database
- SMTP Email Integration

## Visualization Skills

- Plotly Interactive Charts
- Streamlit Dashboards

## Automation Skills

- Automated Email Alerts
- Smart Alert Generation

---

# 👨‍💻 Author

Deepika

---
