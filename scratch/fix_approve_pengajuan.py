import psycopg2
from django.conf import settings
import os
import sys

# Setup Django environment
sys.path.append("/Users/dafffc/Documents/SiLaptop79/silaptop79")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
import django
django.setup()

def run_fix():
    db_settings = settings.DATABASES['default']
    conn = psycopg2.connect(
        dbname=db_settings['NAME'],
        user=db_settings['USER'],
        password=db_settings['PASSWORD'],
        host=db_settings['HOST'],
        port=db_settings['PORT']
    )
    
    query = """
    CREATE OR REPLACE FUNCTION approve_pengajuan(
        f_id_pengajuan VARCHAR,
        f_status VARCHAR,
        f_approved_by VARCHAR
    )
    RETURNS TEXT AS $$
    BEGIN 
        IF f_status NOT IN ('approved','rejected') THEN
            RAISE EXCEPTION 'Status tidak valid';
        END IF;
        
        UPDATE inventori_pengajuan 
        SET 
            status = f_status,
            tanggal_approval = CURRENT_TIMESTAMP,
            approved_by_id = f_approved_by
        WHERE id_pengajuan = f_id_pengajuan;

        RETURN 'Pengajuan berhasil diupdate menjadi ' || f_status;
    END;
    $$ LANGUAGE plpgsql;
    """
    
    with conn.cursor() as cur:
        cur.execute(query)
        conn.commit()
    conn.close()
    print("PostgreSQL approve_pengajuan function successfully updated!")

if __name__ == '__main__':
    run_fix()
