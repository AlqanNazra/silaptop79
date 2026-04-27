from db import get_connection
from tests.seeder_dss import SeederSAWReady

if __name__ == "__main__":
    conn = get_connection()
    SeederSAWReady(conn).seed_all()
    print("✅ Seeder SAW siap")