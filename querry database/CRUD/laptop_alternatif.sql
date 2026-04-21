-- =============================================
-- 5. ALTERNATIF Laptop
-- =============================================
CREATE TABLE dss_laptopalternatif (
    id_alternatif_laptop VARCHAR(100) PRIMARY KEY,
    model_alternatif TEXT,
    brand_alternatif TEXT,
    id_dss VARCHAR(100),
    FOREIGN KEY (id_dss) REFERENCES dss_dssproses(id_dss)
);

CREATE OR REPLACE FUNCTION tambah_laptop_alternatif(
    f_model_alternatif TEXT,
    f_brand_alternatif TEXT,
    f_id_dss VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO dss_laptopalternatif (
        id_alternatif_laptop,
        model_alternatif,
        brand_alternatif,
        id_dss
    )
    VALUES (
        f_generate_id('LA', 'dss_laptopalternatif', 'id_alternatif_laptop'),
        f_model_alternatif,
        f_brand_alternatif,
        f_id_dss
    );

    RETURN 'Processor berhasil ditambahkan!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_processor()
RETURNS TABLE (
    id_alternatif_laptop VARCHAR,
    f_model_alternatif TEXT,
    f_brand_alternatif TEXT,
    f_id_dss VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM dss_laptopalternatif;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_processor_by_id(f_id VARCHAR)
RETURNS TABLE (
    id_alternatif_laptop VARCHAR,
    f_model_alternatif TEXT,
    f_brand_alternatif TEXT,
    f_id_dss VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT p.id_alternatif_laptop, 
        p.model_alternatif, 
        p.brand_alternatif, 
        p.id_dss FROM dss_laptopalternatif
    WHERE p.id_alternatif_laptop = f_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_processor(
    f_id VARCHAR,
    f_model_alternatif TEXT,
    f_brand_alternatif TEXT,
    f_id_dss VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    UPDATE dss_laptopalternatif
    SET 
        id_alternatif_laptop = f_nama_processor,
        model_alternatif = f_manufacturer,
        brand_alternatif = f_model,
        id_dss = f_cores
    WHERE id_alternatif_laptop = f_id;

    RETURN 'Processor berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_processor(f_id INT)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM dss_laptopalternatif
    WHERE id_alternatif_laptop = f_id;

    RETURN 'Processor berhasil dihapus!';
END;
$$ LANGUAGE plpgsql;