import sqlite3, json, datetime as dt
from src.features import jd_resume_features   # ✅ FIXED IMPORT

def rank_job(db, job_id, min_req=2):

    con = sqlite3.connect(db)
    cur = con.cursor()

    candidates = cur.execute("SELECT candidate_id FROM resumes").fetchall()

    job = cur.execute("SELECT must_have FROM jobs WHERE id=?", (job_id,)).fetchone()
    must_total = len(json.loads(job[0]) if job[0] else [])

    results = []

    for (cid,) in candidates:

        f = jd_resume_features(db, job_id, cid)

        score = (
            0.55 * f["sim"] +
            0.35 * (f["must_hits"] / max(1, must_total)) +
            0.10 * min(1, f["years"] / min_req)
        )

        results.append((cid, score))

    results.sort(key=lambda x: x[1], reverse=True)

    for cid, score in results:
        cur.execute("""
        INSERT OR REPLACE INTO rankings(job_id, candidate_id, score, reasons, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (
            job_id,
            cid,
            score,
            json.dumps({"score": score}),
            dt.datetime.utcnow().isoformat()
        ))

    con.commit()
    con.close()