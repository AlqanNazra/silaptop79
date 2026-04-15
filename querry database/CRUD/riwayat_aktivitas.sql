-- =============================================
-- 14. RIWAYAT AKTIVITAS
-- =============================================
CREATE TABLE riwayat_aktivitas (
    id_aktivitas VARCHAR(100) PRIMARY KEY,
    id_user VARCHAR(15),
    id_laptop_inventori VARCHAR(100),
    jenis_aktivitas VARCHAR(100),
    keterangan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_laptop_inventori) REFERENCES laptop_inventori(id_laptop_inventori)
);

-- Update Table
ALTER TABLE inventori_riwayataktivitas
ADD COLUMN role_pengguna VARCHAR(50),
ADD COLUMN nama_aset VARCHAR(255);

-- CREATE (INSERT AKTIVITAS)
CREATE OR REPLACE FUNCTION create_riwayat_aktivitas(
    p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO riwayat_aktivitas (
        id_aktivitas,
        id_user,
        id_laptop_inventori,
        nama_aset,
        role_pengguna,
        jenis_aktivitas,
        keterangan,
        created_at
    )
    VALUES (
        p_id_aktivitas,
        p_id_user,
        p_id_laptop,
        p_nama_aset,
        p_role,
        p_jenis_aktivitas,
        p_keterangan,
        CURRENT_TIMESTAMP
    );
END;
$$ LANGUAGE plpgsql;

-- READ (GET DATA RIWAYAT)
-- Semua data
CREATE OR REPLACE FUNCTION get_all_riwayat()
RETURNS TABLE (
    id_aktivitas VARCHAR,
    id_user VARCHAR,
    id_laptop VARCHAR,
    nama_aset VARCHAR,
    role_pengguna VARCHAR,
    jenis_aktivitas VARCHAR,
    keterangan TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id_aktivitas,
        r.id_user,
        r.id_laptop_inventori,
        r.nama_aset,
        r.role_pengguna,
        r.jenis_aktivitas,
        r.keterangan,
        r.created_at
    FROM riwayat_aktivitas r
    ORDER BY r.created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- FILTER
-- Filter berdasarkan laptop (tracking aset)
CREATE OR REPLACE FUNCTION get_riwayat_by_laptop(p_id_laptop VARCHAR)
RETURNS TABLE (
    id_aktivitas VARCHAR,
    jenis_aktivitas VARCHAR,
    keterangan TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id_aktivitas,
        jenis_aktivitas,
        keterangan,
        created_at
    FROM inventori_riwayataktivitas
    WHERE id_laptop_inventori = p_id_laptop
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Filter berdasarkan user
CREATE OR REPLACE FUNCTION get_riwayat_by_user(p_id_user VARCHAR)
RETURNS TABLE (
    id_aktivitas VARCHAR,
    jenis_aktivitas VARCHAR,
    keterangan TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id_aktivitas,
        jenis_aktivitas,
        keterangan,
        created_at
    FROM inventori_riwayataktivitas
    WHERE id_user = p_id_user
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- filter by tanggal 
CREATE OR REPLACE FUNCTION get_riwayat_by_tanggal(p_tanggal DATE)
RETURNS TABLE (
    id_aktivitas VARCHAR,
    jenis_aktivitas VARCHAR,
    keterangan TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id_aktivitas,
        jenis_aktivitas,
        keterangan,
        created_at
    FROM inventori_riwayataktivitas
    WHERE created_at::DATE = p_tanggal
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- filter by jenis aktivitas 
CREATE OR REPLACE FUNCTION get_riwayat_by_jenis(p_jenis VARCHAR)
RETURNS TABLE (
    id_aktivitas VARCHAR,
    jenis_aktivitas VARCHAR,
    keterangan TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id_aktivitas,
        jenis_aktivitas,
        keterangan,
        created_at
    FROM inventori_riwayataktivitas
    WHERE jenis_aktivitas = p_jenis
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- filter by kombinasi
CREATE OR REPLACE FUNCTION filter_riwayat(
    p_id_laptop VARCHAR DEFAULT NULL,
    p_id_user VARCHAR DEFAULT NULL,
    p_tanggal DATE DEFAULT NULL,
    p_jenis VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    id_aktivitas VARCHAR,
    id_user VARCHAR,
    id_laptop VARCHAR,
    nama_aset VARCHAR,
    role_pengguna VARCHAR,
    jenis_aktivitas VARCHAR,
    keterangan TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id_aktivitas,
        id_user,
        id_laptop_inventori,
        nama_aset,
        role_pengguna,
        jenis_aktivitas,
        keterangan,
        created_at
    FROM riwayat_aktivitas
    WHERE 
        (p_id_laptop IS NULL OR id_laptop_inventori = p_id_laptop)
        AND (p_id_user IS NULL OR id_user = p_id_user)
        AND (p_tanggal IS NULL OR created_at::DATE = p_tanggal)
        AND (p_jenis IS NULL OR jenis_aktivitas = p_jenis)
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- -- Filter joint kobinasi
-- CREATE OR REPLACE FUNCTION get_riwayat_lengkap(
--     f_jenis_aktivitas TEXT,
--     f_created_at DATE,
--     p_id_user INT,
--     p_id_laptop INT
-- )
-- RETURNS TABLE (
--     id_log INT,
--     laptop_name TEXT,
--     username TEXT,
--     aktivitas TEXT,
--     waktu_kejadian TIMESTAMP
-- ) AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT 
--         l.id, 
--         lp.nama_laptop, 
--         u.nama_user, 
--         l.jenis_aktivitas, 
--         l.created_at
--     FROM logs l
--     JOIN laptops lp ON l.id_laptop = lp.id
--     JOIN users u ON l.id_user = u.id
--     WHERE 
--         -- Filter ini bersifat "Strict" karena dipanggil dari blok IF semua-tidak-null
--         l.jenis_aktivitas = f_jenis_aktivitas
--         AND l.created_at::DATE = f_created_at
--         AND l.id_user = p_id_user
--         AND l.id_laptop = p_id_laptop;
-- END;
-- $$ LANGUAGE plpgsql;


-- DELETE
CREATE OR REPLACE FUNCTION delete_riwayat(p_id_aktivitas VARCHAR)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM inventori_riwayataktivitas
    WHERE id_aktivitas = p_id_aktivitas;

    RETURN 'Riwayat berhasil dihapus';
END;
$$ LANGUAGE plpgsql;

-- Triger 
CREATE TRIGGER trg_create_riwayat_aktivitas_invetori
AFTER INSERT OR UPDATE OR DELETE ON inventori_laptopinventori
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_pengadaan
AFTER INSERT OR UPDATE OR DELETE ON dss_laptoppengadaan
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_pengajuan
AFTER INSERT OR UPDATE OR DELETE ON inventori_pengajuan
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_pemimjaman
AFTER INSERT OR UPDATE OR DELETE ON inventori_peminjaman
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);