ALTER TABLE inventori_laptopinventori 
    ALTER COLUMN id_processor TYPE VARCHAR(50),
    ALTER COLUMN id_ram TYPE VARCHAR(50),
    ALTER COLUMN id_storage TYPE VARCHAR(50);
	
SELECT tambah_processor('Intel Core i3','Intel','i3-1115G4',2,4,3.0,4.1,'x64',45,'Entry Level Office');
SELECT tambah_processor('Intel Core i5','Intel','i5-1135G7',4,8,2.4,4.2,'x64',65,'Mid Range Developer');
SELECT tambah_processor('AMD Ryzen 5','AMD','5500U',6,12,2.1,4.0,'x64',75,'Developer Workstation');
SELECT tambah_processor('Intel Core i7','Intel','i7-1165G7',4,8,2.8,4.7,'x64',85,'High Performance');
SELECT tambah_processor('Apple M1','Apple','M1 8-Core',8,8,3.2,3.2,'ARM',95,'Premium Silicon');
-- 5 RAM
SELECT tambah_ram(8, 'DDR4', 'Standard');
SELECT tambah_ram(16, 'DDR4', 'High Speed');
SELECT tambah_ram(32, 'DDR4', 'Workstation');
SELECT tambah_ram(8, 'LPDDR4X', 'Soldered');
SELECT tambah_ram(16, 'LPDDR5', 'Next Gen');

-- 5 Storage
SELECT tambah_storage(256, 'SSD NVMe');
SELECT tambah_storage(512, 'SSD NVMe');
SELECT tambah_storage(1024, 'SSD NVMe');
SELECT tambah_storage(512, 'SATA SSD');
SELECT tambah_storage(1024, 'HDD 7200RPM');

-- Menggunakan loop untuk efisiensi (Simulasi data berbeda)
TRUNCATE TABLE dss_laptoppengadaan;

DO $$ 
DECLARE
    v_brand TEXT;
    v_gpu TEXT;
    v_layar FLOAT;
    v_berat FLOAT;
BEGIN
    FOR i IN 1..20 LOOP
        -- Logika Variasi
        v_brand := (ARRAY['ASUS ROG', 'Lenovo Legion', 'HP Victus', 'MacBook Air', 'Dell XPS'])[floor(random() * 5 + 1)];
        v_gpu := (ARRAY['RTX 3050', 'RTX 4060', 'Intel Iris Xe', 'AMD Radeon', 'RTX 3060'])[floor(random() * 5 + 1)];
        v_layar := (ARRAY[13.3, 14.0, 15.6, 16.0])[floor(random() * 4 + 1)];
        v_berat := (1.1 + (random() * 1.5))::numeric(2,1); -- Range 1.1kg - 2.6kg

        PERFORM tambah_laptop_pengadaan(
            (v_brand || ' Series ' || i)::VARCHAR,              -- 1. f_nama_laptop
            (8000000 + (floor(random() * 20) * 500000))::INTEGER, -- 2. f_harga
            v_gpu::VARCHAR,                                     -- 3. f_gpu
            v_layar::FLOAT,                                     -- 4. f_ukuran_layar
            (4000.0 + (floor(random() * 4) * 1000))::FLOAT,     -- 5. f_baterai
            ('PROS_000' || ((i % 5) + 1))::VARCHAR,             -- 6. f_id_processor
            ('RAM_000' || ((i % 5) + 1))::VARCHAR,              -- 7. f_id_ram
            ('STORE_000' || ((i % 5) + 1))::VARCHAR,            -- 8. f_id_storage
            v_berat::FLOAT                                      -- 9. f_berat
        );
    END LOOP;
END $$;
-- Menggunakan loop untuk efisiensi

TRUNCATE TABLE inventori_laptopinventori cascade;
select * from inventori_laptopinventori

DO $$
DECLARE
    v_kondisi TEXT;
    v_status TEXT;
    v_lokasi TEXT;
    v_os TEXT;
    v_model TEXT;
    v_baterai FLOAT;
BEGIN
    FOR i IN 1..20 LOOP
        -- Logika Variasi (Disesuaikan dengan CHECK constraint huruf kecil)
        v_kondisi := (ARRAY['baik', 'rusak ringan'])[floor(random() * 2 + 1)];
        v_status  := (ARRAY['tersedia', 'dipinjam', 'rusak'])[floor(random() * 3 + 1)];
        
        -- Variasi OS, Lokasi, Model, dan Baterai
        v_lokasi  := (ARRAY['Gudang Pusat', 'Kantor Bandung', 'Kantor Jakarta', 'Remote'])[floor(random() * 4 + 1)];
        v_os      := (ARRAY['Windows 10', 'Windows 11', 'macOS Sonoma', 'Ubuntu 22.04'])[floor(random() * 4 + 1)];
        v_model   := (ARRAY['ThinkPad', 'Latitude', 'EliteBook', 'Vostro'])[floor(random() * 4 + 1)];
        v_baterai := (4000.0 + (floor(random() * 4) * 1000))::FLOAT; -- Range 4000 - 7000 mAh

        -- Memanggil fungsi dengan parameter terbaru
        PERFORM tambah_laptop_inventori(
            (v_model || ' Business ' || i)::VARCHAR, 
            (v_model || '-' || (100 + i))::VARCHAR, 
            v_os::VARCHAR, 
            v_kondisi::VARCHAR, 
            v_status::VARCHAR, 
            v_lokasi::VARCHAR, 
            ('PROS_000' || ((i % 5) + 1))::VARCHAR, 
            ('RAM_000' || ((i % 5) + 1))::VARCHAR, 
            ('STORE_000' || ((i % 5) + 1))::VARCHAR, 
            (ARRAY[12.5, 13.0, 14.0, 15.0])[floor(random() * 4 + 1)]::FLOAT,
            v_baterai                                                        -- Tambahan parameter baterai
        );
    END LOOP;
END $$;



select * from inventori_ram
select * from inventori_processor
select * from inventori_storage
select * from inventori_laptopinventori
select * from dss_laptoppengadaan

select * from dss_kriteria
select * from dss_bobotkriteria

alter table dss_laptoppengadaan
rename column id_processor_id to id_processor

alter table dss_laptoppengadaan
rename column id to id_ram

alter table dss_laptoppengadaan
rename column id to id_storage

alter table inventori_laptopinventori
rename column processor_id to id_processor

alter table inventori_laptopinventori
rename column ram_id to id_ram

alter table inventori_laptopinventori
rename column storage_id to id_storage

drop function tambah_laptop_pengadaan

-- =====================================================
-- SEEDER KRITERIA + BOBOT KRITERIA
-- =====================================================

DO $$
DECLARE
    v_id_processor VARCHAR;
    v_id_ram VARCHAR;
    v_id_storage VARCHAR;
    v_id_berat VARCHAR;
    v_id_layar VARCHAR;
    v_id_baterai VARCHAR;

    -- Tambahkan variabel penampung ID Role Teknologi
    v_id_bnd VARCHAR; -- Backend Developer
    v_id_fnd VARCHAR; -- Frontend Developer
    v_id_mbl VARCHAR; -- Mobile Developer
    v_id_qae VARCHAR; -- QA Engineer
    v_id_aie VARCHAR; -- AI Engineer
BEGIN

    -- =====================================
    -- KRITERIA (Tetap sama)
    -- =====================================
    v_id_processor := tambah_kriteria('processor', 'benefit', 'hardware');
    v_id_ram       := tambah_kriteria('ram', 'benefit', 'hardware');
    v_id_storage   := tambah_kriteria('storage', 'benefit', 'hardware');
    v_id_berat     := tambah_kriteria('berat', 'cost', 'fisik');
    v_id_layar     := tambah_kriteria('layar', 'benefit', 'fisik');
    v_id_baterai   := tambah_kriteria('baterai', 'benefit', 'fisik');

    -- =====================================
    -- GET ID DARI TABLE ROLE_TEKNOLOGI
    -- (Mencari ID ROLETEK_xxx berdasarkan nama role di inventori_role)
    -- =====================================
    SELECT rt.id_role_teknologi INTO v_id_bnd FROM role_teknologi rt JOIN inventori_role r ON rt.id_role = r.id_role WHERE r.nama_role = 'Backend Developer' LIMIT 1;
    SELECT rt.id_role_teknologi INTO v_id_fnd FROM role_teknologi rt JOIN inventori_role r ON rt.id_role = r.id_role WHERE r.nama_role = 'Frontend Developer' LIMIT 1;
    SELECT rt.id_role_teknologi INTO v_id_mbl FROM role_teknologi rt JOIN inventori_role r ON rt.id_role = r.id_role WHERE r.nama_role = 'Mobile Developer' LIMIT 1;
    SELECT rt.id_role_teknologi INTO v_id_qae FROM role_teknologi rt JOIN inventori_role r ON rt.id_role = r.id_role WHERE r.nama_role = 'QA Engineer' LIMIT 1;
    SELECT rt.id_role_teknologi INTO v_id_aie FROM role_teknologi rt JOIN inventori_role r ON rt.id_role = r.id_role WHERE r.nama_role = 'AI Engineer' LIMIT 1;

    -- =====================================
    -- BACKEND DEVELOPER
    -- =====================================
    PERFORM tambah_bobot_kriteria(v_id_bnd, v_id_processor, 0.35);
    PERFORM tambah_bobot_kriteria(v_id_bnd, v_id_ram, 0.25);
    PERFORM tambah_bobot_kriteria(v_id_bnd, v_id_storage, 0.15);
    PERFORM tambah_bobot_kriteria(v_id_bnd, v_id_berat, 0.05);
    PERFORM tambah_bobot_kriteria(v_id_bnd, v_id_layar, 0.10);
    PERFORM tambah_bobot_kriteria(v_id_bnd, v_id_baterai, 0.10);

    -- =====================================
    -- FRONTEND DEVELOPER
    -- =====================================
    PERFORM tambah_bobot_kriteria(v_id_fnd, v_id_processor, 0.20);
    PERFORM tambah_bobot_kriteria(v_id_fnd, v_id_ram, 0.20);
    PERFORM tambah_bobot_kriteria(v_id_fnd, v_id_storage, 0.10);
    PERFORM tambah_bobot_kriteria(v_id_fnd, v_id_berat, 0.10);
    PERFORM tambah_bobot_kriteria(v_id_fnd, v_id_layar, 0.30);
    PERFORM tambah_bobot_kriteria(v_id_fnd, v_id_baterai, 0.10);

    -- =====================================
    -- MOBILE DEVELOPER
    -- =====================================
    PERFORM tambah_bobot_kriteria(v_id_mbl, v_id_processor, 0.25);
    PERFORM tambah_bobot_kriteria(v_id_mbl, v_id_ram, 0.40);
    PERFORM tambah_bobot_kriteria(v_id_mbl, v_id_storage, 0.15);
    PERFORM tambah_bobot_kriteria(v_id_mbl, v_id_berat, 0.05);
    PERFORM tambah_bobot_kriteria(v_id_mbl, v_id_layar, 0.05);
    PERFORM tambah_bobot_kriteria(v_id_mbl, v_id_baterai, 0.10);

    -- =====================================
    -- QA ENGINEER
    -- =====================================
    PERFORM tambah_bobot_kriteria(v_id_qae, v_id_processor, 0.20);
    PERFORM tambah_bobot_kriteria(v_id_qae, v_id_ram, 0.20);
    PERFORM tambah_bobot_kriteria(v_id_qae, v_id_storage, 0.15);
    PERFORM tambah_bobot_kriteria(v_id_qae, v_id_berat, 0.15);
    PERFORM tambah_bobot_kriteria(v_id_qae, v_id_layar, 0.15);
    PERFORM tambah_bobot_kriteria(v_id_qae, v_id_baterai, 0.15);

    -- =====================================
    -- AI ENGINEER
    -- =====================================
    PERFORM tambah_bobot_kriteria(v_id_aie, v_id_processor, 0.40);
    PERFORM tambah_bobot_kriteria(v_id_aie, v_id_ram, 0.30);
    PERFORM tambah_bobot_kriteria(v_id_aie, v_id_storage, 0.15);
    PERFORM tambah_bobot_kriteria(v_id_aie, v_id_berat, 0.05);
    PERFORM tambah_bobot_kriteria(v_id_aie, v_id_layar, 0.05);
    PERFORM tambah_bobot_kriteria(v_id_aie, v_id_baterai, 0.05);

END $$;

SELECT *
FROM dss_laptoppengadaan
LIMIT 5;

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'dss_bobotkriteria'
ORDER BY ordinal_position;
s-- =====================================================
-- ROLE
-- =====================================================

SELECT tambah_role(
    'Frontend Developer',
    8,
    256,
    60
);

SELECT tambah_role(
    'Backend Developer',
    16,
    512,
    75
);

SELECT tambah_role(
    'Mobile Developer',
    16,
    512,
    80
);

SELECT tambah_role(
    'QA Engineer',
    8,
    256,
    65
);

SELECT tambah_role(
    'AI Engineer',
    32,
    1024,
    90
);

-- =====================================================
-- TEKNOLOGI
-- =====================================================

SELECT tambah_teknologi(
    'ReactJS',
    'Frontend'
);

SELECT tambah_teknologi(
    'Spring Boot',
    'Backend'
);

SELECT tambah_teknologi(
    'Flutter',
    'Mobile'
);

SELECT tambah_teknologi(
    'Selenium',
    'Testing'
);

SELECT tambah_teknologi(
    'PyTorch',
    'Artificial Intelligence'
);

-- =====================================================
-- ROLE TEKNOLOGI
-- =====================================================
select * from inventori_teknologi
select * from inventori_role


SELECT tambah_role_teknologi(
    'ROLE_0001',
    'TEK_0001'
);

SELECT tambah_role_teknologi(
    'ROLE_0002',
    'TEK_0002'
);

SELECT tambah_role_teknologi(
    'ROLE_0003',
    'TEK_0003'
);

SELECT tambah_role_teknologi(
    'ROLE_0004',
    'TEK_0004'
);

SELECT tambah_role_teknologi(
    'ROLE_0005',
    'TEK_0005'
);

-- =====================================================
-- PROYEK
-- =====================================================

SELECT tambah_proyek(
    'Sistem Informasi Akademik',
    'Universitas XYZ',
    '2026-01-01',
    '2026-08-30'
);

SELECT tambah_proyek(
    'Mobile Banking App',
    'Bank Nasional',
    '2026-02-01',
    '2026-12-31'
);

SELECT tambah_proyek(
    'AI Resume Screening',
    'NTI Indonesia',
    '2026-03-01',
    '2026-11-30'
);

-- =====================================================
-- PROJECT ROLE
-- =====================================================

-- =====================================
-- Sistem Informasi Akademik
-- =====================================

select * from inventori_proyek
select * from inventori_role
select * from inventori_project_role

-- Sistem Informasi Akademik (Misal ID Proyeknya: PRYK_0001)
SELECT tambah_project_role('PRYK_0001', 'ROLE_0001', 0.40); -- Backend Developer
SELECT tambah_project_role('PRYK_0001', 'ROLE_0003', 0.20); -- QA Engineer

-- Mobile Banking App (Misal ID Proyeknya: PRYK_0002)
SELECT tambah_project_role('PRYK_0002', 'ROLE_0004', 0.50); -- Mobile Developer
SELECT tambah_project_role('PRYK_0002', 'ROLE_0001', 0.30); -- Backend Developer
SELECT tambah_project_role('PRYK_0002', 'ROLE_0003', 0.20); -- QA Engineer

-- AI Resume Screening (Misal ID Proyeknya: PRYK_0003)
SELECT tambah_project_role('PRYK_0003', 'ROLE_0005', 0.60); -- AI Engineer
SELECT tambah_project_role('PRYK_0003', 'ROLE_0001', 0.25); -- Backend Developer
SELECT tambah_project_role('PRYK_0003', 'ROLE_0002', 0.15); -- Frontend Developer

ALTER TABLE inventori_project_role 
    rename column proyek_id to id_processor,
    rename column role_id to id_processor

alter table inventori_project_role
rename column proyek_id to id_proyek

alter table inventori_project_role
    rename column role_id to id_role

CREATE EXTENSION IF NOT EXISTS pgcrypto;

DO $$
DECLARE
    v_nama TEXT;
    v_email TEXT;
    v_role TEXT;
    v_roles TEXT[] := ARRAY['hc', 'talent', 'it infrastruktur'];
    v_status TEXT;
BEGIN
    FOR i IN 1..10 LOOP
        -- 1. Membuat variasi Nama dan Email agar unik
        v_nama := 'Karyawan ' || i;
        v_email := 'user' || i || '@perusahaan.com';
        
        -- 2. Memilih role secara acak dari 3 pilihan yang ditentukan (hc, talent, it infrastruktur)
        v_role := v_roles[floor(random() * 3 + 1)];

        -- 3. Mengeksekusi fungsi create_user
        -- Parameter ke-1 diisi '' karena di dalam fungsi diganti oleh f_generate_id
        SELECT create_user(
            ''::VARCHAR,              -- 1. p_id_user (formalitas)
            v_nama::VARCHAR,          -- 2. p_nama
            v_email::VARCHAR,         -- 3. p_email
            'PasswordSecure123'::TEXT,-- 4. p_password (akan otomatis di-crypt di fungsi)
            v_role::VARCHAR           -- 5. p_role
        ) INTO v_status;

        -- Opsional: Menampilkan log di konsol messages untuk memantau proses
        RAISE NOTICE 'Proses data ke-%: Nama=% , Role=% -> Hasil: %', i, v_nama, v_role, v_status;
    END LOOP;
END $$;

select * from role_teknologi
ALTER TABLE dss_dssproses 
    rename column id_user_id to id_user
ALTER TABLE dss_dssproses 
    rename column id_bobot_id to id_bobot

ALTER TABLE dss_bobotkriteria 
    rename column id_kriteria_id to id_kriteria

SELECT *
FROM dss_bobotkriteria

SELECT *
FROM ambil_kriteria()
WHERE id_role_teknologi = 'ROLETEK_0002';

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'dss_bobotkriteria';

ALTER TABLE dss_bobotkriteria 
ADD CONSTRAINT fk_bobot_role_teknologi 
FOREIGN KEY (id_role_teknologi) REFERENCES role_teknologi(id_role_teknologi);

CREATE TABLE dss_bobotkriteria_backup AS
SELECT *
FROM dss_bobotkriteria;

SELECT *
FROM dss_bobotkriteria
LIMIT 5;

ALTER TABLE dss_bobotkriteria
ADD COLUMN id_role VARCHAR(20);

UPDATE dss_bobotkriteria bk
SET id_role = rt.id_role
FROM role_teknologi rt
WHERE bk.id_role_teknologi = rt.id_role_teknologi;

SELECT
id_bobot,
id_role_teknologi,
id_role
FROM dss_bobotkriteria
LIMIT 20;

SELECT conname
FROM pg_constraint
WHERE conrelid='dss_bobotkriteria'::regclass;

ALTER TABLE dss_bobotkriteria
DROP CONSTRAINT dss_bobotkriteria_id_role_teknologi_fkey;

ALTER TABLE dss_bobotkriteria
ADD CONSTRAINT fk_bobot_role
FOREIGN KEY(id_role)
REFERENCES inventori_role(id_role);

ALTER TABLE dss_bobotkriteria
DROP COLUMN id_role_teknologi;

SELECT *
FROM ambil_kriteria()
WHERE id_role = 'ROLE_0002';

TRUNCATE dss_bobotkriteria CASCADE;