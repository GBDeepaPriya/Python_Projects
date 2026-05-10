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
<img width="1782" height="490" alt="Dashboard1" src="https://github.com/user-attachments/assets/d9c02a0a-786f-40c2-ae46-5abe7b40dae6" />
<img width="1767" height="691" alt="Dashboard2" src="https://github.com/user-attachments/assets/1e813b5f-2a87-428a-83d2-b9e29834377d" />
<img width="1772" height="447" alt="Dashboard3" src="https://github.com/user-attachments/assets/83510a77-33fa-4acc-a95d-3e07aa8dd12c" />
<img width="1787" height="787" alt="Dashboard4" src="https://github.com/user-attachments/assets/c201e3f2-26c8-4cad-81f5-ed780158cd66" />
<img width="1823" height="792" alt="Dashboard5" src="https://github.com/user-attachments/assets/620286a3-7c37-4649-b55a-75abfa80a141" />
<img width="1800" height="447" alt="Dashboard6" src="https://github.com/user-attachments/assets/189e721b-8710-4ba3-9a89-6e95d148ceea" />
<img width="1756" height="675" alt="Dashboard7" src="https://github.com/user-attachments/assets/87ee5757-e6f5-4ba9-aa24-8c3eabda13b2" />


