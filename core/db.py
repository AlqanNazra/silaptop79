import psycopg2
from psycopg2.extras import RealDictCursor
from django.conf import settings

def get_connection():
    """Membuat koneksi ke database menggunakan setting Django."""
    db_settings = settings.DATABASES['default']
    return psycopg2.connect(
        dbname=db_settings['NAME'],
        user=db_settings['USER'],
        password=db_settings['PASSWORD'],
        host=db_settings['HOST'],
        port=db_settings['PORT'],
        cursor_factory=RealDictCursor
    )
