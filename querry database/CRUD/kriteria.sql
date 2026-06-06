-- =============================================
-- 2. KRITERIA
-- =============================================
CREATE TABLE kriteria (
    id_kriteria VARCHAR(100) PRIMARY KEY,
    nama_kriteria VARCHAR(255) NOT NULL,
    tipe_kriteria VARCHAR(20) CHECK (tipe_kriteria IN ('benefit','cost')),
    golongan_kriteria VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_teknologi) REFERENCES kriteria(id_teknologi)
);
ALTER TABLE dss_kriteria
ADD CONSTRAINT kriteria UNIQUE (nama_kriteria);

CREATE OR REPLACE FUNCTION tambah_kriteria(
    p_nama_kriteria VARCHAR,
    p_tipe_kriteria VARCHAR,
    p_golongan_kriteria VARCHAR
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_exist INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_exist
    FROM dss_kriteria
    WHERE LOWER(nama_kriteria) = LOWER(p_nama_kriteria);

    IF v_exist > 0 THEN
        RAISE EXCEPTION 'Kriteria sudah ada';
    END IF;

    INSERT INTO dss_kriteria(
        id_kriteria,
        nama_kriteria,
        tipe_kriteria,
        golongan_kriteria
    )
    VALUES(
        f_generate_id(
            'KRIT',
            'dss_kriteria',
            'id_kriteria'
        ),
        p_nama_kriteria,
        p_tipe_kriteria,
        p_golongan_kriteria
    );

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION ambil_kriteria()
RETURNS TABLE (id_kriteria VARCHAR, nama_kriteria VARCHAR, tipe_kriteria VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        k.id_kriteria, 
        k.nama_kriteria, 
        k.tipe_kriteria,
        k.golongan_kriteria,
        bk.role,
        bk.nilai_bobot,
        bk.nilai_swara
    FROM dss_kriteria k
    LEFT JOIN dss_bobotkriteria ON k.id_kriteria = bk.id_kriteria

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_kriteria (f_id_kriteria VARCHAR(100), f_nama_kriteria VARCHAR(100), f_tipe_kriteria VARCHAR(20))
RETURNS TEXT AS $$
BEGIN  
    UPDATE dss_kriteria
    SET nama_kriteria = f_nama_kriteria, tipe_kriteria = f_tipe_kriteria WHERE id_kriteria = f_id_kriteria;
    RETURN 'Data sudah diupdate';
END;
$$ LANGUAGE plpgsql;

ALTER TABLE dss_kriteria
ADD CONSTRAINT kriteria UNIQUE (nama_kriteria);

CREATE OR REPLACE FUNCTION get_kriteria_by_teknologi(
    p_id_teknologi VARCHAR
)
RETURNS TABLE(
    id_kriteria VARCHAR,
    nama_kriteria VARCHAR,
    tipe_kriteria VARCHAR
)
AS
$$
BEGIN

    RETURN QUERY

    SELECT
        id_kriteria,
        nama_kriteria,
        tipe_kriteria
    FROM kriteria
    WHERE id_teknologi = p_id_teknologi;

END;
$$ LANGUAGE plpgsql;