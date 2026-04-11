-- =============================================
-- 4. DSS PROSES
-- =============================================
CREATE TABLE dss_proses (
    id_dss VARCHAR(100) PRIMARY KEY,
    id_user VARCHAR(15),
    id_bobot VARCHAR(100),
    role_dss VARCHAR(100),
    jenis_dss VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_bobot) REFERENCES bobot_kriteria(id_bobot)
);

CREATE Or REPLACE FUNCTION dss_proses (f_id_user VARCHAR(100), f_id_bobot VARCHAR(100), f_role_dss VARCHAR(100), f_jenis_dss VARCHAR(100))
RETURNS VOID AS $$
BEGIN
    INSERT INTO dss_proses(f_id_dss, id_user, id_bobot, role_dss, jenis_dss, created_at)
    VALUES (f_generate_id('dss','dss_proses'),f_id_user,f_id_bobot,f_role_dss,f_jenis_dss,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_semua_dss_prosess()
RETURNS TABLE (f_id_dss, id_user, id_bobot, role_dss, jenis_dss, created_at)
BEGIN
    RETURNS  QUERY
    SELECT *
    FROM dss_proses;
END;
$$ LANGUAGE plpgsql;

