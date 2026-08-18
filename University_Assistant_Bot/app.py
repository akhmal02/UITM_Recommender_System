import html
import os
import time
from collections import defaultdict, deque

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI


# Load environment variables from app.env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, "app.env"))

app = Flask(__name__)

# Security/abuse controls
MAX_MESSAGE_LENGTH = 600
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 20

# In-memory, IP-based rate tracker (simple baseline protection)
request_log = defaultdict(deque)

SYSTEM_PROMPT = (
    "You are UniAssist Bot, a friendly and professional university assistant. "
    "Help students with general university topics such as courses, timetable, office hours, "
    "academic support, campus services, and guidance. "
    "Be clear, respectful, and concise. "
    "If asked for private student records, grades, or internal-only information, clearly state "
    "you do not have access to official student information systems unless integrated. "
    "Encourage students to confirm official details with the relevant university office."
)


def is_rate_limited(client_ip: str) -> bool:
    """Allow limited requests per IP in a rolling window."""
    now = time.time()
    logs = request_log[client_ip]

    while logs and now - logs[0] > RATE_LIMIT_WINDOW_SECONDS:
        logs.popleft()

    if len(logs) >= RATE_LIMIT_MAX_REQUESTS:
        return True

    logs.append(now)
    return False


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OpenAI API key is missing.")
    return OpenAI(api_key=api_key)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    client_ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown")
    if is_rate_limited(client_ip):
        return jsonify({"error": "Too many requests. Please wait a moment and try again."}), 429

    try:
        payload = request.get_json(silent=True)
    except Exception:
        payload = None

    if not payload or not isinstance(payload, dict):
        return jsonify({"error": "Invalid request format."}), 400

    message = payload.get("message", "")
    if not isinstance(message, str):
        return jsonify({"error": "Message must be text."}), 400

    message = message.strip()
    if not message:
        return jsonify({"error": "Please enter a message before sending."}), 400

    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify(
            {"error": f"Message is too long. Maximum length is {MAX_MESSAGE_LENGTH} characters."}
        ), 400

    # Basic sanitization to reduce XSS risk in logs/echo contexts
    safe_message = html.escape(message)

    try:
        client = get_openai_client()
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": safe_message},
            ],
            temperature=0.4,
        )
        reply = (response.output_text or "").strip()
        if not reply:
            reply = (
                "I could not generate a response right now. "
                "Please try again, or contact your university office for urgent support."
            )

        return jsonify({"reply": reply})
    except Exception:
        # Do not expose raw backend/internal errors to end users
        return jsonify(
            {
                "error": (
                    "I am currently unable to reach the assistant service. "
                    "Please try again shortly."
                )
            }
        ), 503


if __name__ == "__main__":
    # Debug can be enabled for local development only
    app.run(host="0.0.0.0", port=5000, debug=True)
