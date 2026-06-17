import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT routine_name, routine_definition 
        FROM information_schema.routines 
        WHERE routine_schema = 'public' 
          AND routine_definition LIKE '%user_id%';
    """)
    rows = cursor.fetchall()
    print("Functions containing user_id:")
    for row in rows:
        print(f"Name: {row[0]}")
        print(f"Definition:\n{row[1]}")
        print("-" * 50)
