# 💰 Personal Expense Tracker Dashboard

## 📘 Project Overview

The **Personal Expense Tracker Dashboard** is a  financial management application designed to help users track, analyze, and visualize their income and expenses in real time.

It provides an interactive dashboard to monitor spending patterns, categorize transactions, and generate insights for better financial decision-making.

---

## 🏢 Industry Relevance

This project is highly relevant to:

- 🏦 FinTech Applications  
- 💳 Banking & Finance Analytics  
- 📱 Personal Budgeting Apps  
- 📊 Business Expense Management Systems  

### Real-world use cases:
- Personal finance tracking apps
- Banking dashboards
- Corporate expense monitoring systems
- Financial planning tools

---

## ✨ Features

### 📊 Dashboard
- Total expense tracking
- Monthly & daily spend summary
- Top spending category identification

### ➕ Transaction Management
- Add income and expenses
- Select category and account
- Real-time updates
s

### 🍩 Data Visualization
- Pie chart (category-wise spending)
- Line chart (daily trend)
- Bar chart (monthly trend)

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Data Processing | Pandas |
| Database | SQLite |
| Visualization | Matplotlib / Streamlit Charts |

---

## 📁 Folder Structure
```text
expense-tracker/
│
├── data/
│ └── sample_expenses.csv
│
├── db/
│ └── expenses.db
│
├── src/
│ ├── models.py
│ ├── ingest.py
│ ├── categorize.py
│ ├── analyze.py
│ ├── report.py
│ ├── plots.py
│ └── app_streamlit.py
| └── generate_sample_csv.py
| 
│── main.py
├── requirements.txt
└── README.md

```

# Install Dependencies
pip install -r requirements.txt

# Run Application
python main.py

streamlit run src/app_streamlit.py

# 📊 Sample Output

