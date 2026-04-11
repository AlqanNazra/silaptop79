-- =============================================
-- 2. KRITERIA
-- =============================================
CREATE TABLE kriteria (
    id_kriteria VARCHAR(100) PRIMARY KEY,
    nama_kriteria VARCHAR(255) NOT NULL,
    tipe_kriteria VARCHAR(20) CHECK (tipe_kriteria IN ('benefit','cost'))
);

CREATE OR REPLACE tambah_kriteria (f_nama_kriteria VARCHAR(100),f_tipe_kriteria VARCHAR(20))
RETURNS VOID AS $$
BEGIN
    INSERT INTO kriteria(id_kriteria,nama_kriteria,tipe_kriteria)
    VALUES (f_generate_id('kriteria', 'kriteria')), f_nama_kriteria, f_tipe_kriteria
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE ambil_kriteria()
RETURNS TABLE (id_kriteria, nama_kriteria, tipe_kriteria)
BEGIN
    RETURNS  QUERY
    SELECT *
    FROM kriteria;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_kriteria (f_id_kriteria VARCHAR(100), f_nama_kriteria VARCHAR(100), f_tipe_kriteria VARCHAR(100))
RETURNS TEXT AS $$
BEGIN  
    UPDATE kriteria
    SET nama_kriteria = f_nama_kriteria, tipe_kriteria = f_tipe_kriteria
    WHERE id_kriteria = f_id_kriteria
    RETURNS 'data sudah diupdate'
END;
$$ LANGUAGE plpgsql;