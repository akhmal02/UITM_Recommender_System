import os

from config import Config
from services.recommender import CourseRecommender
from uitm_data import MAX_SEMESTER_CREDITS, UITM_FACULTIES
from uitm_knowledge import SYSTEM_ABOUT, UITM_ABOUT


class ChatbotError(Exception):
    def __init__(self, message: str, code: str = "error"):
        self.message = message
        self.code = code
        super().__init__(message)


class UITMChatbot:
    """Free-form AI assistant — answers any question using Groq or OpenAI."""

    MAX_HISTORY = 20

    @classmethod
    def get_context(cls, db, user_id: int | None) -> dict:
        if not user_id:
            return {}
        prefs = CourseRecommender.get_preferences(db, user_id) or {}
        enrollments = CourseRecommender.get_enrollments(db, user_id)
        enrolled_credits = CourseRecommender.get_enrolled_credits(db, user_id)
        recs = CourseRecommender.recommend(db, user_id, limit=5)
        return {
            "prefs": prefs,
            "enrollments": enrollments,
            "enrolled_credits": enrolled_credits,
            "remaining_credits": MAX_SEMESTER_CREDITS - enrolled_credits,
            "recommendations": recs,
            "faculty": prefs.get("faculty", "FSKM"),
        }

    @classmethod
    def _build_system_prompt(cls, db, user_id: int | None, ctx: dict, user_name: str) -> str:
        fac_lines = "\n".join(f"  - {code}: {name}" for code, name in UITM_FACULTIES.items())

        with db.cursor() as cur:
            cur.execute(
                "SELECT code, title, faculty, credits, instructor FROM courses WHERE is_active = 1 ORDER BY faculty, code"
            )
            courses = cur.fetchall()
        course_sample = "\n".join(
            f"  - {c['code']}: {c['title']} ({c['faculty']}, {c['credits']}cr, {c['instructor']})"
            for c in courses[:30]
        )
        if len(courses) > 30:
            course_sample += f"\n  ... and {len(courses) - 30} more courses in the database"

        user_block = "Student is browsing (no personal data loaded)."
        if user_id and ctx:
            p = ctx.get("prefs") or {}
            enroll_lines = "\n".join(
                f"  - {e['code']} {e['title']} ({e['credits']} credit hours)"
                for e in ctx.get("enrollments", [])
            ) or "  - None"
            rec_lines = "\n".join(
                f"  - {r['code']} {r['title']} ({r['match_percent']}% match)"
                for r in ctx.get("recommendations", [])
            ) or "  - None"
            user_block = (
                f"Student name: {user_name}\n"
                f"Faculty: {p.get('faculty', 'FSKM')}\n"
                f"Skill level: {p.get('difficulty_level')}\n"
                f"Duration preference: {p.get('duration_preference')}\n"
                f"Format preference: {p.get('format_preference')}\n"
                f"Interest tags: {p.get('interests') or 'none'}\n"
                f"Credit hours enrolled: {ctx.get('enrolled_credits', 0)}/{MAX_SEMESTER_CREDITS}\n"
                f"Credit hours remaining: {ctx.get('remaining_credits', MAX_SEMESTER_CREDITS)}\n"
                f"Current enrollments:\n{enroll_lines}\n"
                f"Top recommendations:\n{rec_lines}"
            )

        return f"""You are UITM CourseRec AI — a friendly, intelligent assistant for Universiti Teknologi MARA (UITM) students.

IMPORTANT BEHAVIOUR:
- Answer ANY question the student asks — freely and naturally like ChatGPT
- You are NOT limited to predefined rules or fixed responses
- You can discuss UITM, courses, study tips, careers, general knowledge, homework help, casual chat, etc.
- Be warm, helpful, concise, and use markdown (**bold**, bullet lists) when useful
- When asked about this app's data (enrollments, credits, recommendations), use the LIVE STUDENT DATA below
- For course codes, prefer the course catalog below; do not invent fake UITM course codes
- If you don't know something, say so honestly
- Respond in the same language the student uses (English or Malay)

ABOUT THIS APP:
{SYSTEM_ABOUT}

ABOUT UITM:
{UITM_ABOUT}

UITM FACULTIES:
{fac_lines}

COURSE CATALOG ({len(courses)} courses):
{course_sample}

LIVE STUDENT DATA:
{user_block}
"""

    @classmethod
    def _get_ai_client(cls):
        provider = (Config.AI_PROVIDER or "groq").lower()

        if provider == "openai":
            if not Config.OPENAI_API_KEY:
                raise ChatbotError(
                    "OpenAI API key not configured. Add OPENAI_API_KEY to config.env, "
                    "or set AI_PROVIDER=groq with a free key from https://console.groq.com",
                    "no_api_key",
                )
            from openai import OpenAI
            return OpenAI(api_key=Config.OPENAI_API_KEY), Config.OPENAI_MODEL

        # Default: Groq (free tier, fast)
        if not Config.GROQ_API_KEY:
            raise ChatbotError(
                "AI API key not configured.\n\n"
                "**Free setup (recommended):**\n"
                "1. Go to https://console.groq.com and create a free API key\n"
                "2. Add to config.env:\n"
                "   GROQ_API_KEY=your-key-here\n"
                "   AI_PROVIDER=groq\n"
                "3. Restart the app\n\n"
                "Or use OpenAI: set OPENAI_API_KEY and AI_PROVIDER=openai",
                "no_api_key",
            )
        from openai import OpenAI
        client = OpenAI(api_key=Config.GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")
        return client, Config.GROQ_MODEL

    @classmethod
    def respond(
        cls,
        db,
        user_id: int | None,
        message: str,
        user_name: str = "Student",
        history: list | None = None,
    ) -> dict:
        message = message.strip()
        if not message:
            return {"reply": "Ask me anything — I'm here to help!", "suggestions": []}

        if len(message) > 800:
            return {"reply": "Please keep your message under 800 characters.", "suggestions": []}

        ctx = cls.get_context(db, user_id)
        system_prompt = cls._build_system_prompt(db, user_id, ctx, user_name)

        messages = [{"role": "system", "content": system_prompt}]
        for item in (history or [])[-cls.MAX_HISTORY:]:
            if item.get("role") in ("user", "assistant") and item.get("content"):
                messages.append({"role": item["role"], "content": item["content"]})
        messages.append({"role": "user", "content": message})

        try:
            client, model = cls._get_ai_client()
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=800,
                temperature=0.75,
            )
            reply = response.choices[0].message.content.strip()
            return {"reply": reply, "suggestions": []}

        except ChatbotError as e:
            return {"reply": e.message, "suggestions": [], "error": e.code}

        except Exception as e:
            err = str(e).lower()
            if "api key" in err or "authentication" in err or "401" in err:
                return {
                    "reply": "Invalid API key. Please check GROQ_API_KEY or OPENAI_API_KEY in config.env and restart the app.",
                    "suggestions": [],
                    "error": "auth_error",
                }
            if "rate" in err or "429" in err:
                return {
                    "reply": "AI service is busy. Please wait a moment and try again.",
                    "suggestions": [],
                    "error": "rate_limit",
                }
            return {
                "reply": "I couldn't reach the AI service right now. Please check your API key and internet connection, then try again.",
                "suggestions": [],
                "error": "service_error",
            }
