import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="TA",
            user="dafffc",
            password="190105"
        )

        conn.autocommit = False
        print("✅ CONNECTED TO DB")

        return conn

    except Exception as e:
        print("❌ DB CONNECTION ERROR:", e)
        raise