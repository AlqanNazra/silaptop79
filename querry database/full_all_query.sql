-- =============================================
-- 5. ALTERNATIF DSS
-- =============================================
CREATE TABLE alternatif_dss (
    id_alternatif VARCHAR(100) PRIMARY KEY,
    id_dss VARCHAR(100),
    id_laptop_pengadaan VARCHAR(100),
    id_laptop_inventori VARCHAR(100),
    sumber_data VARCHAR(100),
    FOREIGN KEY (id_dss) REFERENCES dss_proses(id_dss)
);


CREATE OR REPLACE FUNCTION tambah_alternatif_dss(T_id_alternatif VARCHAR(100),T_id_dss VARCHAR(100),T_id_laptop_pengadaan VARCHAR(100),T_id_laptop_invetori VARCHAR(100),T_sumber_data VARCHAR(100))
RETURNS VOID AS $$
BEGIN 
    INSERT INTO  alternatif_dss (id_alternatif,id_dss,id_laptop_pengadaan,id_laptop_invetori,sumber_data)
    VALUES (T_id_alternatif,T_id_dss,T_id_laptop_pengadaan,T_id_laptop_invetori,T_sumber_data)
END; 
$$ LANGUAGE plpgsql;

-- SELECT tambah_alternatif_dss ('ID_2', 'ID_D_2', "ID_P_2", "alternatif")

CREATE OR REPLACE FUNCTION cari_alternatif_dss (T_id_alternatif VARCHAR(100))
RETURNS TABLE (id_alternatif,id_dss,id_laptop_pengadaan,id_laptop_invetori,sumber_data) AS $$
BEGIN 
    RETURN QUERY
    SELECT a.id_alternatif,a.id_dss,a.id_laptop_pengadaan,a.id_laptop_invetori,a.sumber_data
    FROM alternatif_dss a
    WHERE a.id_alternatif = T_id_alternatif;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_alternatif_dss (T_id_alternatif VARCHAR(100))
RETURN TEXT AS $$
BEGIN
    DELETE FROM alternatif_dss WHERE id_alternatif = T_id_alternatif;
    RETURN 'DATA prdoduk id_dss' || id_alternatif || ' telah dihapus,';
END;
$$ LANGUAGE plpgsql;

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


-- =============================================
-- 4. DSS PROSES
-- =============================================
CREATE TABLE dss_proses (
    id_dss VARCHAR(100) PRIMARY KEY,
    id_user VARCHAR(15),
    id_bobot VARCHAR(100),
    role_dss VARCHAR(100),
    jenis_dss VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_bobot) REFERENCES bobot_kriteria(id_bobot)
);

CREATE Or REPLACE FUNCTION dss_proses (f_id_user VARCHAR(100), f_id_bobot VARCHAR(100), f_role_dss VARCHAR(100), f_jenis_dss VARCHAR(100))
RETURNS VOID AS $$
BEGIN
    INSERT INTO dss_proses(f_id_dss, id_user, id_bobot, role_dss, jenis_dss, created_at)
    VALUES (f_generate_id('dss','dss_proses'),f_id_user,f_id_bobot,f_role_dss,f_jenis_dss,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_semua_dss_prosess()
RETURNS TABLE (f_id_dss, id_user, id_bobot, role_dss, jenis_dss, created_at)
BEGIN
    RETURNS  QUERY
    SELECT *
    FROM dss_proses;
END;
$$ LANGUAGE plpgsql;


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

-- =============================================
-- 2. KRITERIA
-- =============================================
CREATE TABLE kriteria (
    id_kriteria VARCHAR(100) PRIMARY KEY,
    nama_kriteria VARCHAR(255) NOT NULL,
    tipe_kriteria VARCHAR(20) CHECK (tipe_kriteria IN ('benefit','cost'))
);

CREATE OR REPLACE tambah_kriteria (f_nama_kriteria VARCHAR(100),f_tipe_kriteria VARCHAR(20))
RETURNS VOID AS $$
BEGIN
    INSERT INTO kriteria(id_kriteria,nama_kriteria,tipe_kriteria)
    VALUES (f_generate_id('kriteria', 'kriteria')), f_nama_kriteria, f_tipe_kriteria
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE ambil_kriteria()
RETURNS TABLE (id_kriteria, nama_kriteria, tipe_kriteria)
BEGIN
    RETURNS  QUERY
    SELECT *
    FROM kriteria;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_kriteria (f_id_kriteria VARCHAR(100), f_nama_kriteria VARCHAR(100), f_tipe_kriteria VARCHAR(100))
RETURNS TEXT AS $$
BEGIN  
    UPDATE kriteria
    SET nama_kriteria = f_nama_kriteria, tipe_kriteria = f_tipe_kriteria
    WHERE id_kriteria = f_id_kriteria
    RETURNS 'data sudah diupdate'
END;
$$ LANGUAGE plpgsql;

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

-- =============================================
-- 8. PROCESSOR
-- =============================================
CREATE TABLE processor (
    id_processor SERIAL PRIMARY KEY,
    nama_processor VARCHAR(255),
    manufacturer VARCHAR(255),
    model VARCHAR(255),
    cores INTEGER,
    threads INTEGER,
    base_clock FLOAT,
    max_clock FLOAT,
    arsitektur VARCHAR(100),
    keterangan TEXT
);

CREATE OR REPLACE FUNCTION tambah_processor(
    f_nama_processor VARCHAR,
    f_manufacturer VARCHAR,
    f_model VARCHAR,
    f_cores INT,
    f_threads INT,
    f_base_clock FLOAT,
    f_max_clock FLOAT,
    f_arsitektur VARCHAR,
    f_keterangan TEXT
)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO processor (
        nama_processor,
        manufacturer,
        model,
        cores,
        threads,
        base_clock,
        max_clock,
        arsitektur,
        keterangan
    )
    VALUES (
        f_nama_processor,
        f_manufacturer,
        f_model,
        f_cores,
        f_threads,
        f_base_clock,
        f_max_clock,
        f_arsitektur,
        f_keterangan
    );

    RETURN 'Processor berhasil ditambahkan!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_processor()
RETURNS TABLE (
    id_processor INT,
    nama_processor VARCHAR,
    manufacturer VARCHAR,
    model VARCHAR,
    cores INT,
    threads INT,
    base_clock FLOAT,
    max_clock FLOAT,
    arsitektur VARCHAR,
    keterangan TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM processor;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_processor_by_id(f_id INT)
RETURNS TABLE (
    id_processor INT,
    nama_processor VARCHAR,
    manufacturer VARCHAR,
    model VARCHAR,
    cores INT,
    threads INT,
    base_clock FLOAT,
    max_clock FLOAT,
    arsitektur VARCHAR,
    keterangan TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM processor
    WHERE id_processor = f_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_processor(
    f_id INT,
    f_nama_processor VARCHAR,
    f_manufacturer VARCHAR,
    f_model VARCHAR,
    f_cores INT,
    f_threads INT,
    f_base_clock FLOAT,
    f_max_clock FLOAT,
    f_arsitektur VARCHAR,
    f_keterangan TEXT
)
RETURNS TEXT AS $$
BEGIN
    UPDATE processor
    SET 
        nama_processor = f_nama_processor,
        manufacturer = f_manufacturer,
        model = f_model,
        cores = f_cores,
        threads = f_threads,
        base_clock = f_base_clock,
        max_clock = f_max_clock,
        arsitektur = f_arsitektur,
        keterangan = f_keterangan
    WHERE id_processor = f_id;

    RETURN 'Processor berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_processor(f_id INT)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM processor
    WHERE id_processor = f_id;

    RETURN 'Processor berhasil dihapus!';
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- 9. RAM
-- =============================================
CREATE TABLE ram (
    id_ram SERIAL PRIMARY KEY,
    kapasitas_gb INTEGER,
    tipe VARCHAR(50),
    keterangan TEXT
);

CREATE OR REPLACE FUNCTION tambah_ram(
    f_kapasitas INT,
    f_tipe VARCHAR,
    f_keterangan TEXT
)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO ram (kapasitas_gb, tipe, keterangan)
    VALUES (f_kapasitas, f_tipe, f_keterangan);

    RETURN 'RAM berhasil ditambahkan!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_ram()
RETURNS TABLE (
    id_ram INT,
    kapasitas_gb INT,
    tipe VARCHAR,
    keterangan TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM ram;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_ram(
    f_id INT,
    f_kapasitas INT,
    f_tipe VARCHAR,
    f_keterangan TEXT
)
RETURNS TEXT AS $$
BEGIN
    UPDATE ram
    SET 
        kapasitas_gb = f_kapasitas,
        tipe = f_tipe,
        keterangan = f_keterangan
    WHERE id_ram = f_id;

    RETURN 'RAM berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_ram(f_id INT)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM ram
    WHERE id_ram = f_id;

    RETURN 'RAM berhasil dihapus!';
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- 14. RIWAYAT AKTIVITAS
-- =============================================
CREATE TABLE riwayat_aktivitas (
    id_aktivitas VARCHAR(100) PRIMARY KEY,
    id_user VARCHAR(15),
    id_laptop_inventori VARCHAR(100),
    jenis_aktivitas VARCHAR(100),
    keterangan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_laptop_inventori) REFERENCES laptop_inventori(id_laptop_inventori)
);

-- Update Table
ALTER TABLE riwayat_aktivitas
ADD COLUMN role_pengguna VARCHAR(50),
ADD COLUMN nama_aset VARCHAR(255);

-- CREATE (INSERT AKTIVITAS)
CREATE OR REPLACE FUNCTION create_riwayat_aktivitas(
    p_id_aktivitas VARCHAR,
    p_id_user VARCHAR,
    p_id_laptop VARCHAR,
    p_nama_aset VARCHAR,
    p_role VARCHAR,
    p_jenis_aktivitas VARCHAR,
    p_keterangan TEXT
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO riwayat_aktivitas (
        id_aktivitas,
        id_user,
        id_laptop_inventori,
        nama_aset,
        role_pengguna,
        jenis_aktivitas,
        keterangan,
        created_at
    )
    VALUES (
        p_id_aktivitas,
        p_id_user,
        p_id_laptop,
        p_nama_aset,
        p_role,
        p_jenis_aktivitas,
        p_keterangan,
        CURRENT_TIMESTAMP
    );
END;
$$ LANGUAGE plpgsql;

-- READ (GET DATA RIWAYAT)
-- Semua data
CREATE OR REPLACE FUNCTION get_all_riwayat()
RETURNS TABLE (
    id_aktivitas VARCHAR,
    id_user VARCHAR,
    id_laptop VARCHAR,
    nama_aset VARCHAR,
    role_pengguna VARCHAR,
    jenis_aktivitas VARCHAR,
    keterangan TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id_aktivitas,
        r.id_user,
        r.id_laptop_inventori,
        r.nama_aset,
        r.role_pengguna,
        r.jenis_aktivitas,
        r.keterangan,
        r.created_at
    FROM riwayat_aktivitas r
    ORDER BY r.created_at DESC;
END;
$$ LANGUAGE plpgsql;
-- Filter berdasarkan laptop (tracking aset)
CREATE OR REPLACE FUNCTION get_riwayat_by_laptop(p_id_laptop VARCHAR)
RETURNS TABLE (
    id_aktivitas VARCHAR,
    jenis_aktivitas VARCHAR,
    keterangan TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id_aktivitas,
        jenis_aktivitas,
        keterangan,
        created_at
    FROM riwayat_aktivitas
    WHERE id_laptop_inventori = p_id_laptop
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;
-- Filter berdasarkan user
CREATE OR REPLACE FUNCTION get_riwayat_by_user(p_id_user VARCHAR)
RETURNS TABLE (
    id_aktivitas VARCHAR,
    jenis_aktivitas VARCHAR,
    keterangan TEXT,
    created_at TIMESTAMP
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        id_aktivitas,
        jenis_aktivitas,
        keterangan,
        created_at
    FROM riwayat_aktivitas
    WHERE id_user = p_id_user
    ORDER BY created_at DESC;
END;
$$ LANGUAGE plpgsql;

-- UPDATE 
CREATE OR REPLACE FUNCTION update_riwayat_aktivitas(
    p_id_aktivitas VARCHAR,
    p_keterangan TEXT
)
RETURNS VOID AS $$
BEGIN
    UPDATE riwayat_aktivitas
    SET keterangan = p_keterangan
    WHERE id_aktivitas = p_id_aktivitas;
END;
$$ LANGUAGE plpgsql;

-- AUTO LOGGING
CREATE OR REPLACE FUNCTION log_update_laptop()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO riwayat_aktivitas (
        id_aktivitas,
        id_user,
        id_laptop_inventori,
        nama_aset,
        role_pengguna,
        jenis_aktivitas,
        keterangan
    )
    VALUES (
        gen_random_uuid()::text,
        NEW.updated_by,
        NEW.id_laptop_inventori,
        NEW.model,
        'HC',
        'UPDATE',
        'Update data laptop'
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triger
CREATE TRIGGER trg_log_update_laptop
AFTER UPDATE ON laptop_inventori
FOR EACH ROW
EXECUTE FUNCTION log_update_laptop();

-- =============================================
-- 10. STORAGE
-- =============================================
CREATE TABLE storage (
    id_storage SERIAL PRIMARY KEY,
    kapasitas_gb INTEGER,
    tipe VARCHAR(100)
);

CREATE OR REPLACE FUNCTION tambah_storage(
    f_kapasitas INT,
    f_tipe VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    INSERT INTO storage (kapasitas_gb, tipe)
    VALUES (f_kapasitas, f_tipe);

    RETURN 'Storage berhasil ditambahkan!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_storage()
RETURNS TABLE (
    id_storage INT,
    kapasitas_gb INT,
    tipe VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM storage;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_storage(
    f_id INT,
    f_kapasitas INT,
    f_tipe VARCHAR
)
RETURNS TEXT AS $$
BEGIN
    UPDATE storage
    SET 
        kapasitas_gb = f_kapasitas,
        tipe = f_tipe
    WHERE id_storage = f_id;

    RETURN 'Storage berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION hapus_storage(f_id INT)
RETURNS TEXT AS $$
BEGIN
    DELETE FROM storage
    WHERE id_storage = f_id;

    RETURN 'Storage berhasil dihapus!';
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- 1. USERS
-- =============================================
CREATE TABLE users (
    id_user VARCHAR(15) PRIMARY KEY,
    nama VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL
);

-- Update database
ALTER TABLE users
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP,
ADD COLUMN is_active BOOLEAN DEFAULT TRUE;

-- Ekstention 
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- CREATE DATA
CREATE OR REPLACE FUNCTION create_user(
    p_id_user VARCHAR,
    p_nama VARCHAR,
    p_email VARCHAR,
    p_password TEXT,
    p_role VARCHAR
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO users (
        id_user,
        nama,
        email,
        password,
        role,
        created_at
    )
    VALUES (
        p_id_user,
        p_nama,
        p_email,
        crypt(p_password, gen_salt('bf')), -- HASH PASSWORD
        p_role,
        CURRENT_TIMESTAMP
    );
END;
$$ LANGUAGE plpgsql;

-- READ USER
CREATE OR REPLACE FUNCTION get_all_users()
RETURNS TABLE (
    id_user VARCHAR,
    nama VARCHAR,
    email VARCHAR,
    role VARCHAR,
    is_active BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id_user,
        u.nama,
        u.email,
        u.role,
        u.is_active
    FROM users u
    WHERE u.is_active = TRUE;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_user_by_id(p_id_user VARCHAR)
RETURNS TABLE (
    id_user VARCHAR,
    nama VARCHAR,
    email VARCHAR,
    role VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT id_user, nama, email, role
    FROM users
    WHERE id_user = p_id_user;
END;
$$ LANGUAGE plpgsql;

-- LOGIN FUNCTION
CREATE OR REPLACE FUNCTION login_user(
    p_email VARCHAR,
    p_password TEXT
)
RETURNS TABLE (
    id_user VARCHAR,
    nama VARCHAR,
    email VARCHAR,
    role VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        u.id_user,
        u.nama,
        u.email,
        u.role
    FROM users u
    WHERE u.email = p_email
      AND u.password = crypt(p_password, u.password)
      AND u.is_active = TRUE;
END;
$$ LANGUAGE plpgsql;

-- UPDATE USER
CREATE OR REPLACE FUNCTION update_user(
    p_id_user VARCHAR,
    p_nama VARCHAR,
    p_email VARCHAR,
    p_role VARCHAR
)
RETURNS VOID AS $$
BEGIN
    UPDATE users
    SET 
        nama = p_nama,
        email = p_email,
        role = p_role,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_user = p_id_user;
END;
$$ LANGUAGE plpgsql;

-- UPDATE PASSWORD
CREATE OR REPLACE FUNCTION update_password(
    p_id_user VARCHAR,
    p_password_baru TEXT
)
RETURNS VOID AS $$
BEGIN
    UPDATE users
    SET password = crypt(p_password_baru, gen_salt('bf')),
        updated_at = CURRENT_TIMESTAMP
    WHERE id_user = p_id_user;
END;
$$ LANGUAGE plpgsql;

-- DELETE USER
CREATE OR REPLACE FUNCTION deactivate_user(p_id_user VARCHAR)
RETURNS VOID AS $$
BEGIN
    UPDATE users
    SET is_active = FALSE,
        updated_at = CURRENT_TIMESTAMP
    WHERE id_user = p_id_user;
END;
$$ LANGUAGE plpgsql;

-- VALIDASI ROLE 
ALTER TABLE users
ADD CONSTRAINT role_check
CHECK (role IN ('HC', 'IT', 'TALENT'));

-- TRIGER
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_users_updated
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();

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

        AND (ram = f_ram_kapasitas OR f_ram_kapasitas IS NULL)
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
$$ LANGUAGE plpgsql;0