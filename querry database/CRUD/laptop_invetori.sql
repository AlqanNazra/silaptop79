-- =============================================
-- 12. LAPTOP INVENTORI
-- =============================================
CREATE TABLE inventori_laptopinventori (
    id_laptop_inventori VARCHAR(100) PRIMARY KEY,
    no_inventori VARCHAR(100) UNIQUE,
    nama_laptop VARCHAR(255),
    model VARCHAR(255),
    os VARCHAR(100),
    kondisi VARCHAR(50)     CHECK (kondisi IN ('baik','rusak ringan','rusak berat')),
    status VARCHAR(50) CHECK (status IN ('tersedia','dipinjam','rusak')),
    lokasi VARCHAR(255),
    id_processor INTEGER,
    id_ram INTEGER,
    id_storage INTEGER,
    ukuran_layar FLOAT,
    FOREIGN KEY (id_processor) REFERENCES processor(id_processor),
    FOREIGN KEY (id_ram) REFERENCES ram(id_ram),
    FOREIGN KEY (id_storage) REFERENCES storage(id_storage)
);

CREATE OR REPLACE FUNCTION tambah_laptop_inventori(
    f_nama_laptop VARCHAR,
    f_model VARCHAR,
    f_os VARCHAR,
    f_kondisi VARCHAR,
    f_status VARCHAR,
    f_lokasi VARCHAR,
    f_id_processor VARCHAR, -- Ubah ke VARCHAR
    f_id_ram VARCHAR,       -- Ubah ke VARCHAR
    f_id_storage VARCHAR,   -- Ubah ke VARCHAR
    f_ukuran_layar FLOAT
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
        processor_id, -- Gunakan suffix _id jika Django
        ram_id,
        storage_id,
        ukuran_layar
    )
    VALUES (
        f_generate_id('INV','inventori_laptopinventori','id_laptop_inventori'),
        'LTP-' || CAST(extract(epoch from now()) AS TEXT) || f_nama_laptop, -- Generate manual simpel
        f_nama_laptop,
        f_model,
        f_os,
        f_kondisi,
        f_status,
        f_lokasi,
        NULLIF(f_id_processor, '')::bigint,
        NULLIF(f_id_ram, '')::bigint,
        NULLIF(f_id_storage, '')::bigint,
        f_ukuran_layar
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
    ram_kapasitas INT,
    ram_tipe VARCHAR,
    storage_kapasitas INT,
    storage_tipe VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pro.nama_processor,
        pro.manufacturer,
        pro.model,
        pro.cores,
        pro.threads,
        r.kapasitas_gb,
        r.tipe,
        s.kapasitas_gb,
        s.tipe
    FROM inventori_laptopinventori li
    LEFT JOIN inventori_processor pro ON li.processor_id = pro.id_processor
    LEFT JOIN inventori_ram r ON li.ram_id = r.id_ram
    LEFT JOIN inventori_storage s ON li.storage_id = s.id_storage
    WHERE li.id_laptop_inventori = f_id_laptop_inventori;
END;
$$ LANGUAGE plpgsql;

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
    nama_processor VARCHAR,
    manufacturer VARCHAR,
    processor_model VARCHAR,
    cores INT,
    threads INT,
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
        pro.nama_processor,
        pro.manufacturer,
        pro.model,
        pro.cores,
        pro.threads,
        r.kapasitas_gb,
        r.tipe,
        s.kapasitas_gb,
        s.tipe

    FROM inventori_laptopinventori li

    LEFT JOIN inventori_processor pro ON li.processor_id = pro.id_processor
    LEFT JOIN inventori_ram r ON li.ram_id = r.id_ram
    LEFT JOIN inventori_storage s ON li.storage_id = s.id_storage;
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