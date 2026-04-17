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
ALTER TABLE inventori_user
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN updated_at TIMESTAMP,
ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
ADD CONSTRAINT role_check
CHECK (role IN ('HC', 'IT', 'TALENT'));
ADD CONSTRAINT unique_email UNIQUE (email);

-- =============================================
-- 2. KRITERIA
-- =============================================
CREATE TABLE dss_kriteria (
    id_kriteria VARCHAR(100) PRIMARY KEY,
    nama_kriteria VARCHAR(255) NOT NULL,
    tipe_kriteria VARCHAR(20) CHECK (tipe_kriteria IN ('benefit','cost'))
);
ALTER TABLE dss_kriteria
ADD CONSTRAINT kriteria UNIQUE (nama_kriteria);

-- =============================================
-- 3. BOBOT KRITERIA (SWARA)
-- =============================================
CREATE TABLE dss_bobotkriteria (
    id_bobot VARCHAR(100) PRIMARY KEY,
    id_kriteria VARCHAR(100),
    role VARCHAR(100),
    nilai_bobot FLOAT CHECK (nilai_bobot >= 0),
    FOREIGN KEY (id_kriteria) REFERENCES kriteria(id_kriteria)
);

-- =============================================
-- 4. DSS PROSES
-- =============================================
CREATE TABLE dss_dssproses (
    id_dss VARCHAR(100) PRIMARY KEY,
    id_user VARCHAR(15),
    id_bobot VARCHAR(100),
    role_dss VARCHAR(100),
    jenis_dss VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_bobot) REFERENCES bobot_kriteria(id_bobot)
);

-- =============================================
-- 5. ALTERNATIF DSS
-- =============================================
CREATE TABLE dss_alternatifdss (
    id_alternatif VARCHAR(100) PRIMARY KEY,
    id_dss VARCHAR(100),
    id_laptop_pengadaan VARCHAR(100),
    id_laptop_inventori VARCHAR(100),
    sumber_data VARCHAR(100),
    FOREIGN KEY (id_dss) REFERENCES dss_proses(id_dss)
);

-- =============================================
-- 6. HASIL SAW
-- =============================================
CREATE TABLE dss_hasilsaw (
    id_hasil VARCHAR(100) PRIMARY KEY,
    id_dss VARCHAR(100),
    tanggal_proses TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_dss) REFERENCES dss_proses(id_dss)
);

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

-- =============================================
-- 8. PROCESSOR
-- =============================================
CREATE TABLE inventori_processor (
    id_processor SERIAL PRIMARY KEY,
    nama_processor VARCHAR(255),
    manufacturer VARCHAR(255),
    model VARCHAR(255),
    cores INTEGER CHECK (cores > 0),
    threads INTEGER CHECK (threads > 0),
    base_clock FLOAT CHECK (base_clock > 0),
    max_clock FLOAT CHECK (max_clock > 0),
    arsitektur VARCHAR(100),
    keterangan TEXT
);

-- =============================================
-- 9. RAM
-- =============================================
CREATE TABLE ram (
    id_ram SERIAL PRIMARY KEY,
    kapasitas_gb INTEGER CHECK (kapasitas_gb > 0),
    tipe VARCHAR(50),
    keterangan TEXT
);

-- =============================================
-- 10. STORAGE
-- =============================================
CREATE TABLE storage (
    id_storage SERIAL PRIMARY KEY,
    kapasitas_gb INTEGER CHECK (kapasitas_gb > 0),
    tipe VARCHAR(100)
);

-- =============================================
-- 11. LAPTOP PENGADAAN (SCRAPING)
-- =============================================
CREATE TABLE laptop_pengadaan (
    id_laptop_pengadaan VARCHAR(100) PRIMARY KEY,
    id_processor INTEGER,
    id_ram INTEGER,
    id_storage INTEGER,
    nama_laptop VARCHAR(255),
    harga INTEGER CHECK (harga > 0),
    gpu VARCHAR(255),
    ukuran_layar FLOAT CHECK (ukuran_layar > 0),
    baterai FLOAT CHECK (baterai > 0),
    berat FLOAT CHECK (berat > 0),,
    FOREIGN KEY (id_processor) REFERENCES processor(id_processor),
    FOREIGN KEY (id_ram) REFERENCES ram(id_ram),
    FOREIGN KEY (id_storage) REFERENCES storage(id_storage)
);

-- =============================================
-- 12. LAPTOP INVENTORI
-- =============================================
CREATE TABLE laptop_inventori (
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
-- =============================================
-- 13. PEMINJAMAN
-- =============================================
CREATE TABLE peminjaman (
    id_peminjaman VARCHAR(100) PRIMARY KEY,
    id_pengajuan VARCHAR(100),
    id_user VARCHAR(15),
    id_laptop_inventori VARCHAR(100),
    tanggal_pinjam DATE,
    tanggal_kembali DATE,
    status VARCHAR(50),
    keterangan TEXT,
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (id_laptop_inventori) REFERENCES laptop_inventori(id_laptop_inventori),
    FOREIGN KEY (id_pengajuan) REFERENCES pengajuan(id_pengajuan)
);

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

-- =============================================
--  15, PEngajuan
-- =============================================
CREATE TABLE pengajuan (
    id_pengajuan VARCHAR(100) PRIMARY KEY,
    id_user VARCHAR(15),
    kebutuhan_role VARCHAR(100),
    kebutuhan_requirement TEXT,
    bulan DATE,
    keterangan TEXT,
    perusahaan TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    tanggal_pengajuan TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tanggal_approval TIMESTAMP,
    approved_by VARCHAR(15),
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    FOREIGN KEY (approved_by) REFERENCES users(id_user)
);