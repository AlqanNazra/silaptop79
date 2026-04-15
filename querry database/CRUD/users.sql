-- =============================================
-- 1. USERS
-- =============================================
CREATE TABLE users (
    id_user VARCHAR(15) PRIMARY KEY,
    nama VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Update database
ALTER TABLE inventori_user
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP,
ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
ADD CONSTRAINT role_check
CHECK (role IN ('HC', 'IT', 'TALENT'));
ADD CONSTRAINT unique_email UNIQUE (email);

-- Ekstention 
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- CREATE DATA
CREATE OR REPLACE FUNCTION create_user(
    p_id_user VARCHAR,
    p_nama VARCHAR,
    p_email VARCHAR,
    p_password TEXT,
    p_role VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    -- VALIDASI EMAIL UNIK
    IF EXISTS (
        SELECT 1 FROM inventori_user WHERE email = p_email
    ) THEN
        RETURN 'Email sudah digunakan';
    END IF;

    INSERT INTO inventori_user (
        id_user,
        nama,
        email,
        password,
        role
    )
    VALUES (
        p_id_user,
        p_nama,
        p_email,
        crypt(p_password, gen_salt('bf')),
        p_role
    );

    RETURN 'User berhasil dibuat';
END;
$$ LANGUAGE plpgsql;

-- READ USER
CREATE OR REPLACE FUNCTION get_all_users()
RETURNS TABLE (
    id_user VARCHAR,
    nama VARCHAR,
    email VARCHAR,
    role VARCHAR,
    is_active BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id_user,
        u.nama,
        u.email,
        u.role,
        u.is_active
    FROM inventori_user u
    WHERE u.is_active = TRUE
    ORDER BY u.created_at DESC;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_user_by_id(p_id_user VARCHAR)
RETURNS TABLE (
    id_user VARCHAR,
    nama VARCHAR,
    email VARCHAR,
    role VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT id_user, nama, email, role
    FROM inventori_user
    WHERE id_user = p_id_user;
END;
$$ LANGUAGE plpgsql;

-- LOGIN FUNCTION
CREATE OR REPLACE FUNCTION login_user(
    p_email VARCHAR,
    p_password TEXT
)
RETURNS TABLE (
    id_user VARCHAR,
    nama VARCHAR,
    email VARCHAR,
    role VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id_user,
        u.nama,
        u.email,
        u.role
    FROM inventori_user u
    WHERE u.email = p_email
      AND u.password = crypt(p_password, u.password)
      AND u.is_active = TRUE;

    -- kalau tidak ada hasil → return kosong (normal behavior)
END;
$$ LANGUAGE plpgsql;

-- UPDATE USER
CREATE OR REPLACE FUNCTION update_user(
    p_id_user VARCHAR,
    p_nama VARCHAR,
    p_email VARCHAR,
    p_role VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    UPDATE inventori_user
    SET 
        nama = p_nama,
        email = p_email,
        role = p_role
    WHERE id_user = p_id_user;

    RETURN 'User berhasil diupdate';
END;
$$ LANGUAGE plpgsql;

-- UPDATE PASSWORD
CREATE OR REPLACE FUNCTION update_password(
    p_id_user VARCHAR,
    p_password_baru TEXT
)
RETURNS TEXT AS $$
BEGIN
    UPDATE inventori_user
    SET password = crypt(p_password_baru, gen_salt('bf'))
    WHERE id_user = p_id_user;

    RETURN 'Password berhasil diupdate';
END;
$$ LANGUAGE plpgsql;

-- DELETE USER
CREATE OR REPLACE FUNCTION deactivate_user(p_id_user VARCHAR)
RETURNS TEXT AS $$
BEGIN
    UPDATE inventori_user
    SET is_active = FALSE
    WHERE id_user = p_id_user;

    RETURN 'User berhasil dinonaktifkan';
END;
$$ LANGUAGE plpgsql;

-- VALIDASI ROLE 


-- TRIGER
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated
BEFORE UPDATE ON inventori_user
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();