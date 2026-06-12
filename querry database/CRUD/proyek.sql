CREATE TABLE inventori_proyek (
    id_proyek VARCHAR(20) PRIMARY KEY,
    nama_proyek VARCHAR(255) NOT NULL,
    user_perusahaan VARCHAR(255),
    mulai_proyek DATE,
    akhir_proyek DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE inventori_proyek ALTER COLUMN updated_at DROP NOT NULL;


CREATE OR REPLACE FUNCTION tambah_proyek(
    p_nama_proyek VARCHAR,
    p_user_perusahaan VARCHAR,
    p_mulai_proyek DATE,
    p_akhir_proyek DATE
)
RETURNS BOOLEAN AS
$$
BEGIN

    INSERT INTO inventori_proyek(
        id_proyek,
        nama_proyek,
        user_perusahaan,
        mulai_proyek,
        akhir_proyek,
        created_at,
        updated_at
    )
    VALUES(
        f_generate_id(
            'PRYK',
            'inventori_proyek',
            'id_proyek'
        ),
        p_nama_proyek,
        p_user_perusahaan,
        p_mulai_proyek,
        p_akhir_proyek,
        CURRENT_TIMESTAMP,
        NULL
    );

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_proyek(
    p_id_proyek VARCHAR,
    p_nama_proyek VARCHAR,
    p_client_perusahaan VARCHAR,
    p_mulai_proyek DATE,
    p_akhir_proyek DATE
)
RETURNS BOOLEAN AS
$$
BEGIN

    UPDATE proyek
    SET
        nama_proyek = p_nama_proyek,
        client_perusahaan = p_client_perusahaan,
        mulai_proyek = p_mulai_proyek,
        akhir_proyek = p_akhir_proyek
    WHERE id_proyek = p_id_proyek;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Proyek tidak ditemukan';
    END IF;

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION hapus_proyek(
    p_id_proyek VARCHAR
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_relasi INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_relasi
    FROM projectrole
    WHERE id_proyek = p_id_proyek;

    IF v_relasi > 0 THEN
        RAISE EXCEPTION 'Proyek masih digunakan pada projectrole';
    END IF;

    DELETE FROM proyek
    WHERE id_proyek = p_id_proyek;

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_proyek(
    p_id VARCHAR
)
RETURNS TABLE(
    id_proyek VARCHAR,
    nama_proyek VARCHAR
)
AS $$
BEGIN

    RETURN QUERY
    SELECT
        p.id_proyek,
        p.nama_proyek
    FROM proyek p
    WHERE p.id_proyek = p_id;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_bobot_proyek(
    p_id VARCHAR
)
RETURNS FLOAT AS $$
DECLARE
    hasil FLOAT;
BEGIN
    SELECT AVG(b.nilai_bobot)
    INTO hasil
    FROM bobot_kriteria b
    JOIN teknologi t ON t.id_teknologi = b.id_teknologi
    WHERE t.id_project_role IN (
        SELECT id_project_role
        FROM project_role
        WHERE id_proyek = p_id
    );

    RETURN COALESCE(hasil,0);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION validate_proyek(
    p_id VARCHAR
)
RETURNS BOOLEAN AS $$
DECLARE
    total INT;
BEGIN
    SELECT COUNT(*)
    INTO total
    FROM proyek
    WHERE id_proyek = p_id;

    RETURN total > 0;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_detail_proyek(
    p_id_proyek VARCHAR
)
RETURNS TABLE(
    id_proyek VARCHAR,
    nama_proyek VARCHAR,
    nama_role VARCHAR
)
AS
$$
BEGIN

    RETURN QUERY

    SELECT
        p.id_proyek,
        p.nama_proyek,
        r.nama_role
    FROM proyek p
    JOIN projectrole pr
        ON pr.id_proyek = p.id_proyek
    JOIN role r
        ON r.id_role = pr.id_role
    WHERE p.id_proyek = p_id_proyek;

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_roles_proyek(
    p_id_proyek VARCHAR
)
RETURNS TABLE(
    id_role VARCHAR,
    nama_role VARCHAR
)
AS
$$
BEGIN

    RETURN QUERY

    SELECT
        r.id_role,
        r.nama_role
    FROM projectrole pr
    JOIN role r
        ON r.id_role = pr.id_role
    WHERE pr.id_proyek = p_id_proyek;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_teknologi_proyek(
    p_id_proyek VARCHAR
)
RETURNS TABLE(
    id_teknologi VARCHAR,
    nama_teknologi VARCHAR
)
AS
$$
BEGIN

    RETURN QUERY

    SELECT DISTINCT
        t.id_teknologi,
        t.nama_teknologi
    FROM teknologi t
    JOIN role_teknologi rt
        ON rt.id_teknologi = t.id_teknologi
    JOIN role r
        ON r.id_role = rt.id_role
    JOIN projectrole pr
        ON pr.id_role = r.id_role
    WHERE pr.id_proyek = p_id_proyek;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_summary_proyek(
    p_id_proyek VARCHAR
)
RETURNS TABLE(
    total_role BIGINT,
    total_teknologi BIGINT,
    rata_bobot FLOAT
)
AS
$$
BEGIN

    RETURN QUERY

    SELECT
        COUNT(DISTINCT pr.id_role),
        COUNT(DISTINCT rt.id_teknologi),
        COALESCE(AVG(b.nilai_bobot),0)

    FROM projectrole pr

    LEFT JOIN role_teknologi rt
        ON rt.id_role = pr.id_role

    LEFT JOIN bobot_kriteria b
        ON b.id_role = pr.id_role

    WHERE pr.id_proyek = p_id_proyek;

END;
$$ LANGUAGE plpgsql;