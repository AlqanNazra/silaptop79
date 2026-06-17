drop function cari_bobot_kriteria_by_roles

CREATE OR REPLACE FUNCTION cari_bobot_kriteria_by_roles(
    f_roles VARCHAR[]
)
RETURNS TABLE(
    id_bobot VARCHAR,
    id_kriteria VARCHAR,
    nama_kriteria VARCHAR,
    tipe_kriteria VARCHAR,
    role VARCHAR,
    nilai_bobot FLOAT
)
AS $$
BEGIN

    RETURN QUERY

    SELECT
        b.id_bobot,
        b.id_kriteria,
        k.nama_kriteria,
        k.tipe_kriteria,
        r.nama_role,
        b.nilai_bobot

    FROM dss_bobotkriteria b

    JOIN dss_kriteria k
        ON k.id_kriteria = b.id_kriteria

    JOIN role_teknologi rt
        ON rt.id_role_teknologi = b.id_role_teknologi

    JOIN inventori_role r
        ON r.id_role = rt.id_role

    WHERE r.nama_role = ANY(f_roles)
    AND b.is_active = TRUE;

END;
$$ LANGUAGE plpgsql;

select * from dss_kriteria
---------------------------------------------------------------------
SELECT tambah_role('Backend Developer');

SELECT tambah_role('Data Engineer');

SELECT tambah_teknologi(
    'Python',
    'Programming Language'
);

SELECT tambah_teknologi(
    'PostgreSQL',
    'Database'
);

SELECT * FROM inventori_role;

SELECT * FROM inventori_teknologi;

SELECT tambah_role_teknologi(
    'ROLE_0001',
    'TEK_0001'
);

SELECT tambah_role_teknologi(
    'ROLE_0002',
    'TEK_0002'
);

SELECT tambah_kriteria(
    'processor',
    'benefit',
    'hardware'
);

SELECT tambah_kriteria(
    'ram',
    'benefit',
    'hardware'
);

SELECT tambah_kriteria(
    'storage',
    'benefit',
    'hardware'
);

SELECT tambah_kriteria(
    'berat',
    'cost',
    'mobilitas'
);

SELECT tambah_kriteria(
    'baterai',
    'benefit',
    'mobilitas'
);

SELECT * FROM role_teknologi;

SELECT * FROM dss_kriteria;

SELECT * FROM dss_bobotkriteria;

ALTER TABLE dss_bobotkriteria 
RENAME COLUMN role_teknologi_id TO id_role_teknologi;

ALTER TABLE dss_bobotkriteria 
RENAME COLUMN kriteria_id TO id_kriteria;


SELECT tambah_bobot_kriteria(
    'ROLETEK_0001',
    'KRIT_0001',
    0.40
);

SELECT tambah_bobot_kriteria(
    'ROLETEK_0001',
    'KRIT_0002',
    0.30
);

SELECT tambah_bobot_kriteria(
    'ROLETEK_0001',
    'KRIT_0003',
    0.15
);

SELECT tambah_bobot_kriteria(
    'ROLETEK_0001',
    'KRIT_0004',
    0.05
);

SELECT tambah_bobot_kriteria(
    'ROLETEK_0001',
    'KRIT_0005',
    0.10
);

SELECT tambah_bobot_kriteria(
    'ROLETEK_0002',
    'KRIT_0001',
    0.35
);

SELECT tambah_bobot_kriteria(
    'ROLETEK_0002',
    'KRIT_0002',
    0.25
);

SELECT tambah_bobot_kriteria(
    'ROLETEK_0002',
    'KRIT_0003',
    0.25
);

SELECT tambah_bobot_kriteria(
    'ROLETEK_0002',
    'KRIT_0004',
    0.05
);

SELECT tambah_bobot_kriteria(
    'ROLETEK_0002',
    'KRIT_0005',
    0.10
);

SELECT tambah_proyek(
    'Sistem DSS Laptop',
    'PT ABC Teknologi',
    '2026-05-01',
    '2026-12-31'
);

select * from inventori_proyek

SELECT tambah_project_role(
    'PRYK_0001',
    'ROLE_0001',
    0.6
);

SELECT tambah_project_role(
    'PRYK_0001',
    'ROLE_0002',
    0.4
);

SELECT
    SUM(persentase_role)
FROM inventori_project_role
WHERE id_proyek = 'PRYK001';

SELECT *
FROM dss_bobotkriteria;

SELECT * FROM inventori_proyek;

SELECT * FROM inventori_project_role