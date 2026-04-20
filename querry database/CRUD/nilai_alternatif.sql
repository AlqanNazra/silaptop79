-- =============================================
-- 5. ALTERNATIF nilai alternatif
-- =============================================
CREATE TABLE dss_nilaialternatif (
    id_nilai_alternatif VARCHAR(100) PRIMARY KEY,
    nilai_alternatif Float,
    nilai_normalisasi Float,
    id_alternatif_laptop VARCHAR(100),
    id_bobot VARCHAR(100),
    FOREIGN KEY (id_alternatif_laptop) REFERENCES dss_laptopalternatif(id_alternatif_laptop),
    FOREIGN KEY (id_bobot) REFERENCES dss_bobotkriteria(id_bobot),
);

CREATE OR REPLACE FUNCTION tambah_nilai_alternatif(
    f_nilai_alternatif Float,
    f_nilai_normalisasi Float,
    f_id_alternatif_laptop VARCHAR,
    f_id_bobot VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO dss_laptopalternatif (
        id_nilai_alternatif,
        nilai_alternatif,
        nilai_normalisasi,
        id_alternatif_laptop,
        id_bobot
    )
    VALUES (
        f_generate_id('NALT', 'dss_nilaialternatif', 'id_nilai_alternatif'),
        f_nilai_alternatif,
        f_nilai_normalisasi,
        f_id_alternatif_laptop,
        f_id_bobot
    );

    RETURN 'Processor berhasil ditambahkan!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_processor()
RETURNS TABLE (
    id_nilai_alternatif VARCHAR,
    nilai_alternatif Float,
    nilai_normalisasi Float,
    id_alternatif_laptop VARCHAR,
    id_bobot VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM dss_nilaialternatif;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_processor_by_id(f_id VARCHAR)
RETURNS TABLE (
    id_nilai_alternatif VARCHAR,
    nilai_alternatif Float,
    nilai_normalisasi Float,
    id_alternatif_laptop VARCHAR,
    id_bobot VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id_nilai_alternatif, 
        p.nilai_alternatif, 
        p.nilai_normalisasi, 
        p.id_alternatif_laptop,
        p.id_bobot FROM dss_nilaialternatif
    WHERE p.id_nilai_alternatif = f_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_processor(
    f_id_nilai_alternatif VARCHAR,
    f_nilai_alternatif Float,
    f_nilai_normalisasi Float,
    f_id_alternatif_laptop VARCHAR,
    f_id_bobot VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    UPDATE dss_nilaialternatif
    SET 
        id_nilai_alternatif = f_nilai_alternatif,
        nilai_normalisasi = f_nilai_normalisasi,
        id_alternatif_laptop = f_id_alternatif_laptop,
        id_bobot = f_id_bobot
    WHERE id_nilai_alternatif = f_id_nilai_alternatif;

    RETURN 'Processor berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_processor(f_id INT)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM dss_nilaialternatif
    WHERE id_nilai_alternatif = f_id;

    RETURN 'Processor berhasil dihapus!';
END;
$$ LANGUAGE plpgsql;