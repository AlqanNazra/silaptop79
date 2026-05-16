-- Hapus tabel lama jika sudah terlanjur ada
DROP TABLE IF EXISTS inventori_project_role;

CREATE TABLE inventori_project_role (
    id_project_role VARCHAR(50) PRIMARY KEY,
    id_proyek VARCHAR(20) REFERENCES inventori_proyek(id_proyek), -- ✅ Diperbaiki
    id_role VARCHAR REFERENCES inventori_role(id_role),           -- ✅ Pastikan ini inventori_role atau role
    persentase_role FLOAT DEFAULT 1
);

ALTER TABLE inventori_project_role
ADD COLUMN persentase_role FLOAT DEFAULT 1;

CREATE OR REPLACE FUNCTION tambah_project_role(
    p_id_proyek VARCHAR,
    p_id_role VARCHAR,
    p_persentase_role FLOAT
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_proyek INTEGER;
    v_role INTEGER;
    v_duplicate INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_proyek
    FROM inventori_proyek
    WHERE id_proyek = p_id_proyek;

    IF v_proyek = 0 THEN
        RAISE EXCEPTION 'Proyek tidak ditemukan';
    END IF;

    SELECT COUNT(*)
    INTO v_role
    FROM inventori_role
    WHERE id_role = p_id_role;

    IF v_role = 0 THEN
        RAISE EXCEPTION 'Role tidak ditemukan';
    END IF;

    SELECT COUNT(*)
    INTO v_duplicate
    FROM inventori_project_role
    WHERE id_proyek = p_id_proyek
    AND id_role = p_id_role;

    IF v_duplicate > 0 THEN
        RAISE EXCEPTION 'Role sudah ada di proyek';
    END IF;

    INSERT INTO inventori_project_role(
        id_project_role,
        id_proyek,
        id_role,
        persentase_role
    )
    VALUES(
        f_generate_id(
            'PRJROLE',
            'inventori_project_role',
            'id_project_role'
        ),
        p_id_proyek,
        p_id_role,
        p_persentase_role
    );

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION hapus_projectrole(
    p_id_projectrole VARCHAR
)
RETURNS BOOLEAN AS
$$
BEGIN

    DELETE FROM projectrole
    WHERE id_projectrole = p_id_projectrole;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'ProjectRole tidak ditemukan';
    END IF;

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_projectrole_by_project(
    p_id_proyek VARCHAR
)
RETURNS TABLE(
    id_project_role VARCHAR,
    id_role VARCHAR,
    nama_role VARCHAR
)
AS
$$
BEGIN

    RETURN QUERY

    SELECT
        pr.id_project_role,
        r.id_role,
        r.nama_role

    FROM inventori_project_role pr

    JOIN role r
        ON r.id_role = pr.id_role

    WHERE pr.id_proyek = p_id_proyek;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_projectrole_by_role(
    p_id_role VARCHAR
)
RETURNS TABLE(
    id_project_role VARCHAR,
    id_proyek VARCHAR,
    nama_proyek VARCHAR
)
AS
$$
BEGIN

    RETURN QUERY

    SELECT
        pr.id_project_role,
        p.id_proyek,
        p.nama_proyek

    FROM inventori_project_role pr

    JOIN inventori_proyek p
        ON p.id_proyek = pr.id_proyek

    WHERE pr.id_role = p_id_role;

END;
$$ LANGUAGE plpgsql


CREATE OR REPLACE FUNCTION validate_projectrole_relation(
    p_id_proyek VARCHAR,
    p_id_role VARCHAR
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_proyek INTEGER;
    v_role INTEGER;
    v_duplicate INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_proyek
    FROM inventori_proyek
    WHERE id_proyek = p_id_proyek;

    IF v_proyek = 0 THEN
        RETURN FALSE;
    END IF;

    SELECT COUNT(*)
    INTO v_role
    FROM role
    WHERE id_role = p_id_role;

    IF v_role = 0 THEN
        RETURN FALSE;
    END IF;

    SELECT COUNT(*)
    INTO v_duplicate
    FROM inventori_project_role
    WHERE id_proyek = p_id_proyek
    AND id_role = p_id_role;

    IF v_duplicate > 0 THEN
        RETURN FALSE;
    END IF;

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;