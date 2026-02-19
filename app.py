"""
app.py — Main Flask application for the Institute FAQ Chatbot.
Orchestrates all NLP modules and serves the chat UI.
"""

from flask import Flask, render_template, request, jsonify, session
import os

from faq_data import FAQS
from preprocessor import preprocess
from synonym_matcher import synonym_match
from tfidf_retriever import retriever
from intent_classifier import classify_intent
from entity_extractor import extract_entities
from context_manager import ConversationContext
from fallback_handler import generate_fallback, is_greeting, HIGH_CONFIDENCE

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/")
def index():
    """Serve the chat UI."""
    session.pop("context", None)  # fresh context each page load
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle a chat message.
    Pipeline:
      1. Check for greetings
      2. Preprocess + extract entities
      3. Classify intent
      4. Resolve follow-ups via context manager
      5. Retrieve best FAQ via TF-IDF
      6. Fallback if confidence too low
      7. Return response with metadata
    """
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a question!", "intent": None,
                        "entities": {}, "confidence": 0.0})

    # ── Restore conversation context ──────────────────────────────────────
    ctx_data = session.get("context")
    ctx = ConversationContext.from_dict(ctx_data) if ctx_data else ConversationContext()

    # ── 1. Check greetings ────────────────────────────────────────────────
    greeting_reply = is_greeting(user_message)
    if greeting_reply:
        ctx.update("greeting", {}, user_message)
        session["context"] = ctx.to_dict()
        return jsonify({
            "reply": greeting_reply,
            "intent": "greeting",
            "entities": {},
            "confidence": 1.0
        })

    # ── 2. Extract entities ───────────────────────────────────────────────
    entities = extract_entities(user_message)

    # ── 3. Classify intent ────────────────────────────────────────────────
    intent, intent_conf = classify_intent(user_message)

    # ── 4. Resolve follow-ups ─────────────────────────────────────────────
    resolved_intent, resolved_entities = ctx.resolve_followup(
        user_message, intent, entities, intent_conf
    )

    # ── 5. TF-IDF retrieval ───────────────────────────────────────────────
    top_results = retriever.retrieve(user_message, top_k=3)
    best_faq, best_score = top_results[0] if top_results else (None, 0.0)

    # Also try synonym matching
    syn_faq, syn_score = synonym_match(user_message)

    # Pick the best between TF-IDF and synonym matching
    if syn_faq and syn_score > best_score:
        best_faq = syn_faq
        best_score = max(syn_score, best_score)

    # ── 6. Determine response ─────────────────────────────────────────────
    if best_faq and best_score >= HIGH_CONFIDENCE:
        reply = best_faq["answer"]

        # Enrich with entity context
        entity_notes = []
        if resolved_entities.get("semester"):
            entity_notes.append(f"📌 Semester: {resolved_entities['semester']}")
        if resolved_entities.get("year"):
            entity_notes.append(f"📌 Year: {resolved_entities['year']}")
        if resolved_entities.get("course_codes"):
            entity_notes.append(f"📌 Course: {', '.join(resolved_entities['course_codes'])}")
        if resolved_entities.get("dates"):
            entity_notes.append(f"📌 Date reference: {', '.join(resolved_entities['dates'])}")

        if entity_notes:
            reply += "\n\n" + "\n".join(entity_notes)

        # Update context
        ctx.update(resolved_intent, resolved_entities, user_message, best_faq["id"])
        session["context"] = ctx.to_dict()

        return jsonify({
            "reply": reply,
            "intent": resolved_intent,
            "entities": resolved_entities,
            "confidence": round(best_score, 3),
            "faq_id": best_faq["id"]
        })

    # ── 7. Fallback ───────────────────────────────────────────────────────
    fallback = generate_fallback(user_message, top_results)
    ctx.update(resolved_intent, resolved_entities, user_message)
    session["context"] = ctx.to_dict()

    return jsonify({
        "reply": fallback["reply"],
        "intent": resolved_intent,
        "entities": resolved_entities,
        "confidence": round(best_score, 3),
        "fallback_type": fallback["type"],
        "suggestions": fallback.get("suggestions", [])
    })


@app.route("/reset", methods=["POST"])
def reset():
    """Reset conversation context."""
    session.pop("context", None)
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("🤖 Institute FAQ Chatbot running at http://localhost:5000")
    app.run(debug=True, port=5000)
