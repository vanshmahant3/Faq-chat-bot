"""
entity_extractor.py — Regex-based entity extraction.
Extracts dates, course codes, and semester/year numbers from student queries.
"""

import re


# ── Ordinal / word-to-number mapping ─────────────────────────────────────────
WORD_TO_NUM = {
    "first": "1", "second": "2", "third": "3", "fourth": "4",
    "fifth": "5", "sixth": "6", "seventh": "7", "eighth": "8",
    "1st": "1", "2nd": "2", "3rd": "3", "4th": "4",
    "5th": "5", "6th": "6", "7th": "7", "8th": "8",
}

MONTH_NAMES = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec"
]


def extract_entities(text: str) -> dict:
    """
    Extract structured entities from a student query.
    Returns a dict with optional keys: 'dates', 'course_codes', 'semester', 'year'.
    """
    entities = {}
    lower = text.lower().strip()

    # ── Dates ─────────────────────────────────────────────────────────────
    dates = []

    # DD/MM/YYYY or DD-MM-YYYY
    dates += re.findall(r'\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b', text)

    # "Month YYYY" or "Month DD, YYYY"
    month_pattern = "|".join(MONTH_NAMES)
    dates += re.findall(
        rf'\b({month_pattern})\s+\d{{1,2}}(?:,?\s+\d{{4}})?\b', lower
    )
    dates += re.findall(
        rf'\b({month_pattern})\s+\d{{4}}\b', lower
    )

    if dates:
        entities["dates"] = list(set(dates))

    # ── Course codes (e.g., CS101, ME302, IT-201) ─────────────────────────
    course_codes = re.findall(r'\b[A-Za-z]{2,4}[\-]?\d{2,4}\b', text)
    # Filter out things that look like pure numbers or dates
    course_codes = [
        c.upper() for c in course_codes
        if not re.match(r'^\d+$', c) and not re.match(r'\d{1,2}[/\-]\d', c)
    ]
    if course_codes:
        entities["course_codes"] = list(set(course_codes))

    # ── Semester numbers ──────────────────────────────────────────────────
    # "SEM 5", "semester 3", "sem-5"
    sem_match = re.findall(r'\bsem(?:ester)?[\s\-]*(\d)\b', lower)
    if sem_match:
        entities["semester"] = sem_match[0]

    # ── Year references ───────────────────────────────────────────────────
    # "third year", "2nd year", "year 3"
    for word, num in WORD_TO_NUM.items():
        if re.search(rf'\b{word}\s*year\b', lower):
            entities["year"] = num
            break

    year_num = re.findall(r'\byear\s*(\d)\b', lower)
    if year_num and "year" not in entities:
        entities["year"] = year_num[0]

    return entities
