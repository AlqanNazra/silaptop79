import os
import django
import sys
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from django.db import connection

drop_statements = [
    "DROP FUNCTION IF EXISTS tambah_bobot_kriteria(uuid, uuid, double precision) CASCADE;",
    "DROP FUNCTION IF EXISTS update_nilai_swara(uuid, double precision) CASCADE;",
    "DROP FUNCTION IF EXISTS get_bobot_role_teknologi(uuid) CASCADE;",
    "DROP FUNCTION IF EXISTS validasi_total_bobot_project(uuid) CASCADE;",
    # Also drop any other conflicting versions of tambah_bobot_kriteria
    "DROP FUNCTION IF EXISTS tambah_bobot_kriteria(character varying, character varying, double precision) CASCADE;"
]

with open("querry database/fungsi_preprosesSwara.sql", "r") as f:
    sql_script = f.read()

with connection.cursor() as cursor:
    for stmt in drop_statements:
        try:
            cursor.execute(stmt)
            print(f"Executed: {stmt}")
        except Exception as e:
            print(f"Failed to execute '{stmt}': {str(e)}")
            
    try:
        cursor.execute(sql_script)
        print("Successfully applied new functions from fungsi_preprosesSwara.sql!")
    except Exception as e:
        print("Error applying sql script:", str(e))
