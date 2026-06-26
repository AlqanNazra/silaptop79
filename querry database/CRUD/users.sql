-- =============================================
-- 1. USERS
-- =============================================
CREATE TABLE inventori_user (
    id_user VARCHAR(15) PRIMARY KEY,
    nama VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

select * from inventori_user

-- Update database
ALTER TABLE inventori_user
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP,
ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS departemen VARCHAR(100) NOT NULL DEFAULT 'Non IT';
ALTER TABLE inventori_user
ADD CONSTRAINT role_check
CHECK (role IN ('HC', 'IT', 'TALENT'));

-- Ekstention 
CREATE EXTENSION IF NOT EXISTS pgcrypto;

select create_user

-- CREATE DATA
CREATE OR REPLACE FUNCTION create_user(
    p_nama VARCHAR,
    p_email VARCHAR,
    p_password TEXT,
    p_role VARCHAR,
    p_departemen VARCHAR DEFAULT 'Non IT'
)
RETURNS TEXT AS
$$
BEGIN
    -- Validasi email
    IF EXISTS (
        SELECT 1
        FROM inventori_user
        WHERE email = p_email
    ) THEN
        RETURN 'Email sudah digunakan';
    END IF;

    INSERT INTO inventori_user (
        id_user,
        nama,
        email,
        password,
        role,
        departemen
    )
    VALUES (
        f_generate_id('USR','inventori_user','id_user'),
        p_nama,
        p_email,
        crypt(p_password, gen_salt('bf')),
        p_role,
        p_departemen
    );

    RETURN 'User berhasil dibuat';
END;
$$
LANGUAGE plpgsql;

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
    SELECT u.id_user, u.nama, u.email, u.role
    FROM inventori_user u
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