"""Initialize MySQL database from database_schema.sql and seed courses."""
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
            charset="utf8mb4",
        )
    except pymysql.Error as e:
        print(f"ERROR: Cannot connect to MySQL — {e}")
        sys.exit(1)

    sql = SCHEMA_FILE.read_text(encoding="utf-8")
    statements = [s.strip() for s in sql.split(";") if s.strip()]

    with conn.cursor() as cur:
        for stmt in statements:
            try:
                cur.execute(stmt)
            except pymysql.Error as e:
                if "already exists" not in str(e).lower():
                    print(f"Warning: {e}")

    conn.commit()

    conn.select_db(Config.DB_NAME)
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM courses")
        if cur.fetchone()[0] == 0:
            result = seed_database(conn)
            print(f"Seeded {result['total']} UITM courses.")
        else:
            print("Courses already exist — skipping seed.")

    conn.close()
    print("Database 'recsystem' ready.")


if __name__ == "__main__":
    main()
