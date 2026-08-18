from functools import wraps

from flask import (
    Flask,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from config import Config
from models.db import close_db, get_db
from services.auth import AuthService
from services.chatbot import UITMChatbot
from services.recommender import CourseRecommender
from services.timetable import TimetableService
from uitm_data import MAX_SEMESTER_CREDITS, UITM_FACULTIES

app = Flask(__name__)
app.config.from_object(Config)
app.teardown_appcontext(close_db)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


@app.context_processor
def inject_globals():
    user = None
    if "user_id" in session:
        try:
            user = AuthService.get_user_by_id(get_db(), session["user_id"])
        except Exception:
            session.clear()
    return {
        "current_user": user,
        "uitm_faculties": UITM_FACULTIES,
        "max_semester_credits": MAX_SEMESTER_CREDITS,
    }


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if password != confirm:
            flash("Passwords do not match.", "error")
        else:
            try:
                ok, message = AuthService.create_user(get_db(), full_name, email, password)
                flash(message, "success" if ok else "error")
                if ok:
                    return redirect(url_for("login"))
            except Exception:
                flash("Database error. Please ensure MySQL is running and schema is imported.", "error")

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        try:
            user = AuthService.authenticate(get_db(), email, password)
            if user:
                session.clear()
                session["user_id"] = user["id"]
                session["user_name"] = user["full_name"]
                flash(f"Welcome back, {user['full_name'].split()[0]}!", "success")
                return redirect(url_for("dashboard"))
            flash("Invalid email or password.", "error")
        except Exception:
            flash("Database error. Please ensure MySQL is running and schema is imported.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    stats = CourseRecommender.get_stats(db, session["user_id"])
    recommendations = CourseRecommender.recommend(db, session["user_id"], limit=4)
    enrollments = CourseRecommender.get_enrollments(db, session["user_id"])[:3]
    prefs = CourseRecommender.get_preferences(db, session["user_id"])
    return render_template(
        "dashboard.html",
        stats=stats,
        recommendations=recommendations,
        enrollments=enrollments,
        prefs=prefs,
    )


@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    db = get_db()
    if request.method == "POST":
        data = {
            "faculty": request.form.get("faculty", "FSKM"),
            "difficulty_level": request.form.get("difficulty_level", "Beginner"),
            "duration_preference": request.form.get("duration_preference", "Medium"),
            "format_preference": request.form.get("format_preference", "Any"),
            "interests": request.form.get("interests", "").strip(),
        }
        CourseRecommender.save_preferences(db, session["user_id"], data)
        flash("Preferences saved! Recommendations have been updated.", "success")
        return redirect(url_for("recommendations"))

    prefs = CourseRecommender.get_preferences(db, session["user_id"])
    faculties = list(UITM_FACULTIES.keys())
    return render_template("preferences.html", prefs=prefs, faculties=faculties)


@app.route("/recommendations")
@login_required
def recommendations():
    db = get_db()
    recs = CourseRecommender.recommend(db, session["user_id"])
    prefs = CourseRecommender.get_preferences(db, session["user_id"])
    return render_template("recommendations.html", recommendations=recs, prefs=prefs)


@app.route("/courses")
@login_required
def courses():
    db = get_db()
    prefs = CourseRecommender.get_preferences(db, session["user_id"])
    faculty = request.args.get("faculty") or None
    difficulty = request.args.get("difficulty") or None

    if faculty == "all":
        faculty = None

    grouped = CourseRecommender.get_courses_grouped_by_faculty(db, faculty, difficulty)
    enrolled_ids = {e["id"] for e in CourseRecommender.get_enrollments(db, session["user_id"])}
    enrolled_credits = CourseRecommender.get_enrolled_credits(db, session["user_id"])

    total_shown = sum(len(v) for v in grouped.values())
    return render_template(
        "courses.html",
        grouped_courses=grouped,
        enrolled_ids=enrolled_ids,
        selected_faculty=faculty or "",
        selected_difficulty=difficulty or "",
        user_faculty=prefs.get("faculty", "FSKM"),
        total_shown=total_shown,
        enrolled_credits=enrolled_credits,
        remaining_credits=MAX_SEMESTER_CREDITS - enrolled_credits,
    )


@app.route("/timetable")
@login_required
def timetable():
    db = get_db()
    data = TimetableService.generate(db, session["user_id"])
    return render_template("timetable.html", timetable=data)


@app.route("/enroll/<int:course_id>", methods=["POST"])
@login_required
def enroll(course_id):
    ok, message = CourseRecommender.enroll(get_db(), session["user_id"], course_id)
    flash(message, "success" if ok else "error")
    return redirect(request.referrer or url_for("courses"))


@app.route("/chatbot")
@login_required
def chatbot_page():
    return render_template("chatbot.html")


@app.route("/api/chat", methods=["POST"])
@login_required
def api_chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message or len(message) > 800:
        return jsonify({"error": "Message must be 1–800 characters."}), 400

    user_id = session.get("user_id")
    user_name = session.get("user_name", "Student")
    history = session.get("chat_history", [])

    result = UITMChatbot.respond(get_db(), user_id, message, user_name, history)

    if result.get("reply") and not result.get("error"):
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": result["reply"]})
        session["chat_history"] = history[-UITMChatbot.MAX_HISTORY :]

    return jsonify(result)


@app.route("/api/chat/clear", methods=["POST"])
@login_required
def api_chat_clear():
    session.pop("chat_history", None)
    return jsonify({"ok": True})


@app.route("/profile")
@login_required
def profile():
    db = get_db()
    user = AuthService.get_user_by_id(db, session["user_id"])
    prefs = CourseRecommender.get_preferences(db, session["user_id"])
    enrollments = CourseRecommender.get_enrollments(db, session["user_id"])
    enrolled_credits = CourseRecommender.get_enrolled_credits(db, session["user_id"])
    return render_template(
        "profile.html",
        user=user,
        prefs=prefs,
        enrollments=enrollments,
        enrolled_credits=enrolled_credits,
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
