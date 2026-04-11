-- =============================================
-- 12. LAPTOP INVENTORI
-- =============================================
CREATE TABLE laptop_inventori (
    id_laptop_inventori VARCHAR(100) PRIMARY KEY,
    no_inventori VARCHAR(100) UNIQUE,
    nama_laptop VARCHAR(255),
    model VARCHAR(255),
    os VARCHAR(100),
    kondisi VARCHAR(50),
    status VARCHAR(50),
    lokasi VARCHAR(255),
    id_processor INTEGER,
    id_ram INTEGER,
    id_storage INTEGER,
    ukuran_layar FLOAT,
    FOREIGN KEY (id_processor) REFERENCES processor(id_processor),
    FOREIGN KEY (id_ram) REFERENCES ram(id_ram),
    FOREIGN KEY (id_storage) REFERENCES storage(id_storage)
);

CREATE OR REPLACE FUNCTION tambah_laptop_invetori
(f_nama_laptop VARCHAR(255),f_model VARCHAR(255),f_os VARCHAR(100),f_kondisi VARCHAR(50),f_status VARCHAR(100),f_lokasi VARCHAR(100)
,f_id_processor INTEGER, f_id_ram INTEGER, f_id_storage INTEGER, f_ukuran_layar float)
RETURNS VOID AS $$
BEGIN
    INSERT INTO laptop_inventori (id_laptop_inventori,no_inventori,nama_laptop,model,os,kondisi,status,lokasi,id_processor,id_ram,id_storage,ukuran_layar)
    VALUES (f_generate_id('inventori'.'laptop_invetori'),generate_no_inventori(),f_nama_laptop,f_model,f_os,f_kondisi,f_status,f_lokasi,f_id_processor,id_ram,id_storage,f_ukuran_layar)
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_spek_laptop(f_id_laptop_invetori VARCHAR(100),f_id_processor VARCHAR(100),f_id_ram VARCHAR(100), f_id_storage VARCHAR(100))
RETURNs TABLE (id_laptop_inventori,manufacturer,model,cores,threads,kapasitas_gb,tipe,kapasitas_gb,tipe)
BEGIN
    SELECT 
    pro.nama_processor,
    pro.manufacturer,
    pro.model,
    pro.cores,
    pro.threads,

    r.kapasitas_gb,
    r.tipe,

    store.kapasitas_gb,
    store.tipe

    FROM bobot_kriteria bk
    JOIN processor pro
        ON f_id_laptop_invetori = pro.id_processor
    JOIN ram r
        ON f_id_laptop_invetori = r.id_ram
    JOIN storage
        ON f_id_laptop_invetori = store.id_storage
END;
$$ LANGUAGE plpgsql

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

    -- processor
    nama_processor VARCHAR,
    manufacturer VARCHAR,
    processor_model VARCHAR,
    cores INT,
    threads INT,

    -- RAM
    ram_kapasitas INT,
    ram_tipe VARCHAR,

    -- Storage
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

        -- processor
        pro.nama_processor,
        pro.manufacturer,
        pro.model,
        pro.cores,
        pro.threads,

        -- RAM
        r.kapasitas_gb,
        r.tipe,

        -- Storage
        s.kapasitas_gb,
        s.tipe

    FROM laptop_inventori li

    LEFT JOIN processor pro
        ON li.id_processor = pro.id_processor

    LEFT JOIN ram r
        ON li.id_ram = r.id_ram

    LEFT JOIN storage s
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

    FROM hasil_saw hs

    JOIN detail_hasil_saw dhs 
        ON hs.id_hasil = dhs.id_hasil

    JOIN dss_proses dp 
        ON hs.id_dss = dp.id_dss

    JOIN alternatif_dss ad 
        ON dp.id_dss = ad.id_dss

    LEFT JOIN laptop_inventori li 
        ON ad.id_laptop_inventori = li.id_laptop_inventori

    WHERE 
        f_id_hasil IS NULL 
        OR hs.id_hasil = f_id_hasil;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_kondisi_inventori (f_id_laptop_inventori VARCHAR(100), f_kondisi VARCHAR(100))
RETURNs TEXT AS $$
BEGIN
    UPDATE laptop_inventori
    set kondisi = f_kondisi
    WHERE id_laptop_inventori = f_id_laptop_inventori;
    RETURNS 'Kondisi berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_status_inventori (f_id_laptop_inventori VARCHAR(100), f_status VARCHAR(100), f_lokasi VARCHAR(100) DEFAULT NULL)
RETURNs TEXT AS $$
BEGIN
    UPDATE laptop_inventori
    set status = f_status, lokasi = f_lokasi
    WHERE id_laptop_inventori = f_id_laptop_inventori;
    RETURNS 'status berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_laptop_invetori (f_id_laptop_inventori VARCHAR(100))
RETURNs TEXT AS $$
BEGIN
    DELETE FROM laptop_inventori WHERE id_laptop_inventori = f_id_laptop_inventori
    RETURNS 'DATA bobot dengan id' || id_laptop_inventori || ' telah dihapus,';
END;
$$ LANGUAGE plpgsql

CREATE OR REPLACE FUNCTION update_spek_inventori(f_id_laptop_inventori VARCHAR,f_id_processor INTEGER,f_id_ram INTEGER,f_id_storage INTEGER)
RETURNS TEXT AS $$
BEGIN
    UPDATE laptop_inventori
    SET 
        id_processor = f_id_processor,
        id_ram = f_id_ram,
        id_storage = f_id_storage
    WHERE id_laptop_inventori = f_id_laptop_inventori;

    RETURN 'Spesifikasi berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;