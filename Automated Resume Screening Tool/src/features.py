import sqlite3, json
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")


def jd_resume_features(db, job_id, candidate_id):

    con = sqlite3.connect(db)
    cur = con.cursor()

    jd = cur.execute("SELECT jd_text, must_have FROM jobs WHERE id=?", (job_id,)).fetchone()
    res = cur.execute("SELECT parsed_json FROM resumes WHERE candidate_id=?", (candidate_id,)).fetchone()

    con.close()

    jd_text = jd[0]
    must_have = json.loads(jd[1]) if jd[1] else []

    parsed = json.loads(res[0])

    resume_text = " ".join(parsed.get("skills", []))

    sim = float(util.cos_sim(model.encode(jd_text), model.encode(resume_text))[0][0])

    skills = set(parsed.get("skills", []))
    hits = sum(1 for s in must_have if s.lower() in skills)

    return {
        "sim": sim,
        "must_hits": hits,
        "must_total": len(must_have),
        "years": parsed.get("years_exp", 0)
    }