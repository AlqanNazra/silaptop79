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

INSERT INTO inventori_role (
    id_role,
    nama_role,
    min_ram,
    min_storage,
    nama_processor,
    min_processor_score
)
VALUES
('ROL_0001','Frontend Developer',8,256,'Intel Core i5',12000),
('ROL_0002','Backend Developer',16,512,'Intel Core i7',18000),
('ROL_0003','Fullstack Developer',16,512,'Intel Core i7',19000),
('ROL_0004','Mobile Developer',16,512,'Intel Core i7',17000),
('ROL_0005','QA Engineer',8,256,'Intel Core i5',12000),
('ROL_0006','DevOps Engineer',32,1024,'Intel Core i9',25000),
('ROL_0007','Data Engineer',32,1024,'Intel Core i9',26000),
('ROL_0008','Data Analyst',16,512,'Intel Core i7',18000),
('ROL_0009','AI Engineer',32,1024,'Intel Core i9',28000),
('ROL_0010','ML Engineer',32,1024,'Intel Core i9',28000),
('ROL_0011','UI UX Designer',16,512,'Intel Core i7',16000),
('ROL_0012','System Analyst',16,512,'Intel Core i7',17000),
('ROL_0013','Business Analyst',16,512,'Intel Core i7',16000),
('ROL_0014','Cloud Engineer',32,1024,'Intel Core i9',27000),
('ROL_0015','Security Engineer',32,1024,'Intel Core i9',26000),
('ROL_0016','Database Engineer',32,1024,'Intel Core i9',25000),
('ROL_0017','Project Manager',16,512,'Intel Core i7',16000),
('ROL_0018','Scrum Master',16,512,'Intel Core i7',15000),
('ROL_0019','Technical Writer',8,256,'Intel Core i5',11000),
('ROL_0020','Support Engineer',8,256,'Intel Core i5',10000);

INSERT INTO inventori_teknologi (
    id_teknologi,
    nama_teknologi,
    kategori
)
VALUES
('TEK_0001','ReactJS','Frontend'),
('TEK_0002','VueJS','Frontend'),
('TEK_0003','Angular','Frontend'),
('TEK_0004','Django','Backend'),
('TEK_0005','Spring Boot','Backend'),
('TEK_0006','Laravel','Backend'),
('TEK_0007','Flutter','Mobile'),
('TEK_0008','Kotlin','Mobile'),
('TEK_0009','Swift','Mobile'),
('TEK_0010','PostgreSQL','Database'),
('TEK_0011','MySQL','Database'),
('TEK_0012','MongoDB','Database'),
('TEK_0013','Docker','DevOps'),
('TEK_0014','Kubernetes','DevOps'),
('TEK_0015','AWS','Cloud'),
('TEK_0016','Azure','Cloud'),
('TEK_0017','TensorFlow','AI'),
('TEK_0018','PyTorch','AI'),
('TEK_0019','Selenium','Testing'),
('TEK_0020','JMeter','Testing');

INSERT INTO role_teknologi (
    id_role_teknologi,
    id_role,
    id_teknologi
)
VALUES
('RT_0001','ROL_0001','TEK_0001'),
('RT_0002','ROL_0001','TEK_0002'),

('RT_0003','ROL_0002','TEK_0004'),
('RT_0004','ROL_0002','TEK_0010'),

('RT_0005','ROL_0003','TEK_0001'),
('RT_0006','ROL_0003','TEK_0004'),

('RT_0007','ROL_0004','TEK_0007'),
('RT_0008','ROL_0004','TEK_0008'),

('RT_0009','ROL_0005','TEK_0019'),
('RT_0010','ROL_0005','TEK_0020'),

('RT_0011','ROL_0006','TEK_0013'),
('RT_0012','ROL_0006','TEK_0014'),

('RT_0013','ROL_0007','TEK_0010'),
('RT_0014','ROL_0007','TEK_0015'),

('RT_0015','ROL_0008','TEK_0010'),
('RT_0016','ROL_0008','TEK_0011'),

('RT_0017','ROL_0009','TEK_0017'),
('RT_0018','ROL_0009','TEK_0018'),

('RT_0019','ROL_0010','TEK_0017'),
('RT_0020','ROL_0010','TEK_0018');

INSERT INTO inventori_proyek (
    id_proyek,
    nama_proyek,
    user_perusahaan,
    mulai_proyek,
    akhir_proyek,
    jenis_proyek
)
SELECT
    'PRJ_' || LPAD(i::TEXT,4,'0'),
    'Project ' || i,
    'Client ' || i,
    'Departement',
    CURRENT_DATE,
    CURRENT_DATE + 180
FROM generate_series(1,20) i;

INSERT INTO inventori_project_role (
    id_project_role,
    id_proyek,
    id_role,
    persentase_role
)
SELECT
    'PR_' || LPAD(gs::TEXT,4,'0'),
    'PRJ_' || LPAD(gs::TEXT,4,'0'),
    'ROL_' || LPAD(gs::TEXT,4,'0'),
    1
FROM generate_series(1,20) gs;