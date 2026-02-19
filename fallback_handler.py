"""
fallback_handler.py — Fallback and handover strategy.
Handles unclear or out-of-scope questions with clarification prompts,
related FAQ suggestions, and human advisor routing.
"""

from __future__ import annotations


from faq_data import FAQS

# ── Confidence thresholds ─────────────────────────────────────────────────────
HIGH_CONFIDENCE = 0.35
LOW_CONFIDENCE = 0.15

ADVISOR_INFO = {
    "email": "helpdesk@institute.edu.in",
    "phone": "+91-22-12345678 (Ext. 100)",
    "office": "Student Help Desk, Ground Floor, Admin Block",
    "hours": "Mon–Sat, 9:30 AM – 4:30 PM"
}


def generate_fallback(query: str, top_results: list[tuple[dict, float]]) -> dict:
    """
    Generate an appropriate fallback response based on match confidence.

    Args:
        query: The user's original query
        top_results: List of (faq, score) from TF-IDF retriever

    Returns:
        dict with 'reply', 'type' ('clarification' | 'suggestion' | 'handover'),
        and optional 'suggestions' list
    """
    best_score = top_results[0][1] if top_results else 0.0

    # ── Case 1: Somewhat relevant — suggest related FAQs ─────────────────
    if best_score >= LOW_CONFIDENCE:
        suggestions = []
        for faq, score in top_results[:3]:
            if score >= LOW_CONFIDENCE * 0.5:
                suggestions.append({
                    "question": faq["question"],
                    "id": faq["id"],
                    "score": round(score, 3)
                })

        if suggestions:
            reply = (
                "🤔 I'm not entirely sure I understood your question. "
                "Did you mean one of these?\n\n"
            )
            for i, s in enumerate(suggestions, 1):
                reply += f"  {i}. {s['question']}\n"
            reply += "\nPlease try rephrasing or pick one of the above!"

            return {
                "reply": reply,
                "type": "suggestion",
                "suggestions": suggestions
            }

    # ── Case 2: Very low confidence — ask for clarification ───────────────
    if best_score >= LOW_CONFIDENCE * 0.3:
        return {
            "reply": (
                "😅 I didn't quite get that. Could you rephrase your question?\n\n"
                "💡 **Tip:** Try asking about specific topics like:\n"
                "  • Admission process\n"
                "  • Exam schedule\n"
                "  • Hostel facilities\n"
                "  • Fee structure\n"
                "  • Scholarships\n"
                "  • Placements"
            ),
            "type": "clarification",
            "suggestions": []
        }

    # ── Case 3: No match at all — handover to human ──────────────────────
    return {
        "reply": (
            "😔 I'm sorry, I couldn't find an answer to your question. "
            "This might require assistance from our team.\n\n"
            "📧 **Email:** {email}\n"
            "📞 **Phone:** {phone}\n"
            "🏢 **Visit:** {office}\n"
            "🕐 **Hours:** {hours}\n\n"
            "A human advisor will be happy to help you!"
        ).format(**ADVISOR_INFO),
        "type": "handover",
        "suggestions": []
    }


def is_greeting(query: str) -> str | None:
    """Check if the query is a greeting and return an appropriate response."""
    greetings = {
        "hi": "Hello! 👋 Welcome to the Institute FAQ Bot. How can I help you today?",
        "hello": "Hi there! 👋 I'm your institute FAQ assistant. What would you like to know?",
        "hey": "Hey! 👋 I'm here to answer your questions about the institute. Ask away!",
        "good morning": "Good morning! ☀️ How can I assist you today?",
        "good afternoon": "Good afternoon! How can I help you?",
        "good evening": "Good evening! What can I help you with?",
        "thanks": "You're welcome! 😊 Feel free to ask anything else.",
        "thank you": "Happy to help! 😊 Is there anything else you'd like to know?",
        "bye": "Goodbye! 👋 Have a great day! Feel free to come back anytime.",
        "goodbye": "See you later! 👋 Don't hesitate to ask if you have more questions.",
    }
    lower = query.lower().strip().rstrip("!.,?")
    return greetings.get(lower)
