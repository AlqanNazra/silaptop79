CREATE TABLE inventori_teknologi (
    id_teknologi VARCHAR(20) PRIMARY KEY,
    nama_teknologi VARCHAR(100) NOT NULL UNIQUE,
    kategori VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION tambah_teknologi(
    p_nama_teknologi VARCHAR,
    p_kategori VARCHAR DEFAULT NULL
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_exist INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_exist
    FROM inventori_teknologi
    WHERE LOWER(nama_teknologi) = LOWER(p_nama_teknologi);

    IF v_exist > 0 THEN
        RAISE EXCEPTION 'Teknologi sudah ada';
    END IF;

    INSERT INTO inventori_teknologi(
        id_teknologi,
        nama_teknologi,
        kategori,
        created_at
    )
    VALUES(
        f_generate_id(
            'TEK',
            'inventori_teknologi',
            'id_teknologi'
        ),
        p_nama_teknologi,
        p_kategori,
        CURRENT_TIMESTAMP
    );

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION hapus_teknologi(
    p_id_teknologi VARCHAR
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_role INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_role
    FROM role_teknologi
    WHERE id_teknologi = p_id_teknologi;

    IF v_role > 0 THEN
        RAISE EXCEPTION
        'Teknologi masih digunakan pada role';
    END IF;

    DELETE FROM inventori_teknologi
    WHERE id_teknologi = p_id_teknologi;

    IF NOT FOUND THEN
        RAISE EXCEPTION
        'Teknologi tidak ditemukan';
    END IF;

    RETURN TRUE;

END;
$$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_teknologi(
    p_id_teknologi VARCHAR,
    p_nama_teknologi VARCHAR
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_exist INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_exist
    FROM inventori_teknologi
    WHERE LOWER(nama_teknologi) = LOWER(p_nama_teknologi)
    AND id_teknologi != p_id_teknologi;

    IF v_exist > 0 THEN
        RAISE EXCEPTION 'Nama teknologi sudah digunakan';
    END IF;

    UPDATE inventori_teknologi
    SET
        nama_teknologi = p_nama_teknologi,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_teknologi = p_id_teknologi;

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_compatibility_teknologi(
    p_nama_teknologi VARCHAR
)
RETURNS TABLE(
    minimal_ram INTEGER,
    minimal_core INTEGER,
    gpu_required BOOLEAN
)
AS
$$
BEGIN

    RETURN QUERY

    SELECT
        CASE
            WHEN LOWER(p_nama_teknologi) LIKE '%docker%' THEN 16
            WHEN LOWER(p_nama_teknologi) LIKE '%flutter%' THEN 16
            WHEN LOWER(p_nama_teknologi) LIKE '%tensorflow%' THEN 32
            ELSE 8
        END,
        CASE
            WHEN LOWER(p_nama_teknologi) LIKE '%tensorflow%' THEN 8
            ELSE 4
        END,
        CASE
            WHEN LOWER(p_nama_teknologi) LIKE '%tensorflow%' THEN TRUE
            ELSE FALSE
        END;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION validate_version_teknologi(
    p_versi VARCHAR
)
RETURNS BOOLEAN AS
$$
BEGIN

    IF p_versi ~ '^[0-9]+(\.[0-9]+){0,2}$' THEN
        RETURN TRUE;
    END IF;

    RETURN FALSE;

END;
$$ LANGUAGE plpgsql;