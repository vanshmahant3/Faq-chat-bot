ocument.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.getElementById("chatMessages");
    const userInput    = document.getElementById("userInput");
    const sendBtn      = document.getElementById("sendBtn");
    const resetBtn     = document.getElementById("resetBtn");

    // ── Send message on Enter or click ───────────────────────────────────
    userInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener("click", sendMessage);

    // ── Topic chips ──────────────────────────────────────────────────────
    document.querySelectorAll(".topic-chip").forEach((chip) => {
        chip.addEventListener("click", () => {
            const query = chip.getAttribute("data-query");
            userInput.value = query;
            sendMessage();
        });
    });

    // ── Reset conversation ───────────────────────────────────────────────
    resetBtn.addEventListener("click", async () => {
        await fetch("/reset", { method: "POST" });
        // Clear all messages except the welcome card
        chatMessages.innerHTML = "";
        // Re-create welcome card
        chatMessages.innerHTML = getWelcomeHTML();
        // Re-bind topic chips
        document.querySelectorAll(".topic-chip").forEach((chip) => {
            chip.addEventListener("click", () => {
                const query = chip.getAttribute("data-query");
                userInput.value = query;
                sendMessage();
            });
        });
        userInput.focus();
    });

    // ── Core send function ───────────────────────────────────────────────
    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // Remove welcome card if still showing
        const welcome = chatMessages.querySelector(".welcome-card");
        if (welcome) {
            welcome.style.animation = "fadeOut 0.2s ease forwards";
            setTimeout(() => welcome.remove(), 200);
        }

        // Render user message
        appendMessage("user", text);
        userInput.value = "";
        userInput.focus();

        // Show typing indicator
        const typingEl = showTypingIndicator();

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            // Remove typing indicator
            typingEl.remove();

            // Render bot reply with metadata
            appendMessage("bot", data.reply, {
                intent: data.intent,
                confidence: data.confidence,
                entities: data.entities || {},
                fallback_type: data.fallback_type || null,
                suggestions: data.suggestions || []
            });

        } catch (err) {
            typingEl.remove();
            appendMessage("bot", "⚠️ Oops! Something went wrong. Please try again.", {
                fallback_type: "error"
            });
        }
    }

    // ── Render a message bubble ──────────────────────────────────────────
    function appendMessage(role, text, meta = {}) {
        const row = document.createElement("div");
        row.className = `message-row ${role}`;

        const avatarEmoji = role === "user" ? "👤" : "🎓";

        let metaHTML = "";
        if (role === "bot" && meta) {
            const chips = [];

            if (meta.intent && meta.intent !== "greeting") {
                chips.push(`<span class="meta-chip intent">🏷️ ${meta.intent}</span>`);
            }

            if (meta.confidence !== undefined && meta.confidence > 0) {
                const pct = Math.round(meta.confidence * 100);
                chips.push(`<span class="meta-chip confidence">📊 ${pct}%</span>`);
            }

            if (meta.entities) {
                if (meta.entities.semester) {
                    chips.push(`<span class="meta-chip entity">📌 Sem ${meta.entities.semester}</span>`);
                }
                if (meta.entities.year) {
                    chips.push(`<span class="meta-chip entity">📌 Year ${meta.entities.year}</span>`);
                }
                if (meta.entities.course_codes && meta.entities.course_codes.length) {
                    chips.push(`<span class="meta-chip entity">📌 ${meta.entities.course_codes.join(", ")}</span>`);
                }
            }

            if (meta.fallback_type) {
                const labels = {
                    suggestion: "🔍 Similar FAQs",
                    clarification: "❓ Need more info",
                    handover: "🧑‍💼 Human help",
                    error: "⚠️ Error"
                };
                chips.push(`<span class="meta-chip fallback">${labels[meta.fallback_type] || meta.fallback_type}</span>`);
            }

            if (chips.length > 0) {
                metaHTML = `<div class="msg-meta">${chips.join("")}</div>`;
            }
        }

        // Format text: convert \n to line breaks
        const formattedText = escapeHTML(text)
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
            .replace(/\n/g, "<br>");

        row.innerHTML = `
            <div class="msg-avatar">${avatarEmoji}</div>
            <div class="msg-content">
                <div class="msg-bubble">${formattedText}</div>
                ${metaHTML}
            </div>
        `;

        chatMessages.appendChild(row);
        scrollToBottom();
    }

    // ── Typing indicator ─────────────────────────────────────────────────
    function showTypingIndicator() {
        const el = document.createElement("div");
        el.className = "typing-indicator";
        el.innerHTML = `
            <div class="msg-avatar">🎓</div>
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        `;
        chatMessages.appendChild(el);
        scrollToBottom();
        return el;
    }

    // ── Scroll to bottom ─────────────────────────────────────────────────
    function scrollToBottom() {
        requestAnimationFrame(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
    }

    // ── HTML escaping ────────────────────────────────────────────────────
    function escapeHTML(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    // ── Welcome card HTML ────────────────────────────────────────────────
    function getWelcomeHTML() {
        return `
            <div class="welcome-card">
                <div class="welcome-icon">🤖</div>
                <h2>Welcome to Institute FAQ Bot!</h2>
                <p>I can help you with questions about:</p>
                <div class="topic-chips">
                    <button class="topic-chip" data-query="What is the admission process?">📋 Admissions</button>
                    <button class="topic-chip" data-query="What are the tuition fees?">💰 Fees</button>
                    <button class="topic-chip" data-query="When are the exams scheduled?">📝 Exams</button>
                    <button class="topic-chip" data-query="Tell me about hostel facilities">🏠 Hostel</button>
                    <button class="topic-chip" data-query="What scholarships are available?">🎓 Scholarships</button>
                    <button class="topic-chip" data-query="Does the college have a placement cell?">💼 Placements</button>
                    <button class="topic-chip" data-query="What are the college timings?">🕐 Timings</button>
                    <button class="topic-chip" data-query="How do I contact the administration?">📞 Contact</button>
                </div>
            </div>
        `;
    }
});

/* Fade-out animation for welcome card */
const style = document.createElement("style");
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to   { opacity: 0; transform: translateY(-10px); }
    }
`;
document.head.appendChild(style);
