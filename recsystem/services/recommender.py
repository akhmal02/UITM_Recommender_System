from uitm_data import MAX_SEMESTER_CREDITS, UITM_FACULTIES

DIFFICULTY_RANK = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}

# Maximum achievable raw score (used to normalize match % to 0–100 for display)
# 30 faculty + 25 difficulty + 20 duration + 15 format + 5 credits + 24 interests + 10 rating
MAX_POSSIBLE_SCORE = 129.0

DURATION_RANGES = {
    "Short": (1, 10),
    "Medium": (11, 14),
    "Long": (15, 99),
}


class CourseRecommender:
    """Rule-based course recommendation engine for UITM."""

    @staticmethod
    def _parse_tags(tags: str) -> set[str]:
        return {t.strip().lower() for t in (tags or "").split(",") if t.strip()}

    @staticmethod
    def _parse_interests(interests: str) -> set[str]:
        return {i.strip().lower() for i in (interests or "").split(",") if i.strip()}

    @staticmethod
    def get_enrolled_credits(db, user_id: int) -> int:
        with db.cursor() as cur:
            cur.execute(
                """SELECT COALESCE(SUM(c.credits), 0) AS total
                   FROM enrollments e
                   JOIN courses c ON c.id = e.course_id
                   WHERE e.user_id = %s""",
                (user_id,),
            )
            return int(cur.fetchone()["total"])

    @staticmethod
    def get_remaining_credits(db, user_id: int) -> int:
        return MAX_SEMESTER_CREDITS - CourseRecommender.get_enrolled_credits(db, user_id)

    @classmethod
    def score_course(
        cls,
        course: dict,
        prefs: dict,
        enrolled_ids: set[int],
        remaining_credits: int,
    ) -> dict | None:
        if course["id"] in enrolled_ids:
            return None

        faculty_pref = prefs.get("faculty") or prefs.get("field_of_study", "FSKM")
        course_faculty = course.get("faculty") or course.get("field_of_study", "")

        reasons: list[str] = []
        score = 0.0

        # Rule 1: Faculty match (required)
        if course_faculty.upper() != faculty_pref.upper():
            return None
        faculty_name = UITM_FACULTIES.get(course_faculty, course_faculty)
        score += 30
        reasons.append(f"Matches your faculty: {faculty_name}")

        # Rule 2: Difficulty within acceptable range
        user_diff = DIFFICULTY_RANK.get(prefs["difficulty_level"], 1)
        course_diff = DIFFICULTY_RANK.get(course["difficulty"], 1)
        if course_diff > user_diff + 1:
            return None
        if course_diff == user_diff:
            score += 25
            reasons.append(f"Perfect difficulty level ({course['difficulty']})")
        elif course_diff < user_diff:
            score += 15
            reasons.append(f"Comfortable difficulty ({course['difficulty']})")
        else:
            score += 10
            reasons.append(f"Stretch goal difficulty ({course['difficulty']})")

        # Rule 3: Duration preference
        low, high = DURATION_RANGES.get(prefs["duration_preference"], (1, 99))
        weeks = course["duration_weeks"]
        if low <= weeks <= high:
            score += 20
            reasons.append(f"Fits your {prefs['duration_preference'].lower()} duration preference")
        elif abs(weeks - low) <= 2 or abs(weeks - high) <= 2:
            score += 10
            reasons.append("Close to your preferred course length")
        else:
            score += 3

        # Rule 4: Format preference
        fmt_pref = prefs["format_preference"]
        if fmt_pref == "Any" or course["format"] == fmt_pref:
            score += 15
            reasons.append(f"{course['format']} delivery matches your preference")
        elif course["format"] == "Hybrid":
            score += 8
            reasons.append("Hybrid format offers flexibility")

        # Rule 5: Semester credit limit (max 24 hours)
        if course["credits"] > remaining_credits:
            return None
        score += 5
        reasons.append(
            f"Fits within semester limit ({course['credits']} cr, {remaining_credits} cr remaining)"
        )

        # Rule 6: Interest tag overlap
        course_tags = cls._parse_tags(course["tags"])
        user_interests = cls._parse_interests(prefs.get("interests") or "")
        overlap = course_tags & user_interests
        if overlap:
            tag_score = min(len(overlap) * 8, 24)
            score += tag_score
            reasons.append(f"Interest match: {', '.join(sorted(overlap))}")

        # Rule 7: Rating boost
        rating = float(course["rating"])
        score += rating * 2
        reasons.append(f"Rated {rating:.1f}/5.0 by students")

        # Raw score can exceed 100 — used for ranking between courses.
        # Match % is normalized to 0–100 so users see a clear, comparable percentage.
        match_pct = min(100, round(score / MAX_POSSIBLE_SCORE * 100))
        return {
            **course,
            "faculty": course_faculty,
            "match_score": round(score, 1),
            "match_percent": match_pct,
            "reasons": reasons,
        }

    @classmethod
    def recommend(cls, db, user_id: int, limit: int = 12) -> list[dict]:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM user_preferences WHERE user_id = %s", (user_id,))
            prefs = cur.fetchone()
            if not prefs:
                return []

            cur.execute(
                "SELECT course_id FROM enrollments WHERE user_id = %s",
                (user_id,),
            )
            enrolled_ids = {row["course_id"] for row in cur.fetchall()}

            cur.execute(
                "SELECT * FROM courses WHERE is_active = 1 ORDER BY rating DESC",
            )
            courses = cur.fetchall()

        remaining = cls.get_remaining_credits(db, user_id)
        scored = []
        for course in courses:
            result = cls.score_course(course, prefs, enrolled_ids, remaining)
            if result:
                scored.append(result)

        scored.sort(key=lambda c: (c["match_score"], float(c["rating"])), reverse=True)
        return scored[:limit]

    @staticmethod
    def get_preferences(db, user_id: int) -> dict | None:
        with db.cursor() as cur:
            cur.execute("SELECT * FROM user_preferences WHERE user_id = %s", (user_id,))
            prefs = cur.fetchone()
        if prefs and not prefs.get("faculty"):
            prefs["faculty"] = prefs.get("field_of_study", "FSKM")
        return prefs

    @staticmethod
    def save_preferences(db, user_id: int, data: dict) -> None:
        with db.cursor() as cur:
            cur.execute(
                """UPDATE user_preferences SET
                   faculty = %s,
                   difficulty_level = %s,
                   duration_preference = %s,
                   format_preference = %s,
                   interests = %s
                   WHERE user_id = %s""",
                (
                    data["faculty"],
                    data["difficulty_level"],
                    data["duration_preference"],
                    data["format_preference"],
                    data["interests"],
                    user_id,
                ),
            )
        db.commit()

    @staticmethod
    def get_all_courses(
        db,
        faculty: str | None = None,
        difficulty: str | None = None,
    ) -> list[dict]:
        query = "SELECT * FROM courses WHERE is_active = 1"
        params: list = []
        if faculty:
            query += " AND faculty = %s"
            params.append(faculty)
        if difficulty:
            query += " AND difficulty = %s"
            params.append(difficulty)
        query += " ORDER BY faculty ASC, code ASC"
        with db.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchall()

    @staticmethod
    def get_courses_grouped_by_faculty(
        db,
        faculty: str | None = None,
        difficulty: str | None = None,
    ) -> dict[str, list[dict]]:
        courses = CourseRecommender.get_all_courses(db, faculty, difficulty)
        grouped: dict[str, list[dict]] = {code: [] for code in UITM_FACULTIES}
        for course in courses:
            fac = course.get("faculty") or course.get("field_of_study", "FSKM")
            if fac not in grouped:
                grouped[fac] = []
            grouped[fac].append(course)
        return {k: v for k, v in grouped.items() if v}

    @staticmethod
    def get_enrollments(db, user_id: int) -> list[dict]:
        with db.cursor() as cur:
            cur.execute(
                """SELECT c.*, e.enrolled_at
                   FROM enrollments e
                   JOIN courses c ON c.id = e.course_id
                   WHERE e.user_id = %s
                   ORDER BY e.enrolled_at DESC""",
                (user_id,),
            )
            return cur.fetchall()

    @staticmethod
    def enroll(db, user_id: int, course_id: int) -> tuple[bool, str]:
        with db.cursor() as cur:
            cur.execute(
                "SELECT id, credits, code FROM courses WHERE id = %s AND is_active = 1",
                (course_id,),
            )
            course = cur.fetchone()
            if not course:
                return False, "Course not found."

            cur.execute(
                "SELECT id FROM enrollments WHERE user_id = %s AND course_id = %s",
                (user_id, course_id),
            )
            if cur.fetchone():
                return False, "You are already enrolled in this course."

            enrolled_credits = CourseRecommender.get_enrolled_credits(db, user_id)
            if enrolled_credits + course["credits"] > MAX_SEMESTER_CREDITS:
                remaining = MAX_SEMESTER_CREDITS - enrolled_credits
                return False, (
                    f"Cannot enroll. UITM semester limit is {MAX_SEMESTER_CREDITS} credit hours. "
                    f"You have {remaining} credit hour(s) remaining."
                )

            cur.execute(
                "INSERT INTO enrollments (user_id, course_id) VALUES (%s, %s)",
                (user_id, course_id),
            )
        db.commit()
        return True, f"Successfully enrolled in {course['code']}!"

    @staticmethod
    def get_faculties(db) -> list[str]:
        with db.cursor() as cur:
            cur.execute(
                "SELECT DISTINCT faculty FROM courses WHERE is_active = 1 ORDER BY faculty"
            )
            return [row["faculty"] for row in cur.fetchall()]

    @staticmethod
    def get_stats(db, user_id: int) -> dict:
        prefs = CourseRecommender.get_preferences(db, user_id)
        faculty = (prefs or {}).get("faculty", "FSKM")

        with db.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) AS total FROM courses WHERE is_active = 1 AND faculty = %s",
                (faculty,),
            )
            faculty_courses = cur.fetchone()["total"]

            cur.execute("SELECT COUNT(*) AS total FROM courses WHERE is_active = 1")
            total_courses = cur.fetchone()["total"]

            cur.execute(
                "SELECT COUNT(*) AS total FROM enrollments WHERE user_id = %s",
                (user_id,),
            )
            enrolled = cur.fetchone()["total"]

        enrolled_credits = CourseRecommender.get_enrolled_credits(db, user_id)
        recommendations = CourseRecommender.recommend(db, user_id, limit=100)
        return {
            "total_courses": total_courses,
            "faculty_courses": faculty_courses,
            "enrolled_count": enrolled,
            "enrolled_credits": enrolled_credits,
            "remaining_credits": MAX_SEMESTER_CREDITS - enrolled_credits,
            "max_credits": MAX_SEMESTER_CREDITS,
            "recommendation_count": len(recommendations),
            "top_match": recommendations[0]["match_percent"] if recommendations else 0,
        }
