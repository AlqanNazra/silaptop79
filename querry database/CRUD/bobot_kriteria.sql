-- =============================================
-- 3. BOBOT KRITERIA (SWARA)
-- =============================================
CREATE TABLE bobot_kriteria (
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
    INSERT INTO bobot_kriteria(id_bobot,id_kriteria, role, nilai_bobot, id_kriteria)
    VALUES (f_generate_id('bobot','bobot_kriteria'), f_id_kriteria, f_role, f_nilai_bobot)
END;
$$ LANGUAGE plpgsql;

-- cari bobot kriteria

CREATE OR REPLACE FUNCTION cari_bobot_kriteria(f_id_bobot VARCHAR(100))
RETURNS TABLE (id_bobot,id_kriteria, role, nilai_bobot, id_kriteria) AS $$
BEGIN 
    RETURNS QUERY
    SELECT b.id_bobot,b.id_kriteria, b.role, b.nilai_bobot, b.id_kriteria
    FROM bobot_kriteria b
    WHERE b.id_bobot = f_id_bobot;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_semua_data_detail_hasil_saw()
RETURNS TABLE (id_bobot,id_kriteria, role, nilai_bobot, id_kriteria) AS $$
BEGIN
    RETURNS  QUERY
    SELECT *
    FROM bobot_kriteria;
END;
$$ LANGUAGE plpgsql;

-- update bobot kriteria

CREATE OR REPLACE FUNCTION update_bobot_kriteria(f_id_bobot VARCHAR(100), f_nilai_bobot float)
RETURNS TEXT AS $$
BEGIN
    UPDATE bobot_kriteria 
    SET nilai_bobot = f_nilai_bobot 
    WHERE id_bobot = f_id_bobot;
    RETURNS 'Bobot berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

-- DELETE bobot kriteria

CREATE OR REPLACE function hapus_bobot_kriteria(f_id_bobot VARCHAR(100),f_id_kriteria VALUES(100))
RETURNS TEXT As $$
BEGIN
    DELETE FROM kriteria WHERE id_kriteria = f_id_kriteria
    DELETE FROM bobot_kriteria WHERE id_bobot = f_id_bobot;
    RETURNS 'DATA bobot dengan id' || id_alternatif || ' telah dihapus,';
END;
$$ LANGUAGE plpgsql

-- Cara panggil:
-- SELECT update_stok(4, 15);