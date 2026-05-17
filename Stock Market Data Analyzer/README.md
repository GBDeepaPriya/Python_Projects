# 📈 Stock Market Analyzer

A Stock Market Analysis & Backtesting System built using Python, Streamlit, SQLite, and modular financial analytics components.

It provides multi-stock comparison, technical indicators, backtesting, alerts, API access, and an interactive dashboard.

---

# 📁 Project Structure
```text
Stock-Market-Analyzer/

├── api/
│ └── app.py # API layer (data endpoints)

├── db/
│ ├── market.db # SQLite database (OHLC + indicators)
│ └── schema.sql # Database schema

├── jobs/
│ └── alerts.py # Alert system (price/indicator alerts)

├── src/
│ ├── ingest.py # Data ingestion pipeline
│ ├── indicators.py # Technical indicators (SMA, RSI)
│ ├── backtest.py # Strategy backtesting engine
│ ├── reports.py # Report generation

├── dashboard/
│ └── streamlit_app.py # Streamlit dashboard UI

├── outputs/ # Generated reports & exports

├── main.py # Entry point script

├── requirements.txt # Dependencies

├── README.md # Documentation
```
---

# 🚀 Features

## 📊 Dashboard

- Multi-stock comparison (normalized & actual prices)
- Candlestick / Line / Area charts
- RSI and Volume analysis
- SMA20 / SMA50 overlays
- Returns distribution & volatility analysis

## 🧠 Technical Indicators

- SMA (20, 50)
- RSI (14)
- Volume trends
- Rolling statistics

## 💰 Backtesting Engine

- SMA-based trading strategy
- Buy/Sell simulation
- Performance metrics:
  - Total Return
  - Sharpe Ratio
  - Max Drawdown

## 🗄️ Database

- candles_daily (OHLCV data)
- indicators_daily (SMA, RSI)
- SQLite-based structured storage

---

## Install Dependencies

pip install -r requirements.txt

---

## Run Dashboard

python main.py

streamlit run dashboard/streamlit_app.py

---

## Run API (optional)

python api/app.py

---

# 📊 System Flow

Data Source → ingest.py → SQLite DB  
 ↓  
indicators.py (SMA, RSI)  
 ↓  
dashboard (Streamlit UI)  
 ↓  
Visualization + Backtesting

---

# 🧠 Tech Stack

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- FastAPI / Flask (API layer)
- NumPy

---

# 📌 Future Improvements

- Live market data integration (Yahoo Finance)
- AI-based stock prediction
- Portfolio optimization (Markowitz model)
- Correlation heatmaps
- Real-time streaming dashboard
- AI trading assistant

---

# Sample Outputs
<img width="1822" height="480" alt="Dashboard1" src="https://github.com/user-attachments/assets/43a60888-0f7a-448d-9109-bdb4c9122343" />
<img width="1447" height="692" alt="Dashboard2" src="https://github.com/user-attachments/assets/5b63d096-6597-4f5a-baf4-855bae0539c1" />
<img width="1477" height="482" alt="Dashboard3" src="https://github.com/user-attachments/assets/4d8064ee-92cc-4fc7-bede-82fb61ddab76" />
<img width="1457" height="627" alt="Dashboard4" src="https://github.com/user-attachments/assets/099aa0b7-0b34-4c85-9b4e-dc0bcdb1099a" />
<img width="1502" height="527" alt="Dashboard5" src="https://github.com/user-attachments/assets/f3c9d938-af29-428d-ba41-d6e6feae3aa6" />
<img width="1497" height="405" alt="Dashboard6" src="https://github.com/user-attachments/assets/5d58b8be-f74e-451d-80f9-d9123efec102" />
<img width="1505" height="426" alt="Dashboard7" src="https://github.com/user-attachments/assets/cdddc6da-da48-48a6-8448-3c86ea0bb7bf" />
<img width="1437" height="562" alt="Dashboard8" src="https://github.com/user-attachments/assets/30aec5d0-674a-4829-aa76-e7d6b953fed4" />



