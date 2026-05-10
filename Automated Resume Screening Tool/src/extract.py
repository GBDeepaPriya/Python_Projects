import re
import json
from rapidfuzz import process, fuzz

SKILLS = [
    "python","sql","pandas","numpy","scikit-learn","tensorflow","pytorch",
    "aws","azure","gcp","react","node","django","flask","docker",
    "kubernetes","java","c++","git","linux","power bi","excel"
]

def fuzzy_skills(text):
    tokens = set(re.findall(r"[a-zA-Z\+\#\.]{2,}", text.lower()))
    found = set()

    for t in tokens:
        match = process.extractOne(t, SKILLS, scorer=fuzz.token_sort_ratio)
        if match and match[1] > 85:
            found.add(match[0])

    return list(found)


def extract_years(text):
    matches = re.findall(r'(\d+(?:\.\d+)?)\s*(years|yrs|y)', text.lower())
    if not matches:
        return 0
    return max([float(m[0]) for m in matches])


def parse_resume(text):
    return {
        "skills": fuzzy_skills(text),
        "years_exp": extract_years(text)
    }