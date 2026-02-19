"""
context_manager.py — Conversation state manager for multi-turn support.
Tracks last intent, entities, and turn count per session to resolve
follow-up queries like "What about hostel?" after an admissions question.
"""

from __future__ import annotations



class ConversationContext:
    """Maintains minimal conversation state for follow-up resolution."""

    def __init__(self):
        self.last_intent = None
        self.last_entities = {}
        self.last_query = ""
        self.last_faq_id = None
        self.turn_count = 0

    def update(self, intent: str, entities: dict, query: str, faq_id: int | None = None):
        """Update context after a successful response."""
        self.last_intent = intent
        # Merge entities — keep old ones if not overridden
        merged = {**self.last_entities, **entities}
        self.last_entities = merged
        self.last_query = query
        self.last_faq_id = faq_id
        self.turn_count += 1

    def resolve_followup(self, query: str, current_intent: str,
                         current_entities: dict, confidence: float) -> tuple[str, dict]:
        """
        If the current query looks like a follow-up (short, low confidence,
        or missing key info), merge with previous context.
        Returns (resolved_intent, resolved_entities).
        """
        words = query.lower().split()
        is_short = len(words) <= 4
        is_low_conf = confidence < 0.3
        has_reference = any(w in words for w in [
            "it", "that", "this", "those", "same", "also",
            "what", "about", "and", "too"
        ])

        # Determine if this is a follow-up
        is_followup = self.turn_count > 0 and (
            (is_short and has_reference) or
            (is_short and is_low_conf) or
            (is_short and not current_entities and self.last_entities)
        )

        if is_followup and self.last_intent:
            # Use current intent if confident, else fall back to previous
            resolved_intent = current_intent if confidence > 0.4 else self.last_intent
            # Merge entities: current overrides previous
            resolved_entities = {**self.last_entities, **current_entities}
            return resolved_intent, resolved_entities

        return current_intent, current_entities

    def reset(self):
        """Reset conversation state."""
        self.last_intent = None
        self.last_entities = {}
        self.last_query = ""
        self.last_faq_id = None
        self.turn_count = 0

    def to_dict(self) -> dict:
        """Serialize context for session storage."""
        return {
            "last_intent": self.last_intent,
            "last_entities": self.last_entities,
            "last_query": self.last_query,
            "last_faq_id": self.last_faq_id,
            "turn_count": self.turn_count
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ConversationContext":
        """Restore context from session data."""
        ctx = cls()
        ctx.last_intent = data.get("last_intent")
        ctx.last_entities = data.get("last_entities", {})
        ctx.last_query = data.get("last_query", "")
        ctx.last_faq_id = data.get("last_faq_id")
        ctx.turn_count = data.get("turn_count", 0)
        return ctx
