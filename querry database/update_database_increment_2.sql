SELECT * FROM public.dss_bobotkriteria
ORDER BY id_bobot ASC 

alter table dss_bobotkriteria
RENAME COLUMN id_kriteria_id TO id_kriteria;

alter table dss_bobotkriteria
add nilai_swara float;

ALTER TABLE dss_bobotkriteria
ADD CONSTRAINT unique_kriteria_role UNIQUE (id_kriteria, role);

select * from dss_kriteria

drop function tambah_kriteria

CREATE OR REPLACE FUNCTION tambah_kriteria(
    f_nama_kriteria VARCHAR,
    f_tipe_kriteria VARCHAR,
    f_golongan_kriteria VARCHAR
)
RETURNS VARCHAR AS $$
DECLARE
    v_id_kriteria VARCHAR;
BEGIN
    INSERT INTO dss_kriteria(
        id_kriteria,
        nama_kriteria,
        tipe_kriteria,
        golongan_kriteria
    )
    VALUES (
        f_generate_id('KRIT', 'dss_kriteria', 'id_kriteria'),
        f_nama_kriteria,
        f_tipe_kriteria,
        f_golongan_kriteria
    )
    RETURNING id_kriteria INTO v_id_kriteria;

    RETURN v_id_kriteria;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION ambil_kriteria()
RETURNS TABLE (
    id_kriteria VARCHAR, 
    nama_kriteria VARCHAR, 
    tipe_kriteria VARCHAR,
    golongan_kriteria VARCHAR,
    role VARCHAR,
    nilai_bobot NUMERIC, 
    nilai_swara NUMERIC  
) AS $$
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
    LEFT JOIN dss_bobotkriteria bk ON k.id_kriteria = bk.id_kriteria;
END;
$$ LANGUAGE plpgsql;