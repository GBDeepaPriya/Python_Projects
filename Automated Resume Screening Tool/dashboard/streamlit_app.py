import streamlit as st
import pandas as pd
import sqlite3
import uuid
import os
import sys
import json
import pdfplumber
from docx import Document

# FIX PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.extract import parse_resume
from src.ingest import save_resume
from src.rank import rank_job


DB = "db/screening.db"
RESUME_FOLDER = "resumes"


# -------------------------
# SETUP
# -------------------------
st.set_page_config(page_title="AI ATS System", layout="wide")

st.title("📄 Automated Resume Screening Tool")
st.markdown("Upload, manage, and rank resumes like a real ATS")


# -------------------------
# SESSION STORAGE (SELECTED RESUMES)
# -------------------------
if "selected_resumes" not in st.session_state:
    st.session_state["selected_resumes"] = set()


# -------------------------
# FILE READER (PDF / DOCX / TXT)
# -------------------------
def read_file(path, file_type):

    if file_type == "pdf":
        with pdfplumber.open(path) as pdf:
            return "".join([page.extract_text() or "" for page in pdf.pages])

    elif file_type == "docx":
        doc = Document(path)
        return "\n".join([p.text for p in doc.paragraphs])

    elif file_type == "txt":
        return open(path, "r", encoding="utf-8").read()

    return ""

def evaluate_candidate(skills, exp, must_have, min_exp):

    missing = [s for s in must_have if s not in skills]

    exp_ok = exp >= min_exp

    if len(missing) == 0 and exp_ok:
        return "SELECTED", missing, exp_ok

    return "REJECTED", missing, exp_ok

# -------------------------
# JOB DESCRIPTION
# -------------------------
st.header("📌 Job Description")

job_title = st.text_input("Job Title")
job_desc = st.text_area("Enter Job Description")
must_have = st.text_input("Must-have skills (comma separated)")

must_have_list = [s.strip().lower() for s in must_have.split(",") if s.strip()]

min_exp_years = st.number_input(
    "Minimum Experience Required (Years)",
    min_value=0.0,
    max_value=30.0,
    value=2.0,
    step=0.5
)
if st.button("Create Job"):

    job_id = str(uuid.uuid4())

    con = sqlite3.connect(DB)
    con.execute("""
    INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
        job_id,
        job_title,
        job_desc,
        json.dumps(must_have_list),
        json.dumps([]),
        min_exp_years,   # ✅ NEW FIELD
        "India"
    ))
    con.commit()
    con.close()

    st.session_state["job_id"] = job_id
    st.session_state["min_exp"] = min_exp_years

    st.success(f"✅ Job Created: {job_id}")


# -------------------------
# UPLOAD RESUMES (MULTI FORMAT)
# -------------------------
st.header("📤 Upload Resumes (PDF / DOCX / TXT)")

uploaded_files = st.file_uploader(
    "Upload Resumes",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)

parsed_resumes = {}

if uploaded_files:

    for file in uploaded_files:

        file_path = os.path.join(RESUME_FOLDER, file.name)

        with open(file_path, "wb") as f:
            f.write(file.getbuffer())

        ext = file.name.split(".")[-1].lower()
        text = read_file(file_path, ext)

        parsed = parse_resume(text)

        parsed_resumes[file.name] = {
            "text": text,
            "skills": parsed.get("skills", []),
            "exp": parsed.get("years_exp", 0),
            "selected": True
        }

        st.success(f"Uploaded: {file.name}")


# -------------------------
# SHOW ALL RESUMES (MANAGEMENT PANEL)
# -------------------------
st.header("📂 Resume Pool (Manage Candidates)")

all_files = os.listdir(RESUME_FOLDER)

for file in all_files:

    file_path = os.path.join(RESUME_FOLDER, file)
    ext = file.split(".")[-1]

    st.write(f"📄 {file}")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(f"Preview {file}"):
            text = read_file(file_path, ext)
            st.text_area("Resume Content", text, height=150)

    with col2:
        if st.button(f"Include {file}"):
            st.session_state["selected_resumes"].add(file)
            st.success(f"Included {file}")

    with col3:
        if st.button(f"Remove {file}"):
            try:
                os.remove(file_path)
                st.session_state["selected_resumes"].discard(file)
                st.warning(f"Deleted {file}")
            except:
                st.error("Delete failed")


# -------------------------
# RUN RANKING (ONLY SELECTED)
# -------------------------
# -------------------------
# RUN RANKING (ONLY SELECTED)
# -------------------------
st.header("⚙️ Screening Engine")

if st.button("Run Ranking"):

    if "job_id" not in st.session_state:
        st.error("⚠️ Create job first")
        st.stop()

    selected = list(st.session_state["selected_resumes"])

    if len(selected) == 0:
        st.error("⚠️ No resumes selected")
        st.stop()

    job_id = st.session_state["job_id"]

    # STEP 1: ensure DB is updated
    for file in selected:
        file_path = os.path.join(RESUME_FOLDER, file)
        ext = file.split(".")[-1]

        text = read_file(file_path, ext)
        parsed = parse_resume(text)

        save_resume(DB, file, text, parsed)

    # STEP 2: run ranking
    rank_job(DB, job_id)

    # STEP 3: fetch job details
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    job = con.execute("""
        SELECT must_have, min_exp_years
        FROM jobs
        WHERE id=?
    """, (job_id,)).fetchone()

    must_have_list = json.loads(job["must_have"])
    min_exp = job["min_exp_years"]

    # STEP 4: fetch ranking
    rows = con.execute("""
        SELECT candidate_id, score
        FROM rankings
        WHERE job_id=?
        ORDER BY score DESC
    """, (job_id,)).fetchall()

    df = pd.DataFrame(rows, columns=["candidate_id", "score"])

    df = df[df["candidate_id"].isin(selected)]

    st.subheader("🏆 Final Ranking")
    st.dataframe(df)

    # -------------------------
    # REJECTION + SELECTION ANALYSIS
    # -------------------------
    st.subheader("📊 Selection & Rejection Analysis")

    for file in selected:

        file_path = os.path.join(RESUME_FOLDER, file)
        ext = file.split(".")[-1]

        text = read_file(file_path, ext)
        parsed = parse_resume(text)

        skills = parsed.get("skills", [])
        exp = parsed.get("years_exp", 0)

        status, missing, exp_ok = evaluate_candidate(
            skills, exp, must_have_list, min_exp
        )

        st.markdown(f"### 📄 {file}")

        if status == "SELECTED":
            st.success(f"✅ SELECTED")

        else:
            st.error(f"❌ REJECTED")

        st.write("📌 Experience:", exp, "Years")
        st.write("📌 Required Experience:", min_exp)

        if missing:
            st.write("❌ Missing Skills:", missing)
        else:
            st.write("✔ All required skills matched")

        if not exp_ok:
            st.write("❌ Experience not sufficient")
        else:
            st.write("✔ Experience meets requirement")