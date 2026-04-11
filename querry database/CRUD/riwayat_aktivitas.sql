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
ALTER TABLE riwayat_aktivitas
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
    FROM riwayat_aktivitas
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
    FROM riwayat_aktivitas
    WHERE id_user = p_id_user
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- filter by tanggal 
CREATE OR REPLACE FUNCTION get_riwayat_by_tanggal(f_created_at TIMESTAMP)
RETURN TABEL (
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
    FROM riwayat_aktivitas
    WHERE create_user = f_created_at
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- filter by jenis aktivitas 
CREATE OR REPLACE FUNCTION get_riwayat_by_tanggal(f_jenis_aktivitas VARCHAR)
RETURN TABEL (
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
    FROM riwayat_aktivitas
    WHERE jenis_aktivitas = f_jenis_aktivitas
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- filter by kombinasi
CREATE OR REPLACE FUNCTION filter_riwayat_kombinasi(
    p_id_laptop VARCHAR DEFAULT NULL,
    p_id_user VARCHAR DEFAULT NULL,
    f_created_at VARCHAR DEFAULT NULL,
    f_jenis_aktivitas VARCHAR DEFAULT NULL
    )
RETURN TEXT AS $$
CREATE OR REPLACE FUNCTION fn_get_riwayat_master(
    p_id_laptop INT DEFAULT NULL,
    p_id_user INT DEFAULT NULL,
    f_created_at DATE DEFAULT NULL,
    f_jenis_aktivitas TEXT DEFAULT NULL
)
RETURNS TEXT AS $$
BEGIN 
    -- 1. Cek berdasarkan Laptop
    IF p_id_laptop IS NOT NULL THEN
        PERFORM get_riwayat_by_laptop(p_id_laptop);
    END IF;

    -- 2. Cek berdasarkan User
    IF p_id_user IS NOT NULL THEN
        PERFORM get_riwayat_by_user(p_id_user);
    END IF;

    -- 3. Cek berdasarkan Tanggal
    IF f_created_at IS NOT NULL THEN
        PERFORM get_riwayat_by_tanggal(f_created_at);
    END IF;

    -- 4. Cek jika SEMUA parameter terisi (Kombinasi)
    -- Menggunakan AND untuk mengecek semua kondisi sekaligus
    IF f_jenis_aktivitas IS NOT NULL 
       AND f_created_at IS NOT NULL 
       AND p_id_user IS NOT NULL 
       AND p_id_laptop IS NOT NULL 
    THEN
        PERFORM get_riwayat_lengkap(f_jenis_aktivitas, f_created_at, p_id_user, p_id_laptop);
    END IF;

    RETURN 'Proses Filter Selesai';
END;
$$ LANGUAGE plpgsql;

-- Filter joint kobinasi
CREATE OR REPLACE FUNCTION get_riwayat_lengkap(
    f_jenis_aktivitas TEXT,
    f_created_at DATE,
    p_id_user INT,
    p_id_laptop INT
)
RETURNS TABLE (
    id_log INT,
    laptop_name TEXT,
    username TEXT,
    aktivitas TEXT,
    waktu_kejadian TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        l.id, 
        lp.nama_laptop, 
        u.nama_user, 
        l.jenis_aktivitas, 
        l.created_at
    FROM logs l
    JOIN laptops lp ON l.id_laptop = lp.id
    JOIN users u ON l.id_user = u.id
    WHERE 
        -- Filter ini bersifat "Strict" karena dipanggil dari blok IF semua-tidak-null
        l.jenis_aktivitas = f_jenis_aktivitas
        AND l.created_at::DATE = f_created_at
        AND l.id_user = p_id_user
        AND l.id_laptop = p_id_laptop;
END;
$$ LANGUAGE plpgsql;


-- DELETE
CREATE OR REPLACE FUNCTION delete_riwayat(id_aktivitas VARCHAR)
RETURN TEXT AS $$
BEGIN 
    DELETE FROM riwayat_aktivitas
    WHERE id_aktivitas = f_id_aktivitas;

    RETURN 'RIWAYAT TELAH DIHAPUS';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION 

-- PAGINATION


-- Triger 
CREATE TRIGGER trg_create_riwayat_aktivitas_invetori
AFTER INSERT OR UPDATE OR DELETE ON laptop_inventori
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_prosessor
AFTER INSERT OR UPDATE OR DELETE ON prosessor
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_ram
AFTER INSERT OR UPDATE OR DELETE ON ram
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_storage
AFTER INSERT OR UPDATE OR DELETE ON storage
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_pengadaan
AFTER INSERT OR UPDATE OR DELETE ON pengadaan
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_kriteria
AFTER INSERT OR UPDATE OR DELETE ON kriteria
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_bobot_kriteria
AFTER INSERT OR UPDATE OR DELETE ON bobot_kriteria
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_pengajuan
AFTER INSERT OR UPDATE OR DELETE ON pengajuan
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_pemimjaman
AFTER INSERT OR UPDATE OR DELETE ON pemimjaman
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_hasil_saw
AFTER INSERT OR UPDATE OR DELETE ON hasil_saw
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_datail_hasil_saw
AFTER INSERT OR UPDATE OR DELETE ON datail_hasil_saw
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);

CREATE TRIGGER trg_create_riwayat_aktivitas_dss_proses
AFTER INSERT OR UPDATE OR DELETE ON dss_proses
FOR EACH ROW
EXECUTE FUNCTION create_riwayat_aktivitas(p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT);