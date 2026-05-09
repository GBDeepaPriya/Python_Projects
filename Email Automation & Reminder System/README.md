# 📧 Email Automation & Reminder System

A Python-based automation project built using **Streamlit, SQLite, and SMTP (Gmail)** that helps users automate email sending, schedule reminders, and manage contacts efficiently.

This project simulates real-world email automation systems used in HR, business operations, education, and productivity tools.

---

# 🚀 Project Overview

This system allows users to:

- Add and manage contacts
- Send bulk emails
- Schedule email reminders with date & time
- Automatically send emails when reminder time arrives
- Track sent and pending reminders
- View logs of system activity

The reminder engine runs in the background and continuously checks for due reminders and sends emails automatically.

---

# 🎯 Problem Statement

In real-world scenarios, people and companies often:

- Forget to send important emails
- Miss follow-ups and deadlines
- Manually track reminders
- Spend time on repetitive email tasks

This project solves these problems by automating email communication and reminders.

---

# 💡 Key Features

## 👥 Contact Management
- Add multiple contacts at once
- View all contacts
- Update contact details
- Delete contacts

## 📧 Bulk Email System
- Send emails to multiple recipients
- Personalized message support
- Success/failure tracking

## ⏰ Reminder System
- Schedule reminders using date & time
- Automatic email sending at scheduled time
- Background reminder engine (runs every 60 seconds)
- Status tracking: Pending / Sent

## ✏️ Reminder Management
- Create reminders
- Edit reminders (email, subject, time)
- Delete any reminder (pending or sent)

## 📊 Dashboard
- Total contacts
- Pending reminders
- Sent reminders
- Real-time data visualization

## 📜 Logging System
- Tracks email success and failure
- Engine execution logs
- Debugging support

---

# 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| Language | Python 3.x |
| UI Framework | Streamlit |
| Database | SQLite |
| Email Service | SMTP (Gmail) |
| Data Handling | Pandas |
| Scheduling | Threading + Time |
| Parsing | python-dateutil |

---

# 📁 Project Structure
```text
Email-Automation-Reminder-System/
│
├── dashboard/
│ └── app.py
│
├── src/
│ ├── db.py 
│ ├── mailer.py 
│ ├── logger.py 
| ├── config.py 
│
├── logs/
│ └── app.log 
│
├── data/
│ └── email.db 
│
├── main.py
├── requirements.txt
├── README.md
└── .env

```
-----
## Install Dependencies
pip install -r requirements.txt

## Run Application
streamlit run dashboard/app.py

## 🔐 Gmail SMTP Setup

To send emails, you must configure Gmail SMTP:

Steps:
Enable 2-Step Verification in Google Account

Generate App Password
Use credentials in mailer.py

EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"

-----

## 📌 How It Works
User Input (Contacts + Reminders)
        ↓
Stored in SQLite Database
        ↓
Background Engine (runs every 60 seconds)
        ↓
Checks Due Reminders
        ↓
Sends Email via SMTP
        ↓
Updates Status (Pending → Sent)
        ↓
Dashboard Updates in Real-Time

## 📊 Sample Input Format
Contacts
John Doe, john@gmail.com
Jane Smith, jane@gmail.com

Reminder Example
Email: test@gmail.com
Subject: Meeting Reminder
Time: 2026-05-09 18:30:00

## 👨‍💻 Learning Outcomes

This project demonstrates:

Email automation using SMTP
Streamlit web app development
Database management (SQLite)
Background task execution
Scheduling systems
CRUD operations in Python
Real-world automation system design

## Sample Outputs