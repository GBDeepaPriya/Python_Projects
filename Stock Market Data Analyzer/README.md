# 📈 Stock Market Analyzer

A Stock Market Analysis & Backtesting System built using Python, Streamlit, SQLite, and modular financial analytics components.

It provides multi-stock comparison, technical indicators, backtesting, alerts, API access, and an interactive dashboard.

---

# 📁 Project Structure

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
