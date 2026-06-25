import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'silaptop79.settings')
django.setup()

from django.db import connection

def run():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM inventori_laptopinventori LIMIT 0")
        colnames = [desc[0] for desc in cursor.description]
        print("Columns of inventori_laptopinventori:", colnames)

if __name__ == '__main__':
    run()
