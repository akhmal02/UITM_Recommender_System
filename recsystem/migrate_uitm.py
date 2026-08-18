"""Migrate database to UITM schema and seed 12 courses per faculty."""
import sys
from pathlib import Path

import pymysql

from config import Config
from seed_courses import seed_database

SCHEMA_FILE = Path(__file__).parent / "database_schema.sql"


def main():
    print("Connecting to MySQL...")
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASS,
            database=Config.DB_NAME,
            charset="utf8mb4",
            autocommit=True,
        )
    except pymysql.Error as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    with conn.cursor() as cur:
        cur.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in ("course_schedules", "enrollments", "courses"):
            cur.execute(f"DROP TABLE IF EXISTS {table}")
        cur.execute("SET FOREIGN_KEY_CHECKS = 1")

        cur.execute("SHOW COLUMNS FROM user_preferences LIKE 'faculty'")
        if not cur.fetchone():
            cur.execute("SHOW COLUMNS FROM user_preferences LIKE 'field_of_study'")
            if cur.fetchone():
                cur.execute(
                    "ALTER TABLE user_preferences CHANGE field_of_study faculty VARCHAR(20) NOT NULL DEFAULT 'FSKM'"
                )
            else:
                cur.execute(
                    "ALTER TABLE user_preferences ADD COLUMN faculty VARCHAR(20) NOT NULL DEFAULT 'FSKM'"
                )
        cur.execute("SHOW COLUMNS FROM user_preferences LIKE 'max_credits'")
        if cur.fetchone():
            cur.execute("ALTER TABLE user_preferences DROP COLUMN max_credits")

    conn.close()

    sql = SCHEMA_FILE.read_text(encoding="utf-8")
    statements = [s.strip() for s in sql.split(";") if s.strip() and not s.strip().startswith("CREATE DATABASE")]

    conn = pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASS,
        database=Config.DB_NAME,
        charset="utf8mb4",
        autocommit=False,
    )

    with conn.cursor() as cur:
        for stmt in statements:
            if stmt.upper().startswith("USE "):
                continue
            try:
                cur.execute(stmt)
            except pymysql.Error as e:
                if "already exists" not in str(e).lower():
                    print(f"Note: {e}")

    result = seed_database(conn)
    conn.close()

    print("UITM migration complete!")
    print(f"Total courses: {result['total']}")
    for fac, count in sorted(result["by_faculty"].items()):
        print(f"  {fac}: {count} courses")
    print("Semester credit limit: 24 credit hours.")


if __name__ == "__main__":
    main()
