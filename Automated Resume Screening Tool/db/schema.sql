-- =========================
-- JOBS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    title TEXT,
    jd_text TEXT,
    must_have TEXT,
    nice_to_have TEXT,
    min_exp_years REAL,
    location TEXT
);

-- =========================
-- CANDIDATES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS candidates (
    id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT,
    location TEXT
);

-- =========================
-- RESUMES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS resumes (
    candidate_id TEXT PRIMARY KEY,
    source TEXT,
    raw_text TEXT,
    parsed_json TEXT,
    updated_at TEXT
);

-- =========================
-- FEATURES TABLE
-- =========================
CREATE TABLE IF NOT EXISTS features (
    candidate_id TEXT,
    job_id TEXT,
    sim_embedding REAL,
    rule_musthave_hits INT,
    rule_musthave_total INT,
    years_exp REAL,
    gap_penalty REAL,
    PRIMARY KEY(candidate_id, job_id)
);

-- =========================
-- RANKINGS TABLE
-- =========================
CREATE TABLE IF NOT EXISTS rankings (
    job_id TEXT,
    candidate_id TEXT,
    score REAL,
    reasons TEXT,
    created_at TEXT,
    PRIMARY KEY(job_id, candidate_id)
);