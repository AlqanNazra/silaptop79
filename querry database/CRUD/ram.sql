-- =============================================
-- 9. RAM
-- =============================================
CREATE TABLE ram (
    id_ram VARCHAR(50) PRIMARY KEY,
    kapasitas_gb INTEGER CHECK (kapasitas_gb > 0),
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
    INSERT INTO inventori_ram (id_ram,kapasitas_gb, tipe, keterangan)
    VALUES (f_generate_id('RAM','inventori_ram','id_ram'),f_kapasitas, f_tipe, f_keterangan);

    RETURN 'RAM berhasil ditambahkan!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_ram()
RETURNS TABLE (
    id_ram VARCHAR,
    kapasitas_gb INT,
    tipe VARCHAR,
    keterangan TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM inventori_ram;
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
    UPDATE inventori_ram
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
    DELETE FROM inventori_ram
    WHERE id_ram = f_id;

    RETURN 'RAM berhasil dihapus!';
END;
$$ LANGUAGE plpgsql;