-- =============================================
-- 6. HASIL SAW
-- =============================================
CREATE TABLE dss_hasilsaw (
    id_hasil VARCHAR(100) PRIMARY KEY,
    id_dss VARCHAR(100),
    tanggal_proses TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_nilai_alternatif VARCHAR(100),
    FOREIGN KEY (id_dss) REFERENCES dss_proses(id_dss),
    FOREIGN KEY (id_nilai_alternatif) REFERENCES dss_nilaialternatif(id_nilai_alternatif)
);

 DROP FUNCTION buat_hasil_saw

CREATE OR REPLACE FUNCTION buat_hasil_saw(
    f_id_dss VARCHAR(100)
)
RETURNS VARCHAR(100)
AS $$
DECLARE
    v_id_hasil VARCHAR(100);
BEGIN

    IF NOT EXISTS (
        SELECT 1
        FROM dss_dssproses
        WHERE id_dss = f_id_dss
    ) THEN
        RAISE EXCEPTION 'DSS tidak ditemukan';
    END IF;

    v_id_hasil :=
        f_generate_id(
            'SAW',
            'dss_hasilsaw',
            'id_hasil'
        );

    INSERT INTO dss_hasilsaw(
        id_hasil,
        id_dss,
        tanggal_proses
    )
    VALUES(
        v_id_hasil,
        f_id_dss,
        CURRENT_TIMESTAMP
    );

    RETURN v_id_hasil;

END;
$$ LANGUAGE plpgsql;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'dss_hasilsaw'
ORDER BY ordinal_position;

SELECT *
FROM dss_hasilsaw
LIMIT 1;

SELECT *
FROM dss_dssproses
LIMIT 1;

ALTER TABLE dss_hasilsaw
ADD COLUMN id_dss VARCHAR(100);
ALTER TABLE dss_hasilsaw
ADD CONSTRAINT fk_hasilsaw_dss
FOREIGN KEY (id_dss)
REFERENCES dss_dssproses(id_dss);

ALTER TABLE dss_hasilsaw
DROP COLUMN id_dss_id;

alter table dss_hasilsaw
rename column id_nilai_alternatif_id to id_nilai_alternatif

SELECT
    table_name,
    column_name
FROM information_schema.columns
WHERE column_name='id_dss';
