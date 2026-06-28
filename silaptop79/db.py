import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            port="5433",
            database="TA",
            user="postgres",
            password="190105"
        )

        conn.autocommit = False
        print("✅ CONNECTED TO DB")

        return conn

    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        raise