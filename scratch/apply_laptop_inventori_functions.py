import os
import sys

# Add project root to python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import get_connection
from silaptop79.db import get_connection

def apply_sql():
    sql_file_path = os.path.join(project_root, 'querry database', 'CRUD', 'laptop_invetori.sql')
    print(f"Reading SQL file: {sql_file_path}")
    
    with open(sql_file_path, 'r') as f:
        sql_content = f.read()

    # Split script by CREATE OR REPLACE FUNCTION block roughly, or execute all
    # Since there are multiple commands, we should separate them or execute them as blocks
    # psycopg2 allows executing multiple commands in one execute() call if they are valid SQL
    conn = get_connection()
    try:
        cur = conn.cursor()
        print("Executing SQL content...")
        cur.execute(sql_content)
        conn.commit()
        print("SQL functions applied successfully!")
    except Exception as e:
        print(f"Error executing SQL: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    apply_sql()
