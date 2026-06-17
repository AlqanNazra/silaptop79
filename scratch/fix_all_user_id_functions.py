import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from django.db import connection

queries = [
    # 1. Update 10-parameter tambah_pengajuan
    """
    CREATE OR REPLACE FUNCTION tambah_pengajuan(
        f_id_user VARCHAR,
        f_kebutuhan_role VARCHAR,
        f_kebutuhan_requirement TEXT,
        f_bulan DATE,
        f_keterangan TEXT,
        f_perusahaan TEXT,
        f_status VARCHAR,
        f_tanggal_pengajuan TIMESTAMP,
        f_tanggal_approval TIMESTAMP,
        f_approved_by VARCHAR
    )
    RETURNS VOID AS $$
    BEGIN
        INSERT INTO inventori_pengajuan (
            id_pengajuan,
            id_user,
            kebutuhan_role,
            kebutuhan_requirement,
            bulan,
            keterangan,
            perusahaan,
            status,
            tanggal_pengajuan ,
            tanggal_approval ,
            approved_by 
        )
        VALUES (
            f_generate_id('PNJ','inventori_pengajuan','id_pengajuan'),
            f_id_user,
            f_kebutuhan_role,
            f_kebutuhan_requirement,
            f_bulan,
            f_keterangan,
            f_perusahaan,
            f_status,
            f_tanggal_pengajuan,
            f_tanggal_approval,
            f_approved_by
        );
    END;
    $$ LANGUAGE plpgsql;
    """,
    
    # 2. Update cari_pengajuan
    """
    CREATE OR REPLACE FUNCTION cari_pengajuan(f_id_pengajuan VARCHAR)
    RETURNS TABLE (
        id_pengajuan VARCHAR,
        id_user VARCHAR,
        kebutuhan_role VARCHAR,
        kebutuhan_requirement TEXT,
        bulan DATE,
        keterangan TEXT,
        perusahaan TEXT,
        status VARCHAR,
        tanggal_pengajuan TIMESTAMPTZ,
        is_read_hc BOOLEAN,
        is_read_it BOOLEAN
    ) AS $$
    BEGIN 
        RETURN QUERY
        SELECT 
            p.id_pengajuan,
            p.id_user,
            p.kebutuhan_role,
            p.kebutuhan_requirement,
            p.bulan,
            p.keterangan,
            p.perusahaan,
            p.status,
            p.tanggal_pengajuan,
            p.is_read_hc,
            p.is_read_it
        FROM inventori_pengajuan p
        WHERE p.id_pengajuan = f_id_pengajuan;
    END;
    $$ LANGUAGE plpgsql;
    """
]

with connection.cursor() as cursor:
    for i, q in enumerate(queries, 1):
        print(f"Executing query {i}...")
        cursor.execute(q)
        print("Success!")

print("All database functions fixed successfully!")
