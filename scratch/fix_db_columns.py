import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    try:
        print("Renaming proyek_id to id_proyek...")
        cursor.execute("ALTER TABLE inventori_project_role RENAME COLUMN proyek_id TO id_proyek;")
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")
        
    try:
        print("Renaming role_id to id_role...")
        cursor.execute("ALTER TABLE inventori_project_role RENAME COLUMN role_id TO id_role;")
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")
