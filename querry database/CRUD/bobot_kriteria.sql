-- =============================================
-- 3. BOBOT KRITERIA (SWARA)
-- =============================================
CREATE TABLE dss_bobotkriteria (
    id_bobot VARCHAR(100) PRIMARY KEY,
    id_kriteria VARCHAR(100),
    role VARCHAR(100),
    nilai_bobot FLOAT CHECK (nilai_bobot >= 0),
    FOREIGN KEY (id_kriteria) REFERENCES kriteria(id_kriteria)
);

-- Tambah Bobot function

CREATE OR REPLACE FUNCTION tambah_bobot_kriteria(f_id_kriteria VARCHAR(100), f_role VARCHAR(100), f_nilai_bobot FLOAT)
RETURNS VOID AS $$
BEGIN 
    INSERT INTO dss_bobotkriteria(id_bobot,id_kriteria, role, nilai_bobot)
    VALUES (f_generate_id('bobot','dss_bobotkriteria','id_bobot'), f_id_kriteria, f_role, f_nilai_bobot);
END;
$$ LANGUAGE plpgsql;

-- cari bobot kriteria

CREATE OR REPLACE FUNCTION cari_bobot_kriteria(f_id_bobot VARCHAR(100))
RETURNS TABLE (id_bobot VARCHAR,id_kriteria VARCHAR, role VARCHAR, nilai_bobot FLOAT) AS $$
BEGIN 
    RETURN  QUERY
    SELECT b.id_bobot,b.kriteria_id, b.role, b.nilai_bobot
    FROM dss_bobotkriteria b
    WHERE b.id_bobot = f_id_bobot;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_semua_data_detail_bobot()
RETURNS TABLE (id_bobot VARCHAR,id_kriteria VARCHAR, role VARCHAR, nilai_bobot FLOAT) AS $$
BEGIN
    RETURN  QUERY
    SELECT b.id_bobot,b.kriteria_id, b.role, b.nilai_bobot
    FROM dss_bobotkriteria b;
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