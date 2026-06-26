 -- =============================================
--  PEngajuan
-- =============================================
CREATE TABLE inventori_pengajuan (
    id_pengajuan VARCHAR(100) PRIMARY KEY,
    id_user VARCHAR(15),
    kebutuhan_role VARCHAR(100),
    kebutuhan_requirement TEXT,
    bulan DATE,
    keterangan TEXT,
    perusahaan TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    tanggal_pengajuan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tanggal_deadline TIMESTAMP,
    tanggal_approval TIMESTAMP,
    approved_by VARCHAR(15),
    id_proyek VARCHAR(20),
    FOREIGN KEY (id_proyek) REFERENCES proyek(id_proyek),
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (approved_by) REFERENCES users(id_user)
);

CREATE OR REPLACE FUNCTION tambah_pengajuan (
    f_id_user VARCHAR,
    f_kebutuhan_role VARCHAR,
    f_kebutuhan_requirement TEXT,
    f_bulan DATE,
    f_keterangan TEXT,
    f_perusahaan TEXT,
    f_id_proyek VARCHAR
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO inventori_pengajuan (
        id_pengajuan,id_user,
        kebutuhan_role,kebutuhan_requirement,bulan,
        keterangan,perusahaan,status,
        tanggal_pengajuan,id_proyek
    )
    VALUES (
        f_generate_id('PNJ','inventori_pengajuan','id_pengajuan'),
        f_id_user,f_kebutuhan_role,f_kebutuhan_requirement,
        f_bulan,f_keterangan,f_perusahaan,
        'pending',CURRENT_TIMESTAMP,f_id_proyek
    );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_semua_pengajuan()
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
    tanggal_approval TIMESTAMPTZ,
    approved_by VARCHAR,
    id_proyek VARCHAR
)
AS $$
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
        p.tanggal_approval,
        p.approved_by,
        p.id_proyek
    FROM inventori_pengajuan p
    ORDER BY p.tanggal_pengajuan DESC;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION ambil_semua_pengajuan

DROP FUNCTION cari_pengajuan(character varying)

CREATE OR REPLACE FUNCTION cari_pengajuan(
    f_id_pengajuan VARCHAR
)
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
    tanggal_approval TIMESTAMPTZ,
    approved_by VARCHAR,
    id_proyek VARCHAR
)
AS $$
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
        p.tanggal_approval,
        p.approved_by,
        p.id_proyek
    FROM inventori_pengajuan p
    WHERE p.id_pengajuan = f_id_pengajuan;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_pengajuan(
    f_id_pengajuan VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM inventori_pengajuan
    WHERE id_pengajuan = f_id_pengajuan;
    RETURN 'Pengajuan dengan id ' || f_id_pengajuan || ' telah dihapus';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION approve_pengajuan(f_id_pengajuan VARCHAR,f_status VARCHAR,f_approved_by VARCHAR)
RETURNS TEXT AS $$
BEGIN

    IF f_status NOT IN ('approved','rejected') THEN
        RAISE EXCEPTION
        'Status harus approved atau rejected';
    END IF;
    UPDATE inventori_pengajuan
    SET
        status = f_status,
        tanggal_approval = CURRENT_TIMESTAMP,
        id_approved_by = f_approved_by
    WHERE id_pengajuan = f_id_pengajuan;
    IF NOT FOUND THEN
        RAISE EXCEPTION
        'Pengajuan % tidak ditemukan',
        f_id_pengajuan;
    END IF;
    RETURN 'Pengajuan berhasil diupdate menjadi ' || f_status;
END;
$$ LANGUAGE plpgsql;