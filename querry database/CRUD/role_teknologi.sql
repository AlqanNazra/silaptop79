CREATE TABLE role_teknologi (
    id_role_teknologi VARCHAR(30) PRIMARY KEY,
    id_role VARCHAR(20) NOT NULL,
    id_teknologi VARCHAR(20) NOT NULL,

    is_default BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_role)
        REFERENCES inventori_role(id_role),

    FOREIGN KEY (id_teknologi)
        REFERENCES inventori_teknologi(id_teknologi),

    UNIQUE(id_role, id_teknologi)
);

CREATE OR REPLACE FUNCTION tambah_role_teknologi(
    p_id_role VARCHAR,
    p_id_teknologi VARCHAR
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_role INTEGER;
    v_teknologi INTEGER;
    v_duplicate INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_role
    FROM inventori_role
    WHERE id_role = p_id_role;

    IF v_role = 0 THEN
        RAISE EXCEPTION 'Role tidak ditemukan';
    END IF;

    SELECT COUNT(*)
    INTO v_teknologi
    FROM inventori_teknologi
    WHERE id_teknologi = p_id_teknologi;

    IF v_teknologi = 0 THEN
        RAISE EXCEPTION 'Teknologi tidak ditemukan';
    END IF;

    SELECT COUNT(*)
    INTO v_duplicate
    FROM role_teknologi
    WHERE id_role = p_id_role
    AND id_teknologi = p_id_teknologi;

    IF v_duplicate > 0 THEN
        RAISE EXCEPTION 'Role teknologi sudah ada';
    END IF;

    INSERT INTO role_teknologi(
        id_role_teknologi,
        id_role,
        id_teknologi
    )
    VALUES(
        f_generate_id(
            'ROLETEK',
            'role_teknologi',
            'id_role_teknologi'
        ),
        p_id_role,
        p_id_teknologi
    );

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;