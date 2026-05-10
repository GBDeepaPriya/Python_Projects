import os
import sqlite3
import uuid
import json

from src.ingest import save_resume, read_text
from src.extract import parse_resume
from src.rank import rank_job


DB = "db/screening.db"
JOB_PATH = "data/job_description.txt"
RESUME_FOLDER = "resumes"


# -----------------------------
# INIT DATABASE
# -----------------------------
def init_db():
    con = sqlite3.connect(DB)
    with open("db/schema.sql", "r") as f:
        con.executescript(f.read())
    con.commit()
    con.close()
    print("✅ Database initialized")


# -----------------------------
# CREATE SAMPLE JOB
# -----------------------------
def create_sample_job():

    if not os.path.exists(JOB_PATH):
        print("⚠️ No Job Description found. Running in Resume-Only Mode.")
        return None

    con = sqlite3.connect(DB)
    job_id = str(uuid.uuid4())

    jd_text = open(JOB_PATH, "r", encoding="utf-8").read()

    must_have = ["python", "machine learning", "sql"]

    con.execute("""
    INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        job_id,
        "Data Scientist",
        jd_text,
        json.dumps(must_have),
        json.dumps(["communication"]),
        2,
        "India"
    ))

    con.commit()
    con.close()

    print(f"✅ Job Created: {job_id}")
    return job_id


# -----------------------------
# LOAD RESUMES FROM FOLDER
# -----------------------------
def load_resumes_from_folder(folder):

    resumes = {}

    for file in os.listdir(folder):
        path = os.path.join(folder, file)

        if os.path.isfile(path):

            try:
                text = read_text(path)   # PDF / DOCX / TXT handler
                candidate_id = os.path.splitext(file)[0]
                resumes[candidate_id] = text
                print(f"📄 Loaded: {file}")

            except Exception as e:
                print(f"❌ Error reading {file}: {e}")

    return resumes


# -----------------------------
# ADD RESUME TO DB
# -----------------------------
def add_resume(candidate_id, text):
    parsed = parse_resume(text)
    save_resume(DB, candidate_id, text, parsed)
    print(f"📄 Resume processed → {candidate_id}")


# -----------------------------
# FALLBACK SCORING (NO JD MODE)
# -----------------------------
def fallback_ranking():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    rows = cur.execute("SELECT candidate_id, parsed_json FROM resumes").fetchall()

    results = []

    for cid, parsed_json in rows:

        parsed = json.loads(parsed_json)

        score = (
            len(parsed.get("skills", [])) * 0.6 +
            parsed.get("years_exp", 0) * 0.4
        )

        results.append((cid, score))

    results.sort(key=lambda x: x[1], reverse=True)

    print("\n🏆 RESUME-ONLY RANKING (NO JD MODE)\n")

    for r in results:
        print(f"{r[0]} → Score: {round(r[1], 2)}")


# -----------------------------
# JD-BASED RANKING
# -----------------------------
def jd_ranking(job_id):
    print("📊 Running JD-based ranking...")
    rank_job(DB, job_id)
    print("✅ Ranking completed")


# -----------------------------
# SHOW RESULTS
# -----------------------------
def show_results(job_id):

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    rows = con.execute("""
    SELECT * FROM rankings
    WHERE job_id=?
    ORDER BY score DESC
    """, (job_id,)).fetchall()

    print("\n🏆 FINAL RANKING\n")

    for r in rows:
        print(f"{r['candidate_id']} → {round(r['score'], 3)}")


# -----------------------------
# MAIN PIPELINE
# -----------------------------
if __name__ == "__main__":

    print("\n🚀 Starting Automated Resume Screening Tool\n")

    # STEP 1: INIT DB
    init_db()

    # STEP 2: CREATE JOB
    job_id = create_sample_job()

    # STEP 3: LOAD RESUMES FROM FOLDER ⭐ UPDATED
    resumes = load_resumes_from_folder(RESUME_FOLDER)

    # STEP 4: PROCESS RESUMES
    for cid, text in resumes.items():
        add_resume(cid, text)

    # STEP 5: RUN PIPELINE
    if job_id:
        jd_ranking(job_id)
        show_results(job_id)
    else:
        fallback_ranking()

    print("\n✅ Pipeline Completed\n")