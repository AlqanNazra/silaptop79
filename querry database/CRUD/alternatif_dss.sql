-- =============================================
-- 5. ALTERNATIF DSS
-- =============================================
CREATE TABLE alternatif_dss (
    id_alternatif VARCHAR(100) PRIMARY KEY,
    id_dss VARCHAR(100),
    id_laptop_pengadaan VARCHAR(100),
    id_laptop_inventori VARCHAR(100),
    sumber_data VARCHAR(100),
    FOREIGN KEY (id_dss) REFERENCES dss_proses(id_dss)
);


CREATE OR REPLACE FUNCTION tambah_alternatif_dss(T_id_alternatif VARCHAR(100),T_id_dss VARCHAR(100),T_id_laptop_pengadaan VARCHAR(100),T_id_laptop_inventori VARCHAR(100),T_sumber_data VARCHAR(100))
RETURNS VOID AS $$
BEGIN 
    INSERT INTO  alternatif_dss (id_alternatif,id_dss,id_laptop_pengadaan,id_laptop_invetori,sumber_data)
    VALUES (T_id_alternatif,T_id_dss,T_id_laptop_pengadaan,T_id_laptop_invetori,T_sumber_data);
END; 
$$ LANGUAGE plpgsql;

-- SELECT tambah_alternatif_dss ('ID_2', 'ID_D_2', "ID_P_2", "alternatif")

CREATE OR REPLACE FUNCTION cari_alternatif_dss (
    T_id_alternatif VARCHAR(100)
)
RETURNS TABLE (
    id_alternatif VARCHAR,
    id_dss VARCHAR,
    id_laptop_pengadaan VARCHAR,
    id_laptop_inventori VARCHAR,
    sumber_data VARCHAR
) AS $$
BEGIN 
    RETURN QUERY
    SELECT 
        a.id_alternatif,
        a.id_dss,
        a.id_laptop_pengadaan,
        a.id_laptop_inventori,
        a.sumber_data
    FROM alternatif_dss a
    WHERE a.id_alternatif = T_id_alternatif;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_alternatif_dss (T_id_alternatif VARCHAR(100))
RETURNS TEXT AS $$
BEGIN
    DELETE FROM alternatif_dss WHERE id_alternatif = T_id_alternatif;
    RETURN 'Data alternatif dengan ID ' || T_id_alternatif  || ' berhasil dihapus';
END;
$$ LANGUAGE plpgsql;