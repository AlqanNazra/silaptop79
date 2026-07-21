import psycopg2
import os

def get_connection():
    try:
        db_url = os.environ.get("DATABASE_URL")
        if db_url:
            conn = psycopg2.connect(db_url)
        else:
            conn = psycopg2.connect(
                host="postgres.railway.internal",
                port="5432",
                database="railway",
                user="postgres",
                password="qgkwcevoLtCBZSHlxzgzIaOQlTZrqrAX"
            )

        conn.autocommit = False
        print("✅ CONNECTED TO DB")

        return conn

    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        raise