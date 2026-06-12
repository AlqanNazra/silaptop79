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
    
    queries = [
        # 1. Redefine tambah_laptop_inventori
        """
        CREATE OR REPLACE FUNCTION tambah_laptop_inventori(
            f_nama_laptop VARCHAR,
            f_model VARCHAR,
            f_os VARCHAR,
            f_kondisi VARCHAR,
            f_status VARCHAR,
            f_lokasi VARCHAR,
            f_id_processor VARCHAR,
            f_id_ram VARCHAR,
            f_id_storage VARCHAR,
            f_ukuran_layar FLOAT
        )
        RETURNS VOID AS $$
        BEGIN
            INSERT INTO inventori_laptopinventori (
                id_laptop_inventori,
                no_inventori,
                nama_laptop,
                model,
                os,
                kondisi,
                status,
                lokasi,
                processor_id,
                ram_id,
                storage_id,
                ukuran_layar
            )
            VALUES (
                f_generate_id('INV','inventori_laptopinventori','id_laptop_inventori'),
                'LTP-' || CAST(extract(epoch from now()) AS TEXT) || f_nama_laptop,
                f_nama_laptop,
                f_model,
                f_os,
                f_kondisi,
                f_status,
                f_lokasi,
                NULLIF(f_id_processor, '')::bigint,
                NULLIF(f_id_ram, '')::bigint,
                NULLIF(f_id_storage, '')::bigint,
                f_ukuran_layar
            );
        END;
        $$ LANGUAGE plpgsql;
        """,
        
        # 2. Redefine ambil_spek_laptop
        """
        CREATE OR REPLACE FUNCTION ambil_spek_laptop(f_id_laptop_inventori VARCHAR)
        RETURNS TABLE (
            nama_processor VARCHAR,
            manufacturer VARCHAR,
            processor_model VARCHAR,
            cores INT,
            threads INT,
            ram_kapasitas INT,
            ram_tipe VARCHAR,
            storage_kapasitas INT,
            storage_tipe VARCHAR
        ) AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                pro.nama_processor,
                pro.manufacturer,
                pro.model,
                pro.cores,
                pro.threads,
                r.kapasitas_gb,
                r.tipe,
                s.kapasitas_gb,
                s.tipe
            FROM inventori_laptopinventori li
            LEFT JOIN inventori_processor pro ON li.processor_id = pro.id_processor
            LEFT JOIN inventori_ram r ON li.ram_id = r.id_ram
            LEFT JOIN inventori_storage s ON li.storage_id = s.id_storage
            WHERE li.id_laptop_inventori = f_id_laptop_inventori;
        END;
        $$ LANGUAGE plpgsql;
        """,
        
        # 3. Redefine ambil_laptop_inventori
        """
        CREATE OR REPLACE FUNCTION ambil_laptop_inventori()
        RETURNS TABLE (
            id_laptop_inventori VARCHAR,
            no_inventori VARCHAR,
            nama_laptop VARCHAR,
            model VARCHAR,
            os VARCHAR,
            kondisi VARCHAR,
            status VARCHAR,
            lokasi VARCHAR,
            ukuran_layar FLOAT,
            nama_processor VARCHAR,
            manufacturer VARCHAR,
            processor_model VARCHAR,
            cores INT,
            threads INT,
            ram_kapasitas INT,
            ram_tipe VARCHAR,
            storage_kapasitas INT,
            storage_tipe VARCHAR
        )
        AS $$
        BEGIN
            RETURN QUERY
            SELECT 
                li.id_laptop_inventori,
                li.no_inventori,
                li.nama_laptop,
                li.model,
                li.os,
                li.kondisi,
                li.status,
                li.lokasi,
                li.ukuran_layar,
                pro.nama_processor,
                pro.manufacturer,
                pro.model,
                pro.cores,
                pro.threads,
                r.kapasitas_gb,
                r.tipe,
                s.kapasitas_gb,
                s.tipe
            FROM inventori_laptopinventori li
            LEFT JOIN inventori_processor pro ON li.processor_id = pro.id_processor
            LEFT JOIN inventori_ram r ON li.ram_id = r.id_ram
            LEFT JOIN inventori_storage s ON li.storage_id = s.id_storage;
        END;
        $$ LANGUAGE plpgsql;
        """,
        
        # 4. Redefine update_spek_inventori
        """
        CREATE OR REPLACE FUNCTION update_spek_inventori(
            f_id_laptop_inventori VARCHAR,
            f_id_processor INTEGER,
            f_id_ram INTEGER,
            f_id_storage INTEGER
        )
        RETURNS TEXT AS $$
        BEGIN
            UPDATE inventori_laptopinventori
            SET 
                processor_id = f_id_processor,
                ram_id = f_id_ram,
                storage_id = f_id_storage
            WHERE id_laptop_inventori = f_id_laptop_inventori;

            RETURN 'Spesifikasi berhasil diupdate!';
        END;
        $$ LANGUAGE plpgsql;
        """
    ]
    
    with conn.cursor() as cur:
        for q in queries:
            cur.execute(q)
        conn.commit()
    conn.close()
    print("All PostgreSQL functions successfully updated!")

if __name__ == '__main__':
    run_fix()
