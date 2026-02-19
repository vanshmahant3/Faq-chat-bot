"""
synonym_matcher.py — Synonym-aware keyword matching.
Expands user query tokens using a synonym dictionary so that semantically
similar queries (e.g., "fees", "tuition", "payment") map to the same FAQ.
"""

from __future__ import annotations


from faq_data import FAQS, SYNONYM_DICT
from preprocessor import preprocess


def expand_with_synonyms(tokens: list[str]) -> list[str]:
    """
    Expand each token to its canonical form using the synonym dictionary.
    Returns a new list with both original and canonical tokens (deduplicated).
    """
    expanded = set(tokens)
    for token in tokens:
        canonical = SYNONYM_DICT.get(token)
        if canonical:
            expanded.add(canonical)
    return list(expanded)


def keyword_match_score(query_tokens: list[str], faq: dict) -> float:
    """
    Compute a matching score between expanded query tokens and FAQ keywords.
    Returns a score between 0.0 and 1.0.
    """
    faq_keywords = set(k.lower() for k in faq["keywords"])
    query_set = set(query_tokens)
    if not faq_keywords:
        return 0.0
    intersection = query_set & faq_keywords
    # Jaccard-like score weighted toward FAQ coverage
    score = len(intersection) / len(faq_keywords)
    return min(score, 1.0)


def synonym_match(query: str) -> tuple[dict | None, float]:
    """
    Match a user query to the best FAQ using synonym-expanded keyword matching.
    Returns (best_faq, confidence_score) or (None, 0.0) if no match.
    """
    tokens = preprocess(query)
    expanded = expand_with_synonyms(tokens)

    best_faq = None
    best_score = 0.0

    for faq in FAQS:
        score = keyword_match_score(expanded, faq)
        if score > best_score:
            best_score = score
            best_faq = faq

    return best_faq, best_score
