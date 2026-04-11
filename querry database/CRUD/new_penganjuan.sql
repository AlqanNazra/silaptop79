-- =============================================
--  PEngajuan
-- =============================================
CREATE TABLE pengajuan (
    id_pengajuan VARCHAR(100) PRIMARY KEY,
    id_user VARCHAR(15),
    id_peminjaman VARCHAR(100),

    kebutuhan_role VARCHAR(100),
    kebutuhan_requirement TEXT,
    bulan DATE,
    keterangan TEXT,
    perusahaan TEXT,

    status VARCHAR(20) DEFAULT 'pending',
    tanggal_pengajuan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tanggal_approval TIMESTAMP,
    approved_by VARCHAR(15),

    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_peminjaman) REFERENCES peminjaman(id_peminjaman),
    FOREIGN KEY (approved_by) REFERENCES users(id_user)
);

CREATE OR REPLACE FUNCTION tambah_pengajuan 
( 
    f_id_user VARCHAR,
    f_id_peminjaman VARCHAR,
    f_kebutuhan_ram INTEGER,
    f_kebutuhan_storage INTEGER,
    f_kebutuhan_processor VARCHAR,
    f_kebutuhan_generasi_processor VARCHAR,
    f_keterangan TEXT
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO pengajuan (
        id_pengajuan,
        id_user,
        id_peminjaman,
        kebutuhan_ram,
        kebutuhan_storage,
        kebutuhan_processor,
        kebutuhan_generasi_processor,
        keterangan
    )
    VALUES (
        f_generate_id('PNJ','pengajuan'),
        f_id_user,
        f_id_peminjaman,
        f_kebutuhan_ram,
        f_kebutuhan_storage,
        f_kebutuhan_processor,
        f_kebutuhan_generasi_processor,
        f_keterangan
    );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_semua_pengajuan()
RETURNS TABLE (
    id_pengajuan VARCHAR,
    id_user VARCHAR,
    id_peminjaman VARCHAR,
    kebutuhan_ram INTEGER,
    kebutuhan_storage INTEGER,
    kebutuhan_processor VARCHAR,
    kebutuhan_generasi_processor VARCHAR,
    keterangan TEXT,
    status VARCHAR
) AS $$
BEGIN 
    RETURN QUERY
    SELECT 
        p.*, p.status
    FROM pengajuan p;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cari_peminjaman(f_id_pengajuan VARCHAR(100))
RETURN TABLE (id_pengajuan VARCHAR,
    id_user VARCHAR,
    id_peminjaman VARCHAR,
    kebutuhan_ram INTEGER,
    kebutuhan_storage INTEGER,
    kebutuhan_processor VARCHAR,
    kebutuhan_generasi_processor VARCHAR,
    keterangan TEXT) AS $$
BEGIN 
    RETURN QUERY
    SELECT *
    FROM peminjaman b
    WHERE b.id_pengajuan = f_id_pengajuan;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_pengajuan(f_id_pengajuan VARCHAR)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM pengajuan 
    WHERE id_pengajuan = f_id_pengajuan;
    RETURN 'Pengajuan dengan id ' || f_id_pengajuan || ' telah dihapus';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION approve_pengajuan(
    f_id_pengajuan VARCHAR,
    f_status VARCHAR,
    f_approved_by VARCHAR
)
RETURNS TEXT AS $$
BEGIN 
    UPDATE pengajuan 
    SET 
        status = f_status,
        tanggal_approval = CURRENT_TIMESTAMP,
        approved_by = f_approved_by
    WHERE id_pengajuan = f_id_pengajuan;

    RETURN 'Pengajuan berhasil diupdate menjadi ' || f_status;
END;
$$ LANGUAGE plpgsql;
