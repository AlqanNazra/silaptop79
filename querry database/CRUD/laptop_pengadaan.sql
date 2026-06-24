-- =============================================
-- 11. LAPTOP PENGADAAN (SCRAPING)
-- =============================================
CREATE TABLE dss_laptoppengadaan (
    id_laptop_pengadaan VARCHAR(100) PRIMARY KEY,
    id_processor INTEGER,
    id_ram INTEGER,
    id_storage INTEGER,
    nama_laptop VARCHAR(255),
    harga INTEGER CHECK (harga > 0),
    gpu VARCHAR(255),
    ukuran_layar FLOAT CHECK (ukuran_layar > 0),
    baterai FLOAT CHECK (baterai > 0),
    berat FLOAT CHECK (berat > 0),
    FOREIGN KEY (id_processor) REFERENCES inventori_processor(id_processor),
    FOREIGN KEY (id_ram) REFERENCES inventori_ram(id_ram),
    FOREIGN KEY (id_storage) REFERENCES inventori_storage(id_storage)
);

CREATE OR REPLACE FUNCTION tambah_laptop_pengadaan(
    f_nama_laptop VARCHAR,
    f_harga INTEGER,
    f_gpu VARCHAR,
    f_ukuran_layar FLOAT,
    f_baterai FLOAT,
    f_id_processor VARCHAR,
    f_id_ram VARCHAR,
    f_id_storage VARCHAR,
    f_berat FLOAT
)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO dss_laptoppengadaan (
        id_laptop_pengadaan,
        id_processor,
        id_ram,
        id_storage,
        nama_laptop,
        harga,
        gpu,
        ukuran_layar,
        baterai,
        berat
    )
    VALUES (
        f_generate_id('LP','dss_laptoppengadaan','id_laptop_pengadaan'), -- sesuaikan!
        f_id_processor,
        f_id_ram,
        f_id_storage,
        f_nama_laptop,
        f_harga,
        f_gpu,
        f_ukuran_layar,
        f_baterai,
        f_berat
    );

    RETURN 'Insert berhasil';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION ambil_laptop_pengadaan()
RETURNS TABLE (
    id_laptop_pengadaan VARCHAR,
    nama_laptop VARCHAR,
    harga INTEGER,
    gpu VARCHAR,
    ukuran_layar FLOAT,
    baterai FLOAT,
    berat FLOAT,

    nama_processor VARCHAR,
    manufacturer VARCHAR,
    processor_model VARCHAR,
    cores INT,
    threads INT,
    benchmark_score INTEGER,
    ram_kapasitas INT,
    ram_tipe VARCHAR,
    storage_kapasitas INT,
    storage_tipe VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        lp.id_laptop_pengadaan,
        lp.nama_laptop,
        lp.harga,
        lp.gpu,
        lp.ukuran_layar,
        lp.baterai,
        lp.berat,
        pro.nama_processor,
        pro.manufacturer,
        pro.model,
        pro.cores,
        pro.threads,
        pro.benchmark_score,
        r.kapasitas_gb,
        r.tipe,
        s.kapasitas_gb,
        s.tipe
    FROM dss_laptoppengadaan lp
    LEFT JOIN inventori_processor pro ON lp.id_processor = pro.id_processor
    LEFT JOIN inventori_ram r ON lp.id_ram = r.id_ram
    LEFT JOIN inventori_storage s ON lp.id_storage = s.id_storage;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_laptop_pengadaan(f_id_laptop_pengadaan VARCHAR,f_nama_laptop VARCHAR,f_harga INTEGER,f_gpu VARCHAR,f_ukuran_layar FLOAT,f_baterai FLOAT)
RETURNS TEXT AS $$
BEGIN
    UPDATE dss_laptoppengadaan
    SET 
        nama_laptop = f_nama_laptop,
        harga = f_harga,
        gpu = f_gpu,
        ukuran_layar = f_ukuran_layar,
        baterai = f_baterai
    WHERE id_laptop_pengadaan = f_id_laptop_pengadaan;

    RETURN 'Data laptop pengadaan berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_spek_pengadaan(f_id_laptop_pengadaan VARCHAR,f_id_processor INTEGER,f_id_ram INTEGER,f_id_storage INTEGER)
RETURNS TEXT AS $$
BEGIN
    UPDATE dss_laptoppengadaan
    SET 
        id_processor = f_id_processor,
        id_ram = f_id_ram,
        id_storage = f_id_storage
    WHERE id_laptop_pengadaan = f_id_laptop_pengadaan;

    RETURN 'Spesifikasi berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_laptop_pengadaan(
    f_id_laptop_pengadaan VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM dss_laptoppengadaan
    WHERE id_laptop_pengadaan = f_id_laptop_pengadaan;

    RETURN 'Data laptop pengadaan berhasil dihapus!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_hasil_saw_pengadaan(
    f_id_hasil VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    id_laptop_pengadaan VARCHAR,
    nama_laptop VARCHAR,
    harga INTEGER,
    gpu VARCHAR,
    ukuran_layar FLOAT,
    baterai FLOAT,

    sumber_data VARCHAR,
    jenis_dss VARCHAR,
    role_dss VARCHAR,
    tanggal_proses TIMESTAMP,

    nilai_normalisasi FLOAT,
    nilai_preferensi FLOAT,
    ranking INTEGER
)
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        lp.id_laptop_pengadaan,
        lp.nama_laptop,
        lp.harga,
        lp.gpu,
        lp.ukuran_layar,
        lp.baterai,

        ad.sumber_data,
        dp.jenis_dss,
        dp.role_dss,
        hs.tanggal_proses,

        dhs.nilai_normalisasi,
        dhs.nilai_preferensi,
        dhs.ranking

    FROM dss_hasilsaw hs

    JOIN dss_detailhasilsaw dhs 
        ON hs.id_hasil = dhs.id_hasil

    JOIN dss_proses dp 
        ON hs.id_dss = dp.id_dss

    JOIN dss_alternatifdss ad 
        ON dp.id_dss = ad.id_dss

    LEFT JOIN dss_laptoppengadaan lp 
        ON ad.id_laptop_pengadaan = lp.id_laptop_pengadaan

    WHERE 
        f_id_hasil IS NULL 
        OR hs.id_hasil = f_id_hasil;
END;
$$ LANGUAGE plpgsql;