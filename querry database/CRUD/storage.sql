-- =============================================
-- 10. STORAGE
-- =============================================
CREATE TABLE storage (
    id_storage SERIAL PRIMARY KEY,
    kapasitas_gb INTEGER CHECK (kapasitas_gb > 0),
    tipe VARCHAR(100)
);

CREATE OR REPLACE FUNCTION tambah_storage(
    f_kapasitas INT,
    f_tipe VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO inventori_storage (kapasitas_gb, tipe)
    VALUES (f_kapasitas, f_tipe);

    RETURN 'Storage berhasil ditambahkan!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_storage()
RETURNS TABLE (
    id_storage INT,
    kapasitas_gb INT,
    tipe VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM inventori_storage;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_storage(
    f_id INT,
    f_kapasitas INT,
    f_tipe VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    UPDATE inventori_storage
    SET 
        kapasitas_gb = f_kapasitas,
        tipe = f_tipe
    WHERE id_storage = f_id;

    RETURN 'Storage berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_storage(f_id INT)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM inventori_storage
    WHERE id_storage = f_id;

    RETURN 'Storage berhasil dihapus!';
END;
$$ LANGUAGE plpgsql;