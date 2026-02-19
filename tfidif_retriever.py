"""
tfidf_retriever.py — TF-IDF based FAQ retrieval engine.
Builds TF-IDF vectors from the FAQ corpus and uses cosine similarity
to select the most relevant answer for a student's query.
"""

from __future__ import annotations


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from faq_data import FAQS
from preprocessor import preprocess_to_string


class TFIDFRetriever:
    """Retrieval engine that ranks FAQs by TF-IDF cosine similarity."""

    def __init__(self):
        # Build corpus from FAQ questions + keywords
        self.corpus = []
        for faq in FAQS:
            text = faq["question"] + " " + " ".join(faq["keywords"])
            self.corpus.append(preprocess_to_string(text))

        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

    def retrieve(self, query: str, top_k: int = 3) -> list[tuple[dict, float]]:
        """
        Retrieve top_k FAQs ranked by cosine similarity to the query.
        Returns list of (faq_dict, similarity_score) tuples.
        """
        processed_query = preprocess_to_string(query)
        query_vec = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        ranked_indices = similarities.argsort()[::-1][:top_k]
        results = []
        for idx in ranked_indices:
            results.append((FAQS[idx], float(similarities[idx])))

        return results

    def best_match(self, query: str) -> tuple[dict | None, float]:
        """
        Return the single best FAQ match and its confidence score.
        Returns (None, 0.0) if no meaningful match found.
        """
        results = self.retrieve(query, top_k=1)
        if results and results[0][1] > 0.0:
            return results[0]
        return None, 0.0


# Singleton instance — initialized once at import time
retriever = TFIDFRetriever()
