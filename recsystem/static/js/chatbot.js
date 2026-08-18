document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const input = document.getElementById('chat-input');
    const messages = document.getElementById('chat-messages');
    const suggestions = document.getElementById('chat-suggestions');
    const clearBtn = document.getElementById('chat-clear');
    if (!form || !input || !messages) return;

    let busy = false;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        sendMessage(input.value);
    });

    suggestions?.addEventListener('click', (e) => {
        const chip = e.target.closest('.suggestion-chip');
        if (chip) sendMessage(chip.dataset.msg);
    });

    clearBtn?.addEventListener('click', async () => {
        await fetch('/api/chat/clear', { method: 'POST' });
        messages.innerHTML = '';
        appendBubble('bot',
            'Chat cleared! Ask me **anything** — UITM, courses, study help, general questions, or just chat.');
        if (suggestions) {
            suggestions.innerHTML = `
                <button type="button" class="suggestion-chip" data-msg="What is UITM?">What is UITM?</button>
                <button type="button" class="suggestion-chip" data-msg="Help me choose courses">Help me choose courses</button>
                <button type="button" class="suggestion-chip" data-msg="What are my enrollments?">My enrollments</button>
            `;
        }
    });

    async function sendMessage(text) {
        const msg = text.trim();
        if (!msg || busy) return;

        busy = true;
        appendBubble('user', msg);
        input.value = '';
        const typing = appendTyping();

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: msg }),
            });
            typing.remove();

            const data = await res.json();
            if (data.error && !data.reply) {
                appendBubble('bot', data.error);
                return;
            }
            appendBubble('bot', data.reply || 'No response received.');
        } catch {
            typing.remove();
            appendBubble('bot', 'Connection error. Please check your internet and try again.');
        } finally {
            busy = false;
            input.focus();
        }
    }

    function appendBubble(role, text) {
        const div = document.createElement('div');
        div.className = `chat-bubble ${role}`;
        const icon = role === 'bot' ? 'smart_toy' : 'person';
        div.innerHTML = `
            <span class="material-symbols-outlined bubble-icon">${icon}</span>
            <div class="bubble-content">${formatText(text)}</div>
        `;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
        return div;
    }

    function appendTyping() {
        const div = document.createElement('div');
        div.className = 'chat-bubble bot typing';
        div.innerHTML = `
            <span class="material-symbols-outlined bubble-icon">smart_toy</span>
            <div class="bubble-content"><span class="typing-dots"><span></span><span></span><span></span></span></div>
        `;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
        return div;
    }

    function formatText(text) {
        return escapeHtml(text)
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/_(.+?)_/g, '<em>$1</em>')
            .replace(/\n/g, '<br>');
    }

    function escapeHtml(s) {
        const d = document.createElement('div');
        d.textContent = s;
        return d.innerHTML;
    }
});
