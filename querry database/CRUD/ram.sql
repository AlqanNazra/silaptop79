-- =============================================
-- 9. RAM
-- =============================================
CREATE TABLE ram (
    id_ram SERIAL PRIMARY KEY,
    kapasitas_gb INTEGER,
    tipe VARCHAR(50),
    keterangan TEXT
);

CREATE OR REPLACE FUNCTION tambah_ram(
    f_kapasitas INT,
    f_tipe VARCHAR,
    f_keterangan TEXT
)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO ram (kapasitas_gb, tipe, keterangan)
    VALUES (f_kapasitas, f_tipe, f_keterangan);

    RETURN 'RAM berhasil ditambahkan!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_ram()
RETURNS TABLE (
    id_ram INT,
    kapasitas_gb INT,
    tipe VARCHAR,
    keterangan TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM ram;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_ram(
    f_id INT,
    f_kapasitas INT,
    f_tipe VARCHAR,
    f_keterangan TEXT
)
RETURNS TEXT AS $$
BEGIN
    UPDATE ram
    SET 
        kapasitas_gb = f_kapasitas,
        tipe = f_tipe,
        keterangan = f_keterangan
    WHERE id_ram = f_id;

    RETURN 'RAM berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_ram(f_id INT)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM ram
    WHERE id_ram = f_id;

    RETURN 'RAM berhasil dihapus!';
END;
$$ LANGUAGE plpgsql;