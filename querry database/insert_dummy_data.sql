-- ==========================================
-- DUMMY DATA UNTUK SISTEM SILAPTOP79
-- ==========================================

-- 1. INSERT USERS (inventori_user)
-- Note: id_user menggunakan string ID. Sesuaikan dengan model.
INSERT INTO inventori_user (id_user, nama, email, password, role) VALUES 
('U001', 'Admin HC', 'hc@silaptop79.com', 'pbkdf2_sha256$600000$dummy$hash', 'HC'),
('U002', 'Admin IT', 'it@silaptop79.com', 'pbkdf2_sha256$600000$dummy$hash', 'IT'),
('U003', 'Talent Satu', 'talent1@silaptop79.com', 'pbkdf2_sha256$600000$dummy$hash', 'TALENT'),
('U004', 'Talent Dua', 'talent2@silaptop79.com', 'pbkdf2_sha256$600000$dummy$hash', 'TALENT'),
('U005', 'Budi Santoso', 'budi@silaptop79.com', 'pbkdf2_sha256$600000$dummy$hash', 'TALENT')
ON CONFLICT (id_user) DO NOTHING;

-- 2. INSERT PROCESSOR (inventori_processor)
INSERT INTO inventori_processor (id, nama_processor, manufacturer, model, cores, threads, base_clock, max_clock, arsitektur, keterangan) VALUES 
(1, 'Intel Core i5-1135G7', 'Intel', 'i5-1135G7', 4, 8, 2.4, 4.2, 'Tiger Lake', 'Standar Office'),
(2, 'Intel Core i7-12700H', 'Intel', 'i7-12700H', 14, 20, 2.3, 4.7, 'Alder Lake', 'High Performance'),
(3, 'AMD Ryzen 5 5600U', 'AMD', '5600U', 6, 12, 2.3, 4.2, 'Zen 3', 'Efisiensi Daya'),
(4, 'Apple M2', 'Apple', 'M2', 8, 8, 3.49, 3.49, 'ARM', 'Apple Silicon')
ON CONFLICT (id) DO NOTHING;

-- 3. INSERT RAM (inventori_ram)
INSERT INTO inventori_ram (id, kapasitas_gb, tipe, keterangan) VALUES 
(1, 8, 'DDR4', 'Standar minimal 2023'),
(2, 16, 'DDR4', 'Rekomendasi Multitasking'),
(3, 16, 'LPDDR5', 'High Speed RAM'),
(4, 32, 'DDR5', 'Heavy Duty / Creator')
ON CONFLICT (id) DO NOTHING;

-- 4. INSERT STORAGE (inventori_storage)
INSERT INTO inventori_storage (id, kapasitas_gb, tipe) VALUES 
(1, 256, 'SSD SATA'),
(2, 512, 'SSD NVMe PCIe 3.0'),
(3, 1024, 'SSD NVMe PCIe 4.0')
ON CONFLICT (id) DO NOTHING;

-- 5. INSERT LAPTOP INVENTORI (inventori_laptopinventori)
-- Note: processor_id, ram_id, storage_id merupakan foreign key (pastikan ID 1-4 ada di tabel atas)
INSERT INTO inventori_laptopinventori (id_laptop_inventori, no_inventori, nama_laptop, model, os, kondisi, status, lokasi, ukuran_layar, processor_id, ram_id, storage_id) VALUES 
('LPT-001', 'INV/LPT/2023/001', 'Lenovo ThinkPad E14', 'Gen 2', 'Windows 11 Pro', 'baik', 'tersedia', 'Gudang IT - Rak A', 14.0, 1, 2, 2),
('LPT-002', 'INV/LPT/2023/002', 'ASUS ROG Zephyrus', 'G14', 'Windows 11 Home', 'baik', 'dipinjam', 'Di Talent (U003)', 14.0, 2, 3, 3),
('LPT-003', 'INV/LPT/2023/003', 'MacBook Air M2', '2022', 'macOS Sonoma', 'baik', 'tersedia', 'Gudang IT - Rak B', 13.6, 4, 2, 2),
('LPT-004', 'INV/LPT/2023/004', 'HP ProBook 440', 'G8', 'Windows 10 Pro', 'rusak_ringan', 'rusak', 'Ruang Servis', 14.0, 1, 1, 1),
('LPT-005', 'INV/LPT/2023/005', 'Dell XPS 15', '9520', 'Windows 11 Pro', 'baik', 'tersedia', 'Gudang IT - Rak A', 15.6, 2, 4, 3)
ON CONFLICT (id_laptop_inventori) DO NOTHING;

-- 6. INSERT KRITERIA DSS (dss_kriteria)
INSERT INTO dss_kriteria (id_kriteria, nama_kriteria, tipe_kriteria) VALUES 
('C1', 'Harga', 'cost'),
('C2', 'Processor', 'benefit'),
('C3', 'RAM', 'benefit'),
('C4', 'Storage', 'benefit'),
('C5', 'Berat', 'cost')
ON CONFLICT (id_kriteria) DO NOTHING;

-- 7. INSERT PENGAJUAN (inventori_pengajuan)
INSERT INTO inventori_pengajuan (id_pengajuan, perusahaan, keterangan, kebutuhan_role, kebutuhan_requirement, status, tanggal_pengajuan, id_user, bulan) VALUES 
('REQ-001', 'PT. Silaptop 79', 'Butuh laptop untuk desain grafis dan editing video ringan', 'UI/UX Designer', 'High Performance', 'Pending', CURRENT_DATE, 'U003', CURRENT_DATE),
('REQ-002', 'PT. Silaptop 79', 'Laptop untuk entry data harian', 'Data Entry', 'Standar', 'Approved', CURRENT_DATE, 'U004', CURRENT_DATE)
ON CONFLICT (id_pengajuan) DO NOTHING;

-- 8. INSERT BOBOT KRITERIA (dss_bobotkriteria)
INSERT INTO dss_bobotkriteria (id_bobot, role, nilai_bobot, kriteria_id) VALUES 
('B01', 'UI/UX Designer', 0.15, 'C1'),
('B02', 'UI/UX Designer', 0.25, 'C2'),
('B03', 'UI/UX Designer', 0.30, 'C3'),
('B04', 'UI/UX Designer', 0.20, 'C4'),
('B05', 'UI/UX Designer', 0.10, 'C5')
ON CONFLICT (id_bobot) DO NOTHING;
