# 📄 Automated Resume Screening System (ATS)

## 🚀 Project Overview

The **Automated Resume Screening System** is an intelligent ATS (Applicant Tracking System) built using **Python, NLP, and Streamlit** that automates resume evaluation by matching candidate resumes with job descriptions.

It simulates a real-world ATS used in companies to shortlist candidates based on:

- Skills
- Experience
- Semantic similarity
- Job requirements

---

## 🎯 Problem Statement

HR teams receive hundreds of resumes for a single job role. Manual screening is:

- ⏳ Time-consuming
- ❌ Error-prone
- 🧠 Subjective

This project solves the problem by automating resume screening using NLP and scoring algorithms.

---

## 💡 Key Features

### 📤 Resume Processing

- Upload resumes in **PDF, DOCX, TXT**
- Automatic text extraction
- Resume storage and management system

### 🧠 NLP Features

- Skill extraction using NLP
- Fuzzy skill matching
- Semantic similarity using embeddings

### 📊 Ranking Engine

- Weighted scoring system:
  - 50% Semantic similarity
  - 30% Skill match
  - 20% Experience score
- Gap penalty for missing skills
- Supports **0-year experience (freshers included)**

### 📂 Candidate Management

- Upload and manage resumes
- Include / remove candidates
- Resume pool dashboard

### 📉 Analysis

- Selected vs Rejected candidates
- Missing skills detection
- Experience gap analysis
- Explainable results

### 📥 Export

- Download ATS report as CSV

---

## 🧰 Tech Stack

| Category        | Tools                     |
| --------------- | ------------------------- |
| Language        | Python 3.10+              |
| UI              | Streamlit                 |
| NLP             | SentenceTransformers      |
| Data Processing | Pandas, NumPy             |
| File Parsing    | pdfplumber, python-docx   |
| Database        | SQLite                    |
| ML Techniques   | TF-IDF, Cosine Similarity |

---

## 🏗️ System Architecture

```text
Resume Upload
↓
Text Extraction (PDF/DOCX/TXT)
↓
NLP Processing (Skills + Experience)
↓
Job Description Parsing
↓
Feature Engineering
↓
Ranking Engine
↓
Selection / Rejection Analysis
↓
Streamlit Dashboard Output

```

---

## 📁 Project Structure

```text
Automated-Resume-Screening-Tool/
│
├── db/
│ ├── screening.db
│ └── schema.sql
│
├── resumes/
│ ├── sample resumes (.pdf/.docx/.txt)
│
├── src/
│ ├── extract.py
│ ├── ingest.py
│ └── rank.py
| └── features.py
│
├── dashboard/
│ └── streamlit_app.py
│
├── main.py
├── requirements.txt
└── README.md
```

# Install Dependencies

pip install -r requirements.txt

# Run Application

python main.py

streamlit run dashboard/streamlit_app.py

# 🖼️ Sample Output
