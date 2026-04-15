-- =============================================
-- 7. DETAIL HASIL SAW
-- =============================================
CREATE TABLE dss_detailhasilsaw (
    id_detail VARCHAR(100) PRIMARY KEY,
    id_hasil VARCHAR(100),
    nilai_normalisasi FLOAT,
    nilai_preferensi FLOAT,
    ranking INTEGER,
    FOREIGN KEY (id_hasil) REFERENCES hasil_saw(id_hasil)
);

CREATE OR REPLACE FUNCTION  
tambah_detail_hasil_saw(f_id_hasil VARCHAR(100), f_nilai_normalisasi FLOAT, f_nilai_preferensi FLOAT, f_ranking INTEGER)
RETURNS VOID AS $$
BEGIN
    INSERT INTO dss_detailhasilsaw(id_detail, id_hasil, nilai_normalisasi, nilai_preferensi,ranking)
    VALUES (f_generate_id('detailsaw','detail_hasil_saw'), f_id_hasil, f_nilai_normalisasi, f_nilai_preferensi, f_ranking);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cari_data_detail_hasil_saw(f_id_detail VARCHAR(100))
RETURNS TABLE (id_detail VARCHAR, id_hasil VARCHAR, nilai_normalisasi FLOAT, nilai_preferensi FLOAT, ranking INTEGER) AS $$
BEGIN 
    RETURN QUERY
    SELECT d.id_detail,d.id_hasil,d.nilai_normalisasi,d.nilai_preferensi,d.ranking
    FROM dss_detailhasilsaw d
    WHERE d.id_detail = f_id_bobot;
END;  
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION  ambil_semua_data_detail_hasil_saw()
RETURNS TABLE (id_detail VARCHAR, id_hasil VARCHAR, nilai_normalisasi FLOAT, nilai_preferensi FLOAT, ranking INTEGER)
AS $$
BEGIN
    RETURN QUERY
    SELECT id_detail,id_hasil,nilai_normalisasi,nilai_preferensi,ranking
    FROM dss_detailhasilsaw;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION hapus_detail_hasil_saw(f_id_detail VARCHAR)
RETURNS TEXT AS $$ DECLARE v_id_hasil VARCHAR;
BEGIN
    -- ambil id_hasil dulu
    SELECT id_hasil INTO v_id_hasil
    FROM dss_detailhasilsaw
    WHERE id_bobot = f_id_detail;

    -- hapus bobot dulu (child)
    DELETE FROM dss_detailhasilsaw
    WHERE id_detail = f_id_detail;

    -- hapus hasil (parent)
    DELETE FROM dss_detailhasilsaw
    WHERE id_hasil = v_id_hasil;

    RETURN 'detail dan hasil saw berhasil dihapus';
END;
$$ LANGUAGE plpgsql;


