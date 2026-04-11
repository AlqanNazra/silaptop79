-- =============================================
-- 6. HASIL SAW
-- =============================================
CREATE TABLE hasil_saw (
    id_hasil VARCHAR(100) PRIMARY KEY,
    id_dss VARCHAR(100),
    tanggal_proses TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_dss) REFERENCES dss_proses(id_dss)
);

CREATE OR REPLACE FUNCTION buat_hasil_saw(f_id_dss VARCHAR(100))
RETURNS VOID AS $$
BEGIN
    INSERT INTO (id_hasil, id_dss, tanggal_proses)
    VALUES (f_generate_id('saw','hasil_saw'), f_id_dss, tanggal_proses TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION hapus_hasil_saw(f_id_dss VARCHAR(100), f_id_hasil VALUES(100))
RETURNS TEXT AS $$
BEGIN 
    DELETE FROM hasil_saw WHERE id_hasil = f_id_hasil;
    DELETE FROM dss_proses WHERE id_dss = f_id_dss;
    RETURNS 'Data bobot id' || id_dss || 'telah dihapus';
END;
$$ LANGUAGE plpgsql;