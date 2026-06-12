-- =============================================
-- 4. DSS PROSES
-- =============================================
CREATE TABLE dss_dssproses (
    id_dss VARCHAR(100) PRIMARY KEY,
    id_user VARCHAR(15),
    id_bobot VARCHAR(100),
    role_dss VARCHAR(100),
    jenis_dss VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_bobot) REFERENCES bobot_kriteria(id_bobot)
);

CREATE OR REPLACE FUNCTION tambah_dss_proses (
    f_id_user VARCHAR,
    f_id_bobot VARCHAR,
    f_role_dss VARCHAR,
    f_jenis_dss VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO dss_dssproses(
        id_dss,
        id_user,
        id_bobot,
        role_dss,
        jenis_dss,
        created_at
    )
    VALUES (
        f_generate_id('DSS','dss_dssproses','id_dss'),
        f_id_user,
        f_id_bobot,
        f_role_dss,
        f_jenis_dss,
        CURRENT_TIMESTAMP
    );

    RETURN 'DSS proses berhasil ditambahkan';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION ambil_semua_dss_proses()
RETURNS TABLE (id_dss VARCHAR,id_user VARCHAR,id_bobot VARCHAR,role_dss VARCHAR,jenis_dss VARCHAR,created_at TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT d.id_dss,d.id_user,d.id_bobot,d.role_dss,d.jenis_dss,d.created_at
    FROM dss_dssproses d;
END;
$$ LANGUAGE plpgsql;
