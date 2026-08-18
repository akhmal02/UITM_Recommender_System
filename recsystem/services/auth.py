import bcrypt


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

    @staticmethod
    def create_user(db, full_name: str, email: str, password: str) -> tuple[bool, str]:
        email = email.strip().lower()
        if len(full_name.strip()) < 2:
            return False, "Full name must be at least 2 characters."
        if "@" not in email or "." not in email.split("@")[-1]:
            return False, "Please enter a valid email address."
        if len(password) < 6:
            return False, "Password must be at least 6 characters."

        with db.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            if cur.fetchone():
                return False, "An account with this email already exists."

            password_hash = AuthService.hash_password(password)
            cur.execute(
                "INSERT INTO users (full_name, email, password_hash) VALUES (%s, %s, %s)",
                (full_name.strip(), email, password_hash),
            )
            user_id = cur.lastrowid
            cur.execute(
                """INSERT INTO user_preferences (user_id)
                   VALUES (%s)""",
                (user_id,),
            )
        db.commit()
        return True, "Account created successfully."

    @staticmethod
    def authenticate(db, email: str, password: str) -> dict | None:
        email = email.strip().lower()
        with db.cursor() as cur:
            cur.execute(
                "SELECT id, full_name, email, password_hash FROM users WHERE email = %s",
                (email,),
            )
            user = cur.fetchone()
        if not user or not AuthService.verify_password(password, user["password_hash"]):
            return None
        return {
            "id": user["id"],
            "full_name": user["full_name"],
            "email": user["email"],
        }

    @staticmethod
    def get_user_by_id(db, user_id: int) -> dict | None:
        with db.cursor() as cur:
            cur.execute(
                "SELECT id, full_name, email, created_at FROM users WHERE id = %s",
                (user_id,),
            )
            return cur.fetchone()
