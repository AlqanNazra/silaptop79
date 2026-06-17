-- 1. Function Tambah Bobot dengan Versioning
CREATE OR REPLACE FUNCTION tambah_bobot_kriteria(
    p_id_role_tek VARCHAR,
    p_id_kriteria VARCHAR,
    p_nilai_bobot FLOAT
) RETURNS VARCHAR AS $$
DECLARE
    v_new_id VARCHAR;
BEGIN
    v_new_id := f_generate_id('BBT', 'dss_bobotkriteria', 'id_bobot');

    -- Insert data baru
    INSERT INTO dss_bobotkriteria (id_bobot, role, kriteria_id, nilai_bobot)
    VALUES (v_new_id, p_id_role_tek, p_id_kriteria, p_nilai_bobot);

    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql;

-- 2. Function Update SWARA Weight
CREATE OR REPLACE FUNCTION update_nilai_swara(
    p_id_bobot VARCHAR,
    p_nilai_swara FLOAT
) RETURNS VOID AS $$
BEGIN
    UPDATE dss_bobotkriteria
    SET nilai_swara = p_nilai_swara
    WHERE id_bobot = p_id_bobot;
END;
$$ LANGUAGE plpgsql;

-- 3. Function Get Active Bobot (Role + Technology)
CREATE OR REPLACE FUNCTION get_bobot_role_teknologi(p_id_role_tek VARCHAR)
RETURNS TABLE (
    id_bobot VARCHAR,
    id_kriteria VARCHAR,
    nama_kriteria VARCHAR,
    nilai_bobot FLOAT,
    nilai_swara FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT bk.id_bobot, bk.kriteria_id AS id_kriteria, k.nama_kriteria, bk.nilai_bobot, bk.nilai_swara
    FROM dss_bobotkriteria bk
    JOIN dss_kriteria k ON bk.kriteria_id = k.id_kriteria
    WHERE bk.role = p_id_role_tek;
END;
$$ LANGUAGE plpgsql;

-- 4. Function Validasi Total Persentase Role Project
CREATE OR REPLACE FUNCTION validasi_total_bobot_project(p_id_proyek VARCHAR)
RETURNS BOOLEAN AS $$
DECLARE
    v_total FLOAT;
BEGIN
    SELECT SUM(persentase_role) INTO v_total
    FROM inventori_project_role
    WHERE id_proyek = p_id_proyek;
    
    IF v_total > 1.0 THEN
        RAISE EXCEPTION 'Total persentase role proyek melebihi 1.0 (100 percent)';
    END IF;
    
    RETURN v_total = 1.0;
END;
$$ LANGUAGE plpgsql;