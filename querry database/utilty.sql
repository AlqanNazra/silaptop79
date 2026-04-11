CREATE OR REPLACE FUNCTION f_generate_id(prefix VARCHAR, nama_tabel VARCHAR)
RETURNS VARCHAR AS $$
DECLARE
    last_id VARCHAR;
    new_no INT;
    final_id VARCHAR;
    query_str TEXT;
BEGIN
    -- 1. Cari ID terakhir dari tabel yang ditentukan secara dinamis
    -- Kita asumsikan nama kolom primary key-nya adalah 'id'
    -- Jika nama kolom PK berbeda-beda, kamu bisa menambah parameter ketiga untuk nama kolom
    query_str := 'SELECT id FROM ' || quote_ident(nama_tabel) || ' ORDER BY id DESC LIMIT 1';
    
    EXECUTE query_str INTO last_id;

    -- 2. Cek apakah tabel kosong atau belum ada ID
    IF last_id IS NULL THEN
        new_no := 1;
    ELSE
        -- Mengambil angka di belakang underscore (misal mobil_0001 -> ambil 0001)
        -- Lalu mengubahnya menjadi integer dan ditambah 1
        new_no := (split_part(last_id, '_', 2)::INT) + 1;
    END IF;

    -- 3. Format angka menjadi 4 digit (LPAD) dan gabungkan dengan prefix
    final_id := prefix || '_' || LPAD(new_no::TEXT, 4, '0');

    RETURN final_id;
END;
$$ LANGUAGE plpgsql;


-- =============================================
-- Generaete Nomber inventori 
-- =============================================

-- Sequence
CREATE SEQUENCE seq_no_inventori START 1;

--  Function 
CREATE OR REPLACE FUNCTION generate_no_inventori()
RETURNS TEXT AS $$
DECLARE
    new_number INT;
    formatted_number TEXT;
BEGIN
    new_number := nextval('seq_no_inventori');
    formatted_number := LPAD(new_number::TEXT, 4, '0');
    RETURN 'INV-' || TO_CHAR(NOW(), 'YYYYMM') || '-' || formatted_number;
END;
$$ LANGUAGE plpgsql;

-- Filter Inventori
CREATE OR REPLACE FUNCTION GetFilteredLaptopinventori(
    f_id_laptop_inventori VARCHAR DEFAULT NULL,
    f_kondisi VARCHAR DEFAULT NULL,
    f_status VARCHAR DEFAULT NULL,
    f_lokasi VARCHAR DEFAULT NULL,
    f_ukuran_layar FLOAT DEFAULT NULL,
    f_min_ukuran_layar FLOAT DEFAULT NULL,
    f_max_ukuran_layar FLOAT DEFAULT NULL,
    f_nama_processor VARCHAR DEFAULT NULL,
    f_manufacturer VARCHAR DEFAULT NULL,
    f_processor_model VARCHAR DEFAULT NULL,
    f_cores INT DEFAULT NULL,
    f_min_cores INT DEFAULT NULL,
    f_max_cores INT DEFAULT NULL,
    f_ram_kapasitas INT DEFAULT NULL,
    f_max_ram_kapasitas INT DEFAULT NULL,
    f_min_ram_kapasitas INT DEFAULT NULL,
    f_ram_tipe VARCHAR DEFAULT NULL,
    f_storage_kapasitas INT DEFAULT NULL,
    f_max_storage INT DEFAULT NULL,
    f_min_storage INT DEFAULT NULL,
    f_storage_tipe VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    id_laptop_inventori VARCHAR,
    kondisi VARCHAR,
    status VARCHAR,
    lokasi VARCHAR,
    ukuran_layar FLOAT,
    nama_processor VARCHAR,
    manufacturer VARCHAR,
    processor_model VARCHAR,
    cores INT,
    ram INT,
    ram_tipe VARCHAR,
    storage_kapasitas INT,
    storage_tipe VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM ambil_laptop_inventori()
    WHERE 
        (id_laptop_inventori = f_id_laptop_inventori OR f_id_laptop_inventori IS NULL)
        AND (kondisi = f_kondisi OR f_kondisi IS NULL)
        AND (status = f_status OR f_status IS NULL)
        AND (lokasi = f_lokasi OR f_lokasi IS NULL)

        AND (ukuran_layar = f_ukuran_layar OR f_ukuran_layar IS NULL)
        AND (ukuran_layar <= f_max_ukuran_layar OR f_max_ukuran_layar IS NULL)
        AND (ukuran_layar >= f_min_ukuran_layar OR f_min_ukuran_layar IS NULL)

        AND (nama_processor = f_nama_processor OR f_nama_processor IS NULL)
        AND (manufacturer = f_manufacturer OR f_manufacturer IS NULL)
        AND (processor_model = f_processor_model OR f_processor_model IS NULL)

        AND (cores = f_cores OR f_cores IS NULL)
        AND (cores <= f_max_cores OR f_max_cores IS NULL)
        AND (cores >= f_min_cores OR f_min_cores IS NULL)

        AND (ram = f_ram_kapasitas OR f_ram_kapasitas IS NULL)+
        AND (ram <= f_max_ram_kapasitas OR f_max_ram_kapasitas IS NULL)
        AND (ram >= f_min_ram_kapasitas OR f_min_ram_kapasitas IS NULL)
        AND (ram_tipe = f_ram_tipe OR f_ram_tipe IS NULL)

        AND (storage_kapasitas = f_storage_kapasitas OR f_storage_kapasitas IS NULL)
        AND (storage_kapasitas <= f_max_storage OR f_max_storage IS NULL)
        AND (storage_kapasitas >= f_min_storage OR f_min_storage IS NULL)
        AND (storage_tipe = f_storage_tipe OR f_storage_tipe IS NULL);
END;
$$ LANGUAGE plpgsql;

-- FILTER PENGADAAN
CREATE OR REPLACE FUNCTION GetFilteredLaptopPengadaan(
    f_id_laptop_pengadaan VARCHAR DEFAULT NULL,
    f_harga NUMERIC DEFAULT NULL,
    f_min_harga NUMERIC DEFAULT NULL,
    f_max_harga NUMERIC DEFAULT NULL,
    f_gpu VARCHAR DEFAULT NULL,

    f_ukuran_layar FLOAT DEFAULT NULL,
    f_min_ukuran_layar FLOAT DEFAULT NULL,
    f_max_ukuran_layar FLOAT DEFAULT NULL,

    f_baterai INT DEFAULT NULL,
    f_min_baterai INT DEFAULT NULL,
    f_max_baterai INT DEFAULT NULL,

    -- Processor
    f_nama_processor VARCHAR DEFAULT NULL,
    f_manufacturer VARCHAR DEFAULT NULL,
    f_processor_model VARCHAR DEFAULT NULL,
    f_cores INT DEFAULT NULL,
    f_min_cores INT DEFAULT NULL,
    f_max_cores INT DEFAULT NULL,

    -- RAM
    f_ram_kapasitas INT DEFAULT NULL,
    f_max_ram_kapasitas INT DEFAULT NULL,
    f_min_ram_kapasitas INT DEFAULT NULL,
    f_ram_tipe VARCHAR DEFAULT NULL,

    -- Storage
    f_storage_kapasitas INT DEFAULT NULL,
    f_max_storage INT DEFAULT NULL,
    f_min_storage INT DEFAULT NULL,
    f_storage_tipe VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    id_laptop_pengadaan VARCHAR,
    harga NUMERIC,
    gpu VARCHAR,
    ukuran_layar FLOAT,
    baterai INT,
    nama_processor VARCHAR,
    manufacturer VARCHAR,
    processor_model VARCHAR,
    cores INT,
    ram_kapasitas INT,
    ram_tipe VARCHAR,
    storage_kapasitas INT,
    storage_tipe VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM ambil_laptop_pengadaan()
    WHERE
        (id_laptop_pengadaan = f_id_laptop_pengadaan OR f_id_laptop_pengadaan IS NULL)

        AND (harga = f_harga OR f_harga IS NULL)
        AND (harga <= f_max_harga OR f_max_harga IS NULL)
        AND (harga >= f_min_harga OR f_min_harga IS NULL)

        AND (gpu = f_gpu OR f_gpu IS NULL)

        AND (ukuran_layar = f_ukuran_layar OR f_ukuran_layar IS NULL)
        AND (ukuran_layar <= f_max_ukuran_layar OR f_max_ukuran_layar IS NULL)
        AND (ukuran_layar >= f_min_ukuran_layar OR f_min_ukuran_layar IS NULL)

        AND (baterai = f_baterai OR f_baterai IS NULL)
        AND (baterai <= f_max_baterai OR f_max_baterai IS NULL)
        AND (baterai >= f_min_baterai OR f_min_baterai IS NULL)

        AND (nama_processor = f_nama_processor OR f_nama_processor IS NULL)
        AND (manufacturer = f_manufacturer OR f_manufacturer IS NULL)
        AND (processor_model = f_processor_model OR f_processor_model IS NULL)

        AND (cores = f_cores OR f_cores IS NULL)
        AND (cores <= f_max_cores OR f_max_cores IS NULL)
        AND (cores >= f_min_cores OR f_min_cores IS NULL)

        AND (ram_kapasitas = f_ram_kapasitas OR f_ram_kapasitas IS NULL)
        AND (ram_kapasitas <= f_max_ram_kapasitas OR f_max_ram_kapasitas IS NULL)
        AND (ram_kapasitas >= f_min_ram_kapasitas OR f_min_ram_kapasitas IS NULL)
        AND (ram_tipe = f_ram_tipe OR f_ram_tipe IS NULL)

        AND (storage_kapasitas = f_storage_kapasitas OR f_storage_kapasitas IS NULL)
        AND (storage_kapasitas <= f_max_storage OR f_max_storage IS NULL)
        AND (storage_kapasitas >= f_min_storage OR f_min_storage IS NULL)
        AND (storage_tipe = f_storage_tipe OR f_storage_tipe IS NULL);
END;
$$ LANGUAGE plpgsql;