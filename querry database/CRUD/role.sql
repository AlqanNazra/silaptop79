CREATE TABLE inventori_role (
    id_role VARCHAR(20) PRIMARY KEY,
    nama_role VARCHAR(100) NOT NULL UNIQUE,
    min_ram INTEGER NOT NULL,
    min_storage INTEGER NOT NULL,
    min_processor_score INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION tambah_role(
    p_nama_role VARCHAR,
    p_min_ram INTEGER,
    p_min_storage INTEGER,
    p_min_processor_score INTEGER
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_exist INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_exist
    FROM inventori_role
    WHERE LOWER(nama_role) = LOWER(p_nama_role);
    IF v_exist > 0 THEN
        RAISE EXCEPTION 'Role sudah ada';
    END IF;
    INSERT INTO inventori_role(
        id_role,
        nama_role,
        min_ram,
        min_storage,
        min_processor_score,
        created_at
    )
    VALUES(
        f_generate_id(
            'ROLE',
            'inventori_role',
            'id_role'
        ),
        p_nama_role,
        p_min_ram,
        p_min_storage,
        p_min_processor_score,
        CURRENT_TIMESTAMP
    );
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_role(
    p_id_role VARCHAR,
    p_nama_role VARCHAR,
    p_min_ram INTEGER,
    p_min_storage INTEGER,
    p_min_processor_score INTEGER
)
RETURNS BOOLEAN AS
$$
BEGIN
    UPDATE inventori_role
    SET
        nama_role = p_nama_role,
        min_ram = p_min_ram,
        min_storage = p_min_storage,
        min_processor_score = p_min_processor_score
    WHERE id_role = p_id_role;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Role tidak ditemukan';
    END IF;
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION get_role_by_id(
    p_id_role VARCHAR
)
RETURNS TABLE(
    id_role VARCHAR,
    nama_role VARCHAR,
    min_ram INTEGER,
    min_storage INTEGER,
    min_processor_score INTEGER
)
AS
$$
BEGIN
RETURN QUERY
SELECT
    r.id_role,
    r.nama_role,
    r.min_ram,
    r.min_storage,
    r.min_processor_score
FROM inventori_role r
WHERE r.id_role = p_id_role;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_all_role()
RETURNS TABLE(
    id_role VARCHAR,
    nama_role VARCHAR,
    min_ram INTEGER,
    min_storage INTEGER,
    min_processor_score INTEGER
)
AS
$$
BEGIN
RETURN QUERY
SELECT
    r.id_role,
    r.nama_role,
    r.min_ram,
    r.min_storage,
    r.min_processor_score
FROM inventori_role r
ORDER BY r.nama_role;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_role(
    p_id_role VARCHAR
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_projectrole INTEGER;
    v_bobot INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_projectrole
    FROM projectrole
    WHERE id_role = p_id_role;

    SELECT COUNT(*)
    INTO v_bobot
    FROM bobot_kriteria
    WHERE role = p_id_role;

    IF v_projectrole > 0 THEN
        RAISE EXCEPTION 'Role masih digunakan pada projectrole';
    END IF;

    IF v_bobot > 0 THEN
        RAISE EXCEPTION 'Role masih digunakan pada bobot_kriteria';
    END IF;

    DELETE FROM role
    WHERE id_role = p_id_role;

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION validate_role(
    p_nama VARCHAR
)
RETURNS BOOLEAN AS $$
DECLARE
    total INT;
BEGIN
    SELECT COUNT(*)
    INTO total
    FROM role
    WHERE LOWER(nama_role) = LOWER(p_nama);

    RETURN total = 0;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_kriteria_role(p_id_role VARCHAR)
RETURNS TABLE (id_kriteria VARCHAR, nama_kriteria VARCHAR, nilai_bobot FLOAT) AS $$
BEGIN
    RETURN QUERY
    SELECT k.id_kriteria, k.nama_kriteria, bk.nilai_bobot
    FROM bobot_kriteria bk
    JOIN kriteria k ON bk.id_kriteria = k.id_kriteria
    WHERE bk.role = p_id_role;
END;
$$ LANGUAGE plpgsql;