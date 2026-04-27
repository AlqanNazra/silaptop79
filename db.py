import psycopg2

def get_connection():
    try:
        return psycopg2.connect(
            host="127.0.0.1",
            database="TA",
            user="postgres",
            password="alqan"
        )
        conn.autocommit = False  # pakai transaction
        print("✅ CONNECTED TO DB")
        return conn

    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        raise