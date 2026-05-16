-- =============================================
-- 3. BOBOT KRITERIA (SWARA)
-- =============================================
CREATE TABLE dss_bobotkriteria (
    id_bobot VARCHAR(100) PRIMARY KEY,
    id_role_teknologi VARCHAR(30),
    id_kriteria VARCHAR(100),
    nilai_bobot FLOAT CHECK (nilai_bobot >= 0),
    nilai_swara FLOAT CHECK (nilai_swara >= 0),
    versi INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_role_teknologi)
        REFERENCES role_teknologi(id_role_teknologi),
    FOREIGN KEY (id_kriteria)
        REFERENCES dss_kriteria(id_kriteria)
);
ALTER TABLE dss_bobotkriteria
ADD CONSTRAINT unique_kriteria_role UNIQUE (id_kriteria, role);

-- Tambah Bobot function

CREATE OR REPLACE FUNCTION tambah_bobot_kriteria(
    p_id_role_teknologi VARCHAR,
    p_id_kriteria VARCHAR,
    p_nilai_bobot FLOAT
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_role_teknologi INTEGER;
    v_kriteria INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_role_teknologi
    FROM role_teknologi
    WHERE id_role_teknologi = p_id_role_teknologi;

    IF v_role_teknologi = 0 THEN
        RAISE EXCEPTION 'Role teknologi tidak ditemukan';
    END IF;

    SELECT COUNT(*)
    INTO v_kriteria
    FROM dss_kriteria
    WHERE id_kriteria = p_id_kriteria;

    IF v_kriteria = 0 THEN
        RAISE EXCEPTION 'Kriteria tidak ditemukan';
    END IF;

    INSERT INTO dss_bobotkriteria(
        id_bobot,
        id_role_teknologi,
        id_kriteria,
        nilai_bobot,
        versi,
        is_active,
        created_at
    )
    VALUES(
        f_generate_id(
            'BBT',
            'dss_bobotkriteria',
            'id_bobot'
        ),
        p_id_role_teknologi,
        p_id_kriteria,
        p_nilai_bobot,
        1,
        TRUE,
        CURRENT_TIMESTAMP
    );

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cari_bobot_role_teknologi(
    p_id_role VARCHAR
)
RETURNS TABLE (
    nama_teknologi VARCHAR,
    nama_kriteria VARCHAR,
    nilai_bobot FLOAT
)
AS
$$
BEGIN

RETURN QUERY

SELECT
    t.nama_teknologi,
    k.nama_kriteria,
    b.nilai_bobot

FROM dss_bobotkriteria b

JOIN role_teknologi rt
    ON rt.id_role_teknologi = b.id_role_teknologi

JOIN inventori_teknologi t
    ON t.id_teknologi = rt.id_teknologi

JOIN dss_kriteria k
    ON k.id_kriteria = b.id_kriteria

WHERE rt.id_role = p_id_role
AND b.is_active = TRUE;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_semua_data_detail_bobot()
RETURNS TABLE (id_bobot VARCHAR,id_kriteria VARCHAR, role VARCHAR, nilai_bobot FLOAT) AS $$
BEGIN
    RETURN  QUERY
    SELECT b.id_bobot,b.id_kriteria, b.role, b.nilai_bobot
    FROM dss_bobotkriteria b;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_bobot_by_kriteria(
    p_id_bobot VARCHAR,
    p_id_kriteria VARCHAR
)
RETURNS TABLE 
(nama_kriteria VARCHAR,tipe_kriteria VARCHAR,nilai_bobot FLOAT,role_kriteria VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT
        k.nama_kriteria,
        k.tipe_kriteria,
        bk.nilai_bobot,
        bk.role
    FROM dss_bobotkriteria bk
    LEFT JOIN kriteria k ON bk.id_kriteria = k.id_kriteria
    WHERE bk.id_bobot = p_id_bobot AND bk.id_kriteria = p_id_kriteria;
END;
$$ LANGUAGE plpgsql;

-- update bobot kriteria

CREATE OR REPLACE FUNCTION update_bobot_kriteria(f_id_bobot VARCHAR(100), f_nilai_bobot float)
RETURNS TEXT AS $$
BEGIN
    UPDATE dss_bobotkriteria 
    SET nilai_bobot = f_nilai_bobot 
    WHERE id_bobot = f_id_bobot;
    RETURN 'Bobot berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_nilai_swara_per_kriteria(
    f_id_kriteria VARCHAR,
    f_role VARCHAR,
    f_nilai_swara FLOAT
)
RETURNS TEXT AS $$
BEGIN
    UPDATE dss_bobotkriteria 
    SET nilai_swara = f_nilai_swara 
    WHERE id_kriteria = f_id_kriteria
      AND role = f_role;

    RETURN 'OK';
END;
$$ LANGUAGE plpgsql;


-- DELETE bobot kriteria

CREATE OR REPLACE FUNCTION hapus_bobot_kriteria(f_id_bobot VARCHAR)
RETURNS TEXT AS $$ 
DECLARE 
    v_id_kriteria VARCHAR;
    v_jumlah_bobot_lain INT;
BEGIN
    -- 1. Ambil id_kriteria dari baris yang akan dihapus
    SELECT id_kriteria INTO v_id_kriteria
    FROM dss_bobotkriteria
    WHERE id_bobot = f_id_bobot;

    -- Jika data tidak ditemukan, keluar
    IF v_id_kriteria IS NULL THEN
        RETURN 'Data bobot tidak ditemukan';
    END IF;

    -- 2. Hapus baris bobot yang dimaksud (Child)
    DELETE FROM dss_bobotkriteria
    WHERE id_bobot = f_id_bobot;

    -- 3. Cek apakah masih ada baris LAIN yang menggunakan kriteria tersebut
    SELECT COUNT(*) INTO v_jumlah_bobot_lain
    FROM dss_bobotkriteria
    WHERE id_kriteria = v_id_kriteria;

    -- 4. Jika sudah bersih (tidak ada lagi yang pakai), baru hapus kriterianya (Parent)
    IF v_jumlah_bobot_lain = 0 THEN
        DELETE FROM dss_kriteria
        WHERE id_kriteria = v_id_kriteria;
        RETURN 'Bobot dan kriteria berhasil dihapus sepenuhnya';
    ELSE
        RETURN 'Data bobot berhasil dihapus, kriteria tetap ada karena masih digunakan bobot lain';
    END IF;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cari_bobot_kriteria_by_roles(
    f_roles VARCHAR[]
)
RETURNS TABLE(
    id_bobot VARCHAR,
    id_kriteria VARCHAR,
    nama_kriteria VARCHAR,
    tipe_kriteria VARCHAR,
    role VARCHAR,
    nilai_bobot FLOAT
)
AS $$
BEGIN

    RETURN QUERY

    SELECT
        b.id_bobot,
        b.id_kriteria,
        k.nama_kriteria,
        k.tipe_kriteria,
        r.nama_role,
        b.nilai_bobot

    FROM dss_bobotkriteria b

    JOIN dss_kriteria k
        ON k.id_kriteria = b.id_kriteria

    JOIN role_teknologi rt
        ON rt.id_role_teknologi = b.id_role_teknologi

    JOIN inventori_role r
        ON r.id_role = rt.id_role

    WHERE r.nama_role = ANY(f_roles)
    AND b.is_active = TRUE;

END;
$$ LANGUAGE plpgsql;