"""
preprocessor.py — Text preprocessing pipeline for student queries.
Handles lowercasing, tokenization, stopword removal, punctuation handling,
and basic spelling normalization.
"""

from __future__ import annotations


import re
import string

# ── Common English stopwords ──────────────────────────────────────────────────
STOPWORDS = {
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
    "your", "yours", "yourself", "yourselves", "he", "him", "his",
    "himself", "she", "her", "hers", "herself", "it", "its", "itself",
    "they", "them", "their", "theirs", "themselves", "what", "which",
    "who", "whom", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "having",
    "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if",
    "or", "because", "as", "until", "while", "of", "at", "by", "for",
    "with", "about", "against", "between", "through", "during", "before",
    "after", "above", "below", "to", "from", "up", "down", "in", "out",
    "on", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "both",
    "each", "few", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "s", "t",
    "can", "will", "just", "don", "should", "now", "d", "ll", "m", "o",
    "re", "ve", "y", "ain", "aren", "couldn", "didn", "doesn", "hadn",
    "hasn", "haven", "isn", "ma", "mightn", "mustn", "needn", "shan",
    "shouldn", "wasn", "weren", "won", "wouldn",
    "please", "tell", "know", "want", "need", "could", "would", "like"
}

# ── Spelling corrections dictionary ──────────────────────────────────────────
SPELLING_CORRECTIONS = {
    "addmission": "admission",
    "admision": "admission",
    "addmisions": "admissions",
    "admisons": "admissions",
    "scholership": "scholarship",
    "scholarshp": "scholarship",
    "scholerships": "scholarships",
    "hostle": "hostel",
    "hostl": "hostel",
    "libary": "library",
    "libraray": "library",
    "libray": "library",
    "tution": "tuition",
    "tution": "tuition",
    "tutoin": "tuition",
    "exams": "exam",
    "examinations": "examination",
    "schdeule": "schedule",
    "schdule": "schedule",
    "sechdule": "schedule",
    "timetabel": "timetable",
    "timtable": "timetable",
    "placment": "placement",
    "plcament": "placement",
    "conact": "contact",
    "cotact": "contact",
    "feees": "fees",
    "fess": "fees",
    "scolarship": "scholarship",
    "wify": "wifi",
    "wi-fi": "wifi",
    "cantin": "canteen",
    "cantten": "canteen",
    "ragin": "ragging",
    "raggin": "ragging",
    "spors": "sports",
    "transprt": "transport",
    "buss": "bus",
}


def preprocess(text: str) -> list[str]:
    """
    Full preprocessing pipeline:
    1. Lowercase
    2. Remove punctuation (keep hyphens in course-codes)
    3. Tokenize (split on whitespace)
    4. Spelling normalization
    5. Stopword removal
    Returns a list of cleaned tokens.
    """
    # 1. Lowercase
    text = text.lower().strip()

    # 2. Remove punctuation except hyphens (useful for course codes)
    text = re.sub(r"[^\w\s\-]", " ", text)

    # 3. Tokenize
    tokens = text.split()

    # 4. Spelling correction
    tokens = [SPELLING_CORRECTIONS.get(tok, tok) for tok in tokens]

    # 5. Remove stopwords
    tokens = [tok for tok in tokens if tok not in STOPWORDS and len(tok) > 1]

    return tokens


def preprocess_to_string(text: str) -> str:
    """Return preprocessed text as a single space-joined string."""
    return " ".join(preprocess(text))
