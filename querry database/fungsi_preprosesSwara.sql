-- 1. Function Tambah Bobot dengan Versioning
CREATE OR REPLACE FUNCTION tambah_bobot_kriteria(
    p_id_role_tek UUID,
    p_id_kriteria UUID,
    p_nilai_bobot FLOAT
) RETURNS UUID AS $$
DECLARE
    v_new_id UUID := gen_random_uuid();
    v_versi INT;
BEGIN
    -- Nonaktifkan versi sebelumnya
    UPDATE bobot_kriteria 
    SET is_active = FALSE 
    WHERE id_role_teknologi = p_id_role_tek 
      AND id_kriteria = p_id_kriteria 
      AND is_active = TRUE;

    -- Tentukan versi baru
    SELECT COALESCE(MAX(versi), 0) + 1 INTO v_versi
    FROM bobot_kriteria
    WHERE id_role_teknologi = p_id_role_tek 
      AND id_kriteria = p_id_kriteria;

    -- Insert data baru
    INSERT INTO bobot_kriteria (id_bobot, id_role_teknologi, id_kriteria, nilai_bobot, versi, is_active, created_at)
    VALUES (v_new_id, p_id_role_tek, p_id_kriteria, p_nilai_bobot, v_versi, TRUE, NOW());

    RETURN v_new_id;
END;
$$ LANGUAGE plpgsql;

-- 2. Function Update SWARA Weight
CREATE OR REPLACE FUNCTION update_nilai_swara(
    p_id_bobot UUID,
    p_nilai_swara FLOAT
) RETURNS VOID AS $$
BEGIN
    UPDATE bobot_kriteria
    SET nilai_swara = p_nilai_swara
    WHERE id_bobot = p_id_bobot;
END;
$$ LANGUAGE plpgsql;

-- 3. Function Get Active Bobot (Role + Technology)
CREATE OR REPLACE FUNCTION get_bobot_role_teknologi(p_id_role_tek UUID)
RETURNS TABLE (
    id_bobot UUID,
    id_kriteria UUID,
    nama_kriteria VARCHAR,
    nilai_bobot FLOAT,
    nilai_swara FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT bk.id_bobot, bk.id_kriteria, k.nama, bk.nilai_bobot, bk.nilai_swara
    FROM bobot_kriteria bk
    JOIN kriteria k ON bk.id_kriteria = k.id_kriteria
    WHERE bk.id_role_teknologi = p_id_role_tek 
      AND bk.is_active = TRUE;
END;
$$ LANGUAGE plpgsql;

-- 4. Function Validasi Total Persentase Role Project
CREATE OR REPLACE FUNCTION validasi_total_bobot_project(p_id_proyek UUID)
RETURNS BOOLEAN AS $$
DECLARE
    v_total FLOAT;
BEGIN
    SELECT SUM(persentase_role) INTO v_total
    FROM project_role
    WHERE id_proyek = p_id_proyek;
    
    IF v_total > 1.0 THEN
        RAISE EXCEPTION 'Total persentase role proyek melebihi 1.0 (100%)';
    END IF;
    
    RETURN v_total = 1.0;
END;
$$ LANGUAGE plpgsql;