-- 5 Processor
SELECT tambah_processor('Intel Core i7', 'Intel', 'i7-1165G7', 4, 8, 2.8, 4.7, 'x64', 'High Performance');
SELECT tambah_processor('Intel Core i5', 'Intel', 'i5-1135G7', 4, 8, 2.4, 4.2, 'x64', 'Mid Range');
SELECT tambah_processor('AMD Ryzen 7', 'AMD', '5800U', 8, 16, 1.9, 4.4, 'x64', 'Efficient Multi-core');
SELECT tambah_processor('AMD Ryzen 5', 'AMD', '5500U', 6, 12, 2.1, 4.0, 'x64', 'Mainstream');
SELECT tambah_processor('Apple M1', 'Apple', 'M1 8-Core', 8, 8, 3.2, 3.2, 'ARM', 'Silicon');

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
            (v_brand || ' Series ' || i)::VARCHAR, 
            (8000000 + (floor(random() * 20) * 500000))::INTEGER, -- Harga 8jt - 18jt
            v_gpu::VARCHAR, 
            v_layar::FLOAT, 
            (4000.0 + (floor(random() * 4) * 1000))::FLOAT, -- Baterai 4000-7000 mAh
            ('PROS_000' || ((i % 5) + 1))::VARCHAR, 
            ('RAM_000' || ((i % 5) + 1))::VARCHAR, 
            ('STORE_000' || ((i % 5) + 1))::VARCHAR, 
            v_berat::FLOAT
        );
    END LOOP;
END $$;
-- Menggunakan loop untuk efisiensi

TRUNCATE TABLE inventori_laptopinventori cascade;

DO $$
DECLARE
    v_kondisi TEXT;
    v_status TEXT;
    v_lokasi TEXT;
    v_os TEXT;
    v_model TEXT;
BEGIN
    FOR i IN 1..20 LOOP
        -- Logika Variasi
        v_kondisi := (ARRAY['Baik', 'Rusak Ringan', 'Baru'])[floor(random() * 3 + 1)];
        v_status := (ARRAY['Tersedia', 'Dipinjam', 'Maintenance'])[floor(random() * 3 + 1)];
        v_lokasi := (ARRAY['Gudang Pusat', 'Kantor Bandung', 'Kantor Jakarta', 'Remote'])[floor(random() * 4 + 1)];
        v_os := (ARRAY['Windows 10', 'Windows 11', 'macOS Sonoma', 'Ubuntu 22.04'])[floor(random() * 4 + 1)];
        v_model := (ARRAY['ThinkPad', 'Latitude', 'EliteBook', 'Vostro'])[floor(random() * 4 + 1)];

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
            (ARRAY[12.5, 13.0, 14.0, 15.0])[floor(random() * 4 + 1)]::FLOAT
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
rename column id_ram_id to id_ram

alter table dss_laptoppengadaan
rename column id_storage_id to id_storage

alter table inventori_laptopinventori
rename column id_processor_id to id_processor

alter table inventori_laptopinventori
rename column id_ram_id to id_ram

alter table inventori_laptopinventori
rename column id_storage_id to id_storage

drop function tambah_laptop_pengadaan

DO $$ 
DECLARE 
    v_id_processor VARCHAR;
    v_id_ram VARCHAR;
    v_id_storage VARCHAR;
    v_id_berat VARCHAR;
    v_id_layar VARCHAR;
    v_id_baterai VARCHAR;
BEGIN
    -- 1. INPUT 6 KRITERIA UTAMA & SIMPAN ID-NYA
    v_id_processor := tambah_kriteria('processor', 'benefit', 'hardware');
    v_id_ram       := tambah_kriteria('ram', 'benefit', 'hardware');
    v_id_storage   := tambah_kriteria('storage', 'benefit', 'hardware');
    v_id_berat     := tambah_kriteria('berat', 'cost', 'fisik');
    v_id_layar     := tambah_kriteria('layar', 'benefit', 'fisik');
    v_id_baterai   := tambah_kriteria('baterai', 'benefit', 'fisik');

    -- 2. INPUT BOBOT UNTUK 10 ROLE (Setiap role memiliki total bobot 1.0)
    
    -- Role: Backend (.NET/Python) -> Prioritas: Processor & RAM
    PERFORM tambah_bobot_kriteria(v_id_processor, 'Backend Developer', 0.35);
    PERFORM tambah_bobot_kriteria(v_id_ram,       'Backend Developer', 0.25);
    PERFORM tambah_bobot_kriteria(v_id_storage,   'Backend Developer', 0.15);
    PERFORM tambah_bobot_kriteria(v_id_berat,     'Backend Developer', 0.05);
    PERFORM tambah_bobot_kriteria(v_id_layar,     'Backend Developer', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_baterai,   'Backend Developer', 0.10);

    -- Role: Frontend (CSS/React) -> Prioritas: Layar & RAM
    PERFORM tambah_bobot_kriteria(v_id_processor, 'Frontend Developer', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_ram,       'Frontend Developer', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_storage,   'Frontend Developer', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_berat,     'Frontend Developer', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_layar,     'Frontend Developer', 0.30);
    PERFORM tambah_bobot_kriteria(v_id_baterai,   'Frontend Developer', 0.10);

    -- Role: Data Scientist (AI/Python) -> Prioritas: Processor & RAM Tinggi
    PERFORM tambah_bobot_kriteria(v_id_processor, 'Data Scientist', 0.40);
    PERFORM tambah_bobot_kriteria(v_id_ram,       'Data Scientist', 0.30);
    PERFORM tambah_bobot_kriteria(v_id_storage,   'Data Scientist', 0.15);
    PERFORM tambah_bobot_kriteria(v_id_berat,     'Data Scientist', 0.05);
    PERFORM tambah_bobot_kriteria(v_id_layar,     'Data Scientist', 0.05);
    PERFORM tambah_bobot_kriteria(v_id_baterai,   'Data Scientist', 0.05);

    -- Role: Mobile Developer (Android/Kotlin) -> Prioritas: RAM (Emulators)
    PERFORM tambah_bobot_kriteria(v_id_processor, 'Mobile Developer', 0.25);
    PERFORM tambah_bobot_kriteria(v_id_ram,       'Mobile Developer', 0.40);
    PERFORM tambah_bobot_kriteria(v_id_storage,   'Mobile Developer', 0.15);
    PERFORM tambah_bobot_kriteria(v_id_berat,     'Mobile Developer', 0.05);
    PERFORM tambah_bobot_kriteria(v_id_layar,     'Mobile Developer', 0.05);
    PERFORM tambah_bobot_kriteria(v_id_baterai,   'Mobile Developer', 0.10);

    -- Role: UI/UX Designer -> Prioritas: Layar & Berat (Mobilitas)
    PERFORM tambah_bobot_kriteria(v_id_processor, 'UIUX Designer', 0.15);
    PERFORM tambah_bobot_kriteria(v_id_ram,       'UIUX Designer', 0.15);
    PERFORM tambah_bobot_kriteria(v_id_storage,   'UIUX Designer', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_berat,     'UIUX Designer', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_layar,     'UIUX Designer', 0.30);
    PERFORM tambah_bobot_kriteria(v_id_baterai,   'UIUX Designer', 0.10);

    -- Role: DevOps / SRE -> Prioritas: Storage & Baterai
    PERFORM tambah_bobot_kriteria(v_id_processor, 'DevOps', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_ram,       'DevOps', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_storage,   'DevOps', 0.25);
    PERFORM tambah_bobot_kriteria(v_id_berat,     'DevOps', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_layar,     'DevOps', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_baterai,   'DevOps', 0.15);

    -- Role: Office Work (HR/Finance) -> Prioritas: Baterai, Berat, Harga (Cost-Effective)
    PERFORM tambah_bobot_kriteria(v_id_processor, 'Office Work', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_ram,       'Office Work', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_storage,   'Office Work', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_berat,     'Office Work', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_layar,     'Office Work', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_baterai,   'Office Work', 0.20);

    -- Role: QA Engineer -> Prioritas: Balance
    PERFORM tambah_bobot_kriteria(v_id_processor, 'QA Engineer', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_ram,       'QA Engineer', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_storage,   'QA Engineer', 0.15);
    PERFORM tambah_bobot_kriteria(v_id_berat,     'QA Engineer', 0.15);
    PERFORM tambah_bobot_kriteria(v_id_layar,     'QA Engineer', 0.15);
    PERFORM tambah_bobot_kriteria(v_id_baterai,   'QA Engineer', 0.15);

    -- Role: Database Administrator -> Prioritas: Storage & RAM
    PERFORM tambah_bobot_kriteria(v_id_processor, 'DBA', 0.20);
    PERFORM tambah_bobot_kriteria(v_id_ram,       'DBA', 0.25);
    PERFORM tambah_bobot_kriteria(v_id_storage,   'DBA', 0.35);
    PERFORM tambah_bobot_kriteria(v_id_berat,     'DBA', 0.05);
    PERFORM tambah_bobot_kriteria(v_id_layar,     'DBA', 0.05);
    PERFORM tambah_bobot_kriteria(v_id_baterai,   'DBA', 0.10);

    -- Role: Project Manager -> Prioritas: Berat & Baterai (High Mobility)
    PERFORM tambah_bobot_kriteria(v_id_processor, 'Project Manager', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_ram,       'Project Manager', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_storage,   'Project Manager', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_berat,     'Project Manager', 0.30);
    PERFORM tambah_bobot_kriteria(v_id_layar,     'Project Manager', 0.10);
    PERFORM tambah_bobot_kriteria(v_id_baterai,   'Project Manager', 0.30);

END $$;

select * from dss_bobotkriteria
SELECT * 
FROM cari_bobot_kriteria_by_roles(
    ARRAY['Backend Developer', 'Frontend Developer']
);

drop function cari_bobot_kriteria_by_roles

CREATE OR REPLACE FUNCTION cari_bobot_kriteria_by_roles(
    f_roles VARCHAR[]
)
RETURNS TABLE (
    id_bobot VARCHAR,
    id_kriteria VARCHAR,
    nama_kriteria VARCHAR,
    tipe_kriteria VARCHAR,
    role VARCHAR,
    nilai_bobot FLOAT
) AS $$
BEGIN 
    RETURN QUERY
    SELECT 
        b.id_bobot,
        b.id_kriteria,
        k.nama_kriteria,
        k.tipe_kriteria,
        b.role,
        b.nilai_bobot
    FROM dss_bobotkriteria b
    JOIN dss_kriteria k ON k.id_kriteria = b.id_kriteria
    WHERE b.role = ANY(f_roles);
END;
$$ LANGUAGE plpgsql;