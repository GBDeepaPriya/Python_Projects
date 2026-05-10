from pathlib import Path
import re, json, sqlite3
from docx import Document
from pdfminer.high_level import extract_text

def read_text(path: str) -> str:
    p = Path(path)

    if p.suffix.lower() == ".pdf":
        txt = extract_text(path)

    elif p.suffix.lower() == ".docx":
        doc = Document(path)
        txt = "\n".join([para.text for para in doc.paragraphs])

    else:
        txt = Path(path).read_text(encoding="utf-8")

    return re.sub(r'\s+', ' ', txt).strip()


def save_resume(db, candidate_id, raw_text, parsed):
    con = sqlite3.connect(db)

    con.execute("""
    INSERT OR REPLACE INTO resumes(candidate_id, source, raw_text, parsed_json, updated_at)
    VALUES (?, ?, ?, ?, datetime('now'))
    """, (candidate_id, "pdf", raw_text, json.dumps(parsed)))

    con.commit()
    con.close()