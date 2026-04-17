-- =============================================
-- 6. HASIL SAW
-- =============================================
CREATE TABLE dss_hasilsaw (
    id_hasil VARCHAR(100) PRIMARY KEY,
    id_dss VARCHAR(100),
    tanggal_proses TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_dss) REFERENCES dss_proses(id_dss)
);

CREATE OR REPLACE FUNCTION buat_hasil_saw(
    f_id_dss VARCHAR(100)
)
RETURNS TEXT AS $$
BEGIN
    -- validasi
    IF NOT EXISTS (
        SELECT 1 FROM dss_proses WHERE id_dss = f_id_dss) THEN RAISE EXCEPTION 'DSS tidak ditemukan';
    END IF;

    INSERT INTO dss_hasilsaw(id_hasil,id_dss)
    VALUES (f_generate_id('SAW','hasil_saw','id_hasil'),f_id_dss);
    RETURN 'Hasil SAW berhasil dibuat';
END;
$$ LANGUAGE plpgsql;