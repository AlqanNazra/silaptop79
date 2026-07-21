CREATE OR REPLACE FUNCTION f_generate_id(
    prefix VARCHAR, 
    nama_tabel VARCHAR, 
    nama_kolom VARCHAR
)
RETURNS VARCHAR AS $$
DECLARE
    last_id VARCHAR;
    new_no INT;
    query_str TEXT;
BEGIN
    query_str := 'SELECT ' || quote_ident(nama_kolom) || 
                 ' FROM ' || quote_ident(nama_tabel) || 
                 ' WHERE ' || quote_ident(nama_kolom) || ' LIKE ' || quote_literal(prefix || '%') ||
                 ' ORDER BY ' || quote_ident(nama_kolom) || ' DESC LIMIT 1';
    
    EXECUTE query_str INTO last_id;

    IF last_id IS NULL OR last_id = '' THEN
        new_no := 1;
    ELSE
        -- Menggunakan regex untuk mengambil angka saja dari string ID
        -- Ini lebih aman daripada split_part jika ada banyak underscore
        BEGIN
            new_no := (substring(last_id FROM '[0-9]+$')::INT) + 1;
        EXCEPTION WHEN OTHERS THEN
            -- Jika gagal ekstrak angka, mulai dari 1
            new_no := 1;
        END;
    END IF;

    RETURN prefix || '_' || LPAD(new_no::TEXT, 4, '0');
END;
$$ LANGUAGE plpgsql;


-- =============================================
-- Generaete Nomber inventori 
-- =============================================

-- Sequence
CREATE SEQUENCE IF NOT EXISTS seq_no_inventori START 1;

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

DROP FUNCTION IF EXISTS getfilteredlaptopinventori(character varying,character varying,character varying,character varying,double precision,double precision,double precision,character varying,character varying,character varying,integer,integer,integer,integer,integer,integer,integer,character varying,integer,integer,integer,character varying);

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
    f_processor_score INT DEFAULT NULL,

    f_cores INT DEFAULT NULL,
    f_min_cores INT DEFAULT NULL,
    f_max_cores INT DEFAULT NULL,

    f_ram_kapasitas INT DEFAULT NULL,
    f_min_ram_kapasitas INT DEFAULT NULL,
    f_max_ram_kapasitas INT DEFAULT NULL,
    f_ram_tipe VARCHAR DEFAULT NULL,

    f_storage_kapasitas INT DEFAULT NULL,
    f_min_storage INT DEFAULT NULL,
    f_max_storage INT DEFAULT NULL,
    f_storage_tipe VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    id_laptop_inventori VARCHAR,
    kondisi VARCHAR,
    status VARCHAR,
    lokasi VARCHAR,
    ukuran_layar FLOAT,
    baterai FLOAT,
    nama_processor VARCHAR,
    manufacturer VARCHAR,
    processor_model VARCHAR,
    cores INT,
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
        li.kondisi,
        li.status,
        li.lokasi,
        li.ukuran_layar,
        li.baterai,
        li.nama_processor,
        p.manufacturer,       -- Diambil dari tabel processor
        p.model AS processor_model, -- Diambil dari tabel processor
        p.cores,              -- Diambil dari tabel processor
        p.processor_score,    -- Diambil dari tabel processor
        li.ram_kapasitas,
        li.ram_tipe,
        li.storage_kapasitas,
        li.storage_tipe
    FROM public.ambil_laptop_inventori() li
    LEFT JOIN public.inventori_processor p ON li.nama_processor = p.nama_processor-- JOIN DISINI

    WHERE
        -- IDENTITAS
        (f_id_laptop_inventori IS NULL OR li.id_laptop_inventori = f_id_laptop_inventori)

        -- STATUS & KONDISI
        AND (f_kondisi IS NULL OR li.kondisi = f_kondisi)
        AND (f_status IS NULL OR li.status = f_status)
        AND (f_lokasi IS NULL OR li.lokasi = f_lokasi)

        -- UKURAN LAYAR
        AND (f_ukuran_layar IS NULL OR li.ukuran_layar = f_ukuran_layar)
        AND (f_min_ukuran_layar IS NULL OR li.ukuran_layar >= f_min_ukuran_layar)
        AND (f_max_ukuran_layar IS NULL OR li.ukuran_layar <= f_max_ukuran_layar)

        -- PROCESSOR (Menggunakan alias 'p' dari tabel processor)
        AND (f_nama_processor IS NULL OR li.nama_processor = f_nama_processor)
        AND (f_manufacturer IS NULL OR p.manufacturer = f_manufacturer)
        AND (f_processor_model IS NULL OR p.model = f_processor_model)
        AND (f_processor_score IS NULL OR p.processor_score >= f_processor_score)

        -- CORES
        AND (f_cores IS NULL OR p.cores = f_cores)
        AND (f_min_cores IS NULL OR p.cores >= f_min_cores)
        AND (f_max_cores IS NULL OR p.cores <= f_max_cores)

        -- RAM
        AND (f_ram_kapasitas IS NULL OR li.ram_kapasitas >= f_min_ram_kapasitas)
        AND (f_min_ram_kapasitas IS NULL OR li.ram_kapasitas >= f_min_ram_kapasitas)
        AND (f_max_ram_kapasitas IS NULL OR li.ram_kapasitas <= f_max_ram_kapasitas)
        AND (f_ram_tipe IS NULL OR li.ram_tipe = f_ram_tipe)

        -- STORAGE
        AND (f_storage_kapasitas IS NULL OR li.storage_kapasitas >= f_min_storage)
        AND (f_min_storage IS NULL OR li.storage_kapasitas >= f_min_storage)
        AND (f_max_storage IS NULL OR li.storage_kapasitas <= f_max_storage)
        AND (f_storage_tipe IS NULL OR li.storage_tipe = f_storage_tipe);

END;
$$ LANGUAGE plpgsql;

DROP FUNCTION IF EXISTS getfilteredlaptoppengadaan(character varying,numeric,integer,integer,character varying,double precision,double precision,double precision,double precision,double precision,double precision,character varying,character varying,character varying,integer,integer,integer,integer,integer,integer,integer,character varying,integer,integer,integer,character varying);

-- FILTER PENGADAAN
CREATE OR REPLACE FUNCTION GetFilteredLaptopPengadaan(
    f_id_laptop_pengadaan VARCHAR DEFAULT NULL,

    f_harga NUMERIC DEFAULT NULL,
    f_min_harga INT DEFAULT NULL,
    f_max_harga INT DEFAULT NULL,

    f_gpu VARCHAR DEFAULT NULL,

    f_ukuran_layar FLOAT DEFAULT NULL,
    f_min_ukuran_layar FLOAT DEFAULT NULL,
    f_max_ukuran_layar FLOAT DEFAULT NULL,

    f_baterai FLOAT DEFAULT NULL,
    f_min_baterai FLOAT DEFAULT NULL,
    f_max_baterai FLOAT DEFAULT NULL,

    -- Processor
    f_nama_processor VARCHAR DEFAULT NULL,
    f_manufacturer VARCHAR DEFAULT NULL,
    f_processor_model VARCHAR DEFAULT NULL,
    f_cores INT DEFAULT NULL,
    f_min_cores INT DEFAULT NULL,
    f_max_cores INT DEFAULT NULL,
    f_processor_score INT DEFAULT NULL,

    -- RAM
    f_ram_kapasitas INT DEFAULT NULL,
    f_min_ram_kapasitas INT DEFAULT NULL,
    f_max_ram_kapasitas INT DEFAULT NULL,
    f_ram_tipe VARCHAR DEFAULT NULL,

    -- Storage
    f_storage_kapasitas INT DEFAULT NULL,
    f_min_storage INT DEFAULT NULL,
    f_max_storage INT DEFAULT NULL,
    f_storage_tipe VARCHAR DEFAULT NULL
)
RETURNS TABLE (
    id_laptop_pengadaan VARCHAR,
    harga INT,
    gpu VARCHAR,
    ukuran_layar FLOAT,
    baterai FLOAT,
    nama_processor VARCHAR,
    manufacturer VARCHAR,
    processor_model VARCHAR,
    cores INT,
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
        lp.id_laptop_pengadaan,
        lp.harga,
        lp.gpu,
        lp.ukuran_layar,
        lp.baterai,
        lp.nama_processor,
        p.manufacturer,       -- Diambil dari tabel processor
        p.model AS processor_model, -- Diambil dari tabel processor
        p.cores,              -- Diambil dari tabel processor
        p.processor_score,    -- Diambil dari tabel processor
        lp.ram_kapasitas,
        lp.ram_tipe,
        lp.storage_kapasitas,
        lp.storage_tipe
    FROM ambil_laptop_pengadaan() lp
    LEFT JOIN public.inventori_processor p
    ON lp.nama_processor = p.nama_processor
-- JOIN DISINI

    WHERE
        -- ID
        (f_id_laptop_pengadaan IS NULL OR lp.id_laptop_pengadaan = f_id_laptop_pengadaan)

        -- HARGA
        AND (f_harga IS NULL OR lp.harga = f_harga)
        AND (f_min_harga IS NULL OR lp.harga >= f_min_harga)
        AND (f_max_harga IS NULL OR lp.harga <= f_max_harga)

        -- GPU
        AND (f_gpu IS NULL OR lp.gpu ILIKE '%' || f_gpu || '%')

        -- LAYAR
        AND (f_ukuran_layar IS NULL OR lp.ukuran_layar = f_ukuran_layar)
        AND (f_min_ukuran_layar IS NULL OR lp.ukuran_layar >= f_min_ukuran_layar)
        AND (f_max_ukuran_layar IS NULL OR lp.ukuran_layar <= f_max_ukuran_layar)

        -- BATERAI
        AND (f_baterai IS NULL OR lp.baterai = f_baterai)
        AND (f_min_baterai IS NULL OR lp.baterai >= f_min_baterai)
        AND (f_max_baterai IS NULL OR lp.baterai <= f_max_baterai)

        -- PROCESSOR
        AND (f_nama_processor IS NULL OR lp.nama_processor ILIKE '%' || f_nama_processor || '%')
        AND (f_manufacturer IS NULL OR p.manufacturer = f_manufacturer)
        AND (f_processor_model IS NULL OR p.model ILIKE '%' || f_processor_model || '%')
        AND (f_processor_score IS NULL OR p.processor_score >= f_processor_score) -- Sudah diperbaiki ke alias 'p'

        -- CORES
        AND (f_cores IS NULL OR p.cores = f_cores)
        AND (f_min_cores IS NULL OR p.cores >= f_min_cores)
        AND (f_max_cores IS NULL OR p.cores <= f_max_cores)

        -- RAM
        AND (f_ram_kapasitas IS NULL OR lp.ram_kapasitas = f_min_ram_kapasitas)
        AND (f_min_ram_kapasitas IS NULL OR lp.ram_kapasitas >= f_min_ram_kapasitas)
        AND (f_max_ram_kapasitas IS NULL OR lp.ram_kapasitas <= f_max_ram_kapasitas)
        AND (f_ram_tipe IS NULL OR lp.ram_tipe = f_ram_tipe)

        -- STORAGE
        AND (f_storage_kapasitas IS NULL OR lp.storage_kapasitas = f_min_storage)
        AND (f_min_storage IS NULL OR lp.storage_kapasitas >= f_min_storage)
        AND (f_max_storage IS NULL OR lp.storage_kapasitas <= f_max_storage)
        AND (f_storage_tipe IS NULL OR lp.storage_tipe = f_storage_tipe);

END;
$$ LANGUAGE plpgsql;