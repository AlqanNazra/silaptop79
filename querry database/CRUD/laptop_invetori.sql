-- =============================================
-- 12. LAPTOP INVENTORI
-- =============================================


CREATE OR REPLACE FUNCTION tambah_laptop_inventori(
    f_nama_laptop VARCHAR,
    f_model VARCHAR,
    f_os VARCHAR,
    f_kondisi VARCHAR,
    f_status VARCHAR,
    f_lokasi VARCHAR,
    f_id_processor VARCHAR, 
    f_id_ram VARCHAR,       
    f_id_storage VARCHAR,   
    f_ukuran_layar FLOAT,
    f_baterai FLOAT 
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO inventori_laptopinventori (
        id_laptop_inventori,
        no_inventori,
        nama_laptop,
        model,
        os,
        kondisi,
        status,
        lokasi,
        processor_id, 
        ram_id,
        storage_id,
        ukuran_layar,
        baterai -- Tambahkan kolom target
    )
    VALUES (
        f_generate_id('INV','inventori_laptopinventori','id_laptop_inventori'),
        'LTP-' || CAST(extract(epoch from now()) AS TEXT) || f_nama_laptop, 
        f_nama_laptop,
        f_model,
        f_os,
        f_kondisi,
        f_status,
        f_lokasi,
        NULLIF(f_id_processor, '')::bigint, 
        NULLIF(f_id_ram, '')::bigint,       
        NULLIF(f_id_storage, '')::bigint,   
        f_ukuran_layar,
        f_baterai -- Masukkan nilainya di sini
    );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_spek_laptop(f_id_laptop_inventori VARCHAR)
RETURNS TABLE (
    nama_processor VARCHAR,
    manufacturer VARCHAR,
    processor_model VARCHAR,
    cores INT,
    threads INT,
    processor_score INTEGER,
    ram_kapasitas INT,
    ram_tipe VARCHAR,
    storage_kapasitas INT,
    storage_tipe VARCHAR   -- <--- Koma di sini sudah dihapus
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pro.nama_processor,
        pro.manufacturer,
        pro.model,
        pro.cores,
        pro.threads,
        pro.processor_score,
        r.kapasitas_gb,
        r.tipe,
        s.kapasitas_gb,
        s.tipe
    FROM inventori_laptopinventori li
    LEFT JOIN inventori_processor pro ON li.id_processor = pro.id_processor -- Catatan: pastikan nama kolom foreign key-nya sesuai (li.id_processor atau li.processor_id)
    LEFT JOIN inventori_ram r ON li.id_ram = r.id_ram
    LEFT JOIN inventori_storage s ON li.id_storage = s.id_storage
    WHERE li.id_laptop_inventori = f_id_laptop_inventori;
END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS ambil_laptop_inventori();

CREATE OR REPLACE FUNCTION ambil_laptop_inventori()
RETURNS TABLE (
    id_laptop_inventori VARCHAR,
    no_inventori VARCHAR,
    nama_laptop VARCHAR,
    model VARCHAR,
    os VARCHAR,
    kondisi VARCHAR,
    status VARCHAR,
    lokasi VARCHAR,

    ukuran_layar FLOAT,
    baterai FLOAT,

    nama_processor VARCHAR,
    manufacturer VARCHAR,
    processor_model VARCHAR,
    cores INT,
    threads INT,
    processor_score INTEGER,

    ram_kapasitas INT,
    ram_tipe VARCHAR,

    storage_kapasitas INT,
    storage_tipe VARCHAR
)
AS $$
BEGIN
RETURN QUERY
SELECT
    li.id_laptop_inventori,
    li.no_inventori,
    li.nama_laptop,
    li.model,
    li.os,
    li.kondisi,
    li.status,
    li.lokasi,

    li.ukuran_layar,
    li.baterai,

    pro.nama_processor,
    pro.manufacturer,
    pro.model,
    pro.cores,
    pro.threads,
    pro.processor_score,

    r.kapasitas_gb,
    r.tipe,

    s.kapasitas_gb,
    s.tipe

FROM inventori_laptopinventori li

LEFT JOIN inventori_processor pro
    ON li.id_processor = pro.id_processor

LEFT JOIN inventori_ram r
    ON li.id_ram = r.id_ram

LEFT JOIN inventori_storage s
    ON li.id_storage = s.id_storage;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_hasil_saw_inventori(
    f_id_hasil VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    id_laptop_inventori VARCHAR,
    no_inventori VARCHAR,
    nama_laptop VARCHAR,
    model VARCHAR,
    os VARCHAR,
    kondisi VARCHAR,
    status VARCHAR,
    lokasi VARCHAR,
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
        li.id_laptop_inventori,
        li.no_inventori,
        li.nama_laptop,
        li.model,
        li.os,
        li.kondisi,
        li.status,
        li.lokasi,
        li.ukuran_layar,
        li.baterai,

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

    JOIN dss_dssproses dp 
        ON hs.id_dss = dp.id_dss

    JOIN dss_alternatifdss ad 
        ON dp.id_dss = ad.id_dss

    LEFT JOIN inventori_laptopinventori li 
        ON ad.id_laptop_inventori = li.id_laptop_inventori

    WHERE 
        f_id_hasil IS NULL 
        OR hs.id_hasil = f_id_hasil;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_kondisi_inventori (f_id_laptop_inventori VARCHAR(100), f_kondisi VARCHAR(100))
RETURNs TEXT AS $$
BEGIN
    UPDATE inventori_laptopinventori
    set kondisi = f_kondisi
    WHERE id_laptop_inventori = f_id_laptop_inventori;
    RETURN 'Kondisi berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_status_inventori (f_id_laptop_inventori VARCHAR(100), f_status VARCHAR(100), f_lokasi VARCHAR(100) DEFAULT NULL)
RETURNs TEXT AS $$
BEGIN
    UPDATE inventori_laptopinventori
    set status = f_status, lokasi = f_lokasi
    WHERE id_laptop_inventori = f_id_laptop_inventori;
    RETURN 'status berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_laptop_inventori (f_id_laptop_inventori VARCHAR)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM inventori_laptopinventori 
    WHERE id_laptop_inventori = f_id_laptop_inventori;
    RETURN 'Data inventori dengan ID ' || f_id_laptop_inventori || ' berhasil dihapus';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_spek_inventori(f_id_laptop_inventori VARCHAR,f_id_processor INTEGER,f_id_ram INTEGER,f_id_storage INTEGER)
RETURNS TEXT AS $$
BEGIN
    UPDATE inventori_laptopinventori
    SET 
        processor_id = f_id_processor,
        ram_id = f_id_ram,
        storage_id = f_id_storage
    WHERE id_laptop_inventori = f_id_laptop_inventori;

    RETURN 'Spesifikasi berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_detail_laptop_inventori(
    f_id_laptop VARCHAR
)
RETURNS TABLE (

    id_laptop_inventori VARCHAR,
    no_inventori VARCHAR,

    nama_laptop VARCHAR,
    model VARCHAR,
    os VARCHAR,

    kondisi VARCHAR,
    status VARCHAR,
    lokasi VARCHAR,

    ukuran_layar FLOAT,
    baterai FLOAT,

    nama_processor VARCHAR,
    manufacturer VARCHAR,
    processor_model VARCHAR,

    cores INT,
    threads INT,
    processor_score INTEGER,

    ram_kapasitas INT,
    ram_tipe VARCHAR,

    storage_kapasitas INT,
    storage_tipe VARCHAR

)
AS $$
BEGIN

RETURN QUERY

SELECT

    li.id_laptop_inventori,
    li.no_inventori,

    li.nama_laptop,
    li.model,
    li.os,

    li.kondisi,
    li.status,
    li.lokasi,

    li.ukuran_layar,
    li.baterai,

    pro.nama_processor,
    pro.manufacturer,
    pro.model,

    pro.cores,
    pro.threads,
    pro.processor_score,

    r.kapasitas_gb,
    r.tipe,

    s.kapasitas_gb,
    s.tipe

FROM inventori_laptopinventori li

LEFT JOIN inventori_processor pro
ON li.id_processor = pro.id_processor

LEFT JOIN inventori_ram r
ON li.id_ram = r.id_ram

LEFT JOIN inventori_storage s
ON li.id_storage = s.id_storage

WHERE li.id_laptop_inventori = f_id_laptop;

END;
$$ LANGUAGE plpgsql;