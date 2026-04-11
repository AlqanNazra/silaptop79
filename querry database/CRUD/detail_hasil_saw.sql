-- =============================================
-- 7. DETAIL HASIL SAW
-- =============================================
CREATE TABLE detail_hasil_saw (
    id_detail VARCHAR(100) PRIMARY KEY,
    id_hasil VARCHAR(100),
    nilai_normalisasi FLOAT,
    nilai_preferensi FLOAT,
    ranking INTEGER,
    FOREIGN KEY (id_hasil) REFERENCES hasil_saw(id_hasil)
);

CREATE OR REPLACE tambah_detail_hasil_saw(f_id_hasil VARCHAR(100), f_nilai_normalisasi VARCHAR(100), f_nilai_preferensi VARCHAR(100), f_ranking INTEGER)
RETURNS VOID AS $$
BEGIN
    INSERT INTO detail_hasil_saw(id_detail, id_hasil, nilai_normalisasi, nilai_preferensi,ranking)
    VALUES (f_generate_id('detailsaw','detail_hasil_saw'), f_id_hasil, f_nilai_normalisasi, nilai_preferensi, ranking)
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE cari_data_detail_hasil_saw(f_id_detail VARCHAR(100))
RETURNS TABLE (id_detail, id_hasil, nilai_normalisasi, nilai_preferensi)
BEGIN 
    RETURNS QUERY
    SELECT d.id_detail,d.id_hasil,d.nilai_normalisasi,dd.nilai_preferensi
    FROM detail_hasil_saw d
    WHERE b.id_detail = f_id_bobot;
END;  
$$ LANGUAGE plpgsql;


CREATE OR REPLACE ambil_semua_data_detail_hasil_saw()
RETURNS TABLE (id_detail, id_hasil, nilai_normalisasi, nilai_preferensi)
BEGIN
    RETURNS  QUERY
    SELECT *
    FROM detail_hasil_saw;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE hapus_detail_hasil_saw(f_id_detail VARCHAR(100), f_id_hasil VARCHAR(100))
RETURNS TEXT AS $$
BEGIN
    DELETE From hasil_saw WHERE id_hasil = f_id_hasil;
    DELETE FROM detail_hasil_saw WHERE id_detail = f_id_detail;
    RETURNS 'Data Detail sudah dihapus';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_hasil_saw (f_id_detail VARCHAR(100), f_id_hasil VARCHAR(100))
RETURNS TABLE (id_detail,id_hasil,id_dss,id_alternatif,id_laptop_pengadaan,id_laptop_inventori)


