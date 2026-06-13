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

select * from dss_detailhasilsaw

alter table dss_detailhasilsaw
rename column id_hasil_id to id_hasil

CREATE OR REPLACE FUNCTION  
tambah_detail_hasil_saw(f_id_hasil VARCHAR(100), f_nilai_normalisasi FLOAT, f_nilai_preferensi FLOAT, f_ranking INTEGER)
RETURNS VOID AS $$
BEGIN
    INSERT INTO dss_detailhasilsaw(id_detail, id_hasil, nilai_normalisasi, nilai_preferensi,ranking)
    VALUES (f_generate_id('DHS','dss_detailhasilsaw','id_detail'), f_id_hasil, f_nilai_normalisasi, f_nilai_preferensi, f_ranking);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cari_data_detail_hasil_saw(f_id_detail VARCHAR(100))
RETURNS TABLE (id_detail VARCHAR, id_hasil VARCHAR, nilai_normalisasi FLOAT, nilai_preferensi FLOAT, ranking INTEGER) AS $$
BEGIN 
    RETURN QUERY
    SELECT d.id_detail,d.id_hasil,d.nilai_normalisasi,d.nilai_preferensi,d.ranking
    FROM dss_detailhasilsaw d
    WHERE d.id_detail = f_id_detail;
END;  
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION  ambil_semua_data_detail_hasil_saw()
RETURNS TABLE (id_detail VARCHAR, id_hasil VARCHAR, nilai_normalisasi FLOAT, nilai_preferensi FLOAT, ranking INTEGER)
AS $$
BEGIN
    RETURN QUERY
    SELECT d.id_detail,d.id_hasil,d.nilai_normalisasi,d.nilai_preferensi,d.ranking
    FROM dss_detailhasilsaw d;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION hapus_detail_hasil_saw(
    f_id_detail VARCHAR
)
RETURNS TEXT AS $$
DECLARE 
    v_id_hasil VARCHAR;
BEGIN
    -- ambil id_hasil
    SELECT id_hasil INTO v_id_hasil
    FROM dss_detailhasilsaw
    WHERE id_detail = f_id_detail;

    -- DEBUG
    RAISE NOTICE 'ID HASIL: %', v_id_hasil;

    IF v_id_hasil IS NULL THEN
        RETURN 'ID hasil tidak ditemukan dari detail';
    END IF;

    -- hapus child
    DELETE FROM dss_detailhasilsaw
    WHERE id_detail = f_id_detail;

    -- cek apakah masih ada child
    IF NOT EXISTS (
        SELECT 1 
        FROM dss_detailhasilsaw
        WHERE id_hasil = v_id_hasil
    ) THEN
        DELETE FROM dss_hasilsaw
        WHERE id_hasil = v_id_hasil;

        RETURN 'Detail dan parent berhasil dihapus';
    ELSE
        RETURN 'Detail dihapus, tapi parent masih punya child lain';
    END IF;

END;
$$ LANGUAGE plpgsql;


