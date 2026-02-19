"""
intent_classifier.py — Keyword-based intent classifier.
Routes student queries to one of 7 intent buckets:
  admissions, exams, timetable, hostel, scholarships, facilities, general
"""

from preprocessor import preprocess

# ── Intent keyword definitions ────────────────────────────────────────────────
INTENT_KEYWORDS = {
    "admissions": [
        "admission", "admissions", "apply", "application", "enroll",
        "registration", "join", "intake", "eligibility", "entrance",
        "cutoff", "merit", "counseling", "form"
    ],
    "exams": [
        "exam", "examination", "test", "assessment", "paper",
        "datesheet", "result", "marks", "grade", "semester",
        "internal", "external", "midterm", "final", "backlog",
        "revaluation", "supplementary"
    ],
    "timetable": [
        "timetable", "schedule", "class", "lecture", "period",
        "routine", "slot", "calendar"
    ],
    "hostel": [
        "hostel", "accommodation", "room", "mess", "dormitory",
        "stay", "residence", "boarding", "warden", "curfew"
    ],
    "scholarships": [
        "scholarship", "financial", "aid", "merit", "concession",
        "waiver", "bursary", "grant", "stipend", "freeships"
    ],
    "facilities": [
        "library", "book", "sports", "gym", "ground", "fitness",
        "placement", "job", "recruit", "career", "bus", "transport",
        "shuttle", "wifi", "internet", "canteen", "food", "cafeteria",
        "lab", "computer", "pool", "swimming"
    ],
    "general": [
        "timings", "timing", "hours", "contact", "phone", "email",
        "address", "office", "ragging", "bully", "harassment",
        "principal", "dean", "faculty", "department", "fees",
        "tuition", "payment", "cost"
    ]
}


def classify_intent(query: str) -> tuple[str, float]:
    """
    Classify the intent of a query using weighted keyword matching.
    Returns (intent_label, confidence_score).
    """
    tokens = preprocess(query)
    token_set = set(tokens)

    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        keyword_set = set(keywords)
        matched = token_set & keyword_set
        if keyword_set:
            scores[intent] = len(matched) / len(keyword_set) * 10  # boost raw count
        else:
            scores[intent] = 0.0

    if not scores or max(scores.values()) == 0:
        return "general", 0.0

    best_intent = max(scores, key=scores.get)
    # Normalize confidence to 0-1 range
    total = sum(scores.values())
    confidence = scores[best_intent] / total if total > 0 else 0.0

    return best_intent, round(confidence, 3)
