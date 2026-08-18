from datetime import timedelta

from uitm_data import TIMETABLE_DAYS, TIMETABLE_SLOTS


class TimetableService:
    @staticmethod
    def _time_to_str(t) -> str:
        if hasattr(t, "strftime"):
            return t.strftime("%H:%M")
        return str(t)[:5]

    @staticmethod
    def _slot_index(start_time: str) -> int | None:
        start = TimetableService._time_to_str(start_time)
        for i, (slot_start, _) in enumerate(TIMETABLE_SLOTS):
            if start == slot_start:
                return i
        for i, (slot_start, slot_end) in enumerate(TIMETABLE_SLOTS):
            if slot_start <= start < slot_end:
                return i
        return None

    @staticmethod
    def get_schedules_for_user(db, user_id: int) -> list[dict]:
        with db.cursor() as cur:
            cur.execute(
                """SELECT c.id, c.code, c.title, c.credits, c.faculty, c.instructor,
                          cs.day, cs.start_time, cs.end_time, cs.venue, cs.session_type
                   FROM enrollments e
                   JOIN courses c ON c.id = e.course_id
                   JOIN course_schedules cs ON cs.course_id = c.id
                   WHERE e.user_id = %s
                   ORDER BY cs.day, cs.start_time""",
                (user_id,),
            )
            rows = cur.fetchall()
        for row in rows:
            row["start_label"] = TimetableService._time_to_str(row["start_time"])
            row["end_label"] = TimetableService._time_to_str(row["end_time"])
        return rows

    @classmethod
    def build_grid(cls, schedules: list[dict]) -> dict:
        grid = {
            day: {f"{s[0]}-{s[1]}": [] for s in TIMETABLE_SLOTS}
            for day in TIMETABLE_DAYS
        }
        for item in schedules:
            day = item["day"]
            slot_idx = cls._slot_index(item["start_time"])
            if day not in grid or slot_idx is None:
                continue
            slot_key = f"{TIMETABLE_SLOTS[slot_idx][0]}-{TIMETABLE_SLOTS[slot_idx][1]}"
            grid[day][slot_key].append(item)
        return grid

    @staticmethod
    def detect_clashes(schedules: list[dict]) -> list[dict]:
        clashes = []
        seen: dict[tuple, dict] = {}
        for item in schedules:
            key = (item["day"], TimetableService._time_to_str(item["start_time"]))
            if key in seen:
                clashes.append({
                    "day": item["day"],
                    "time": item["start_label"],
                    "course_a": seen[key]["code"],
                    "course_b": item["code"],
                })
            else:
                seen[key] = item
        return clashes

    @classmethod
    def generate(cls, db, user_id: int) -> dict:
        schedules = cls.get_schedules_for_user(db, user_id)
        enrollments = []
        seen_courses = set()
        total_credits = 0
        for s in schedules:
            if s["id"] not in seen_courses:
                seen_courses.add(s["id"])
                total_credits += s["credits"]
                enrollments.append(s)

        return {
            "grid": cls.build_grid(schedules),
            "slots": TIMETABLE_SLOTS,
            "days": TIMETABLE_DAYS,
            "schedules": schedules,
            "enrollments": enrollments,
            "total_credits": total_credits,
            "clashes": cls.detect_clashes(schedules),
            "slot_labels": [f"{a}–{b}" for a, b in TIMETABLE_SLOTS],
        }
