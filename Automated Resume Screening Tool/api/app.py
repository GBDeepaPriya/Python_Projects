from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3, uuid, json

from src.ingest import read_text, save_resume
from src.extract import parse_resume
from src.rank import rank_job

app = FastAPI()
DB = "db/screening.db"


class Job(BaseModel):
    title: str
    jd_text: str
    must_have: list[str] = []
    min_exp_years: float = 2


@app.post("/job")
def create_job(job: Job):

    jid = str(uuid.uuid4())
    con = sqlite3.connect(DB)

    con.execute("""
    INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, NULL)
    """, (
        jid, job.title, job.jd_text,
        json.dumps(job.must_have),
        json.dumps([]),
        job.min_exp_years
    ))

    con.commit()
    con.close()

    return {"job_id": jid}


@app.post("/rank/{job_id}")
def rank(job_id: str):
    rank_job(DB, job_id)

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    data = con.execute("""
    SELECT * FROM rankings WHERE job_id=? ORDER BY score DESC
    """, (job_id,)).fetchall()

    return [dict(d) for d in data]