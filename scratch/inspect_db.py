import os
import django

import sys
import os
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'inventori_laptopinventori';
    """)
    rows = cursor.fetchall()
    print("Columns in inventori_laptopinventori:")
    for row in rows:
        print(row)
