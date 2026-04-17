select * from inventori_pengajuan
select * from dss_dssproses
select * from  dss_alternatifdss

alter table dss_detailhasilsaw
RENAME COLUMN hasil_id TO id_hasil

SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'dss_dssproses';

DROP FUNCTION hapus_detail_hasil_saw

--  Ambil Hasil SAW Not Test Yet
select * ambil_hasil_saw_pengadaan

select * ambil_hasil_saw_inventori
-- testing alternatif dss

SELECT tambah_alternatif_dss(
    'ALT001',
    'DSS-001',
    'PNJ_002',
     NULL,
    'pengadaan'
);

SELECT * FROM cari_alternatif_dss('ALT001');

SELECT hapus_alternatif_dss('ALT001');

-- testing alternatif dss
SELECT tambah_dss_proses(
    'USR001',
    'B2',
    'IT',
    'SAW'
);

Select * FROM ambil_semua_dss_proses();

-- Testing Pengajuan
SELECT tambah_pengajuan (
    'USR_0003',
    'Frontend Developer',
    'Butuh laptop',
    '2026-05-01',
    'Project X',
    'PT ABC',
    'urgent',           
    NOW() :: TIMESTAMP,              
    NULL,             
    'USR-001');

SELECT * FROM ambil_semua_pengajuan();

SELECT * FROM cari_pengajuan('PNJ_0002');

SELECT approve_pengajuan('PNJ_0002','approved','USR-001');

SELECT approve_pengajuan('PNJ_0002','rejected','USR-001');

SELECT hapus_pengajuan('PNJ_0002');

-- Testing Peminjaman
SELECT tambah_peminjaman
('USR001','LAP001',CURRENT_DATE,CURRENT_DATE + INTERVAL '7 days','dipinjam','Testing manual');

SELECT * FROM ambil_semua_peminjaman();

SELECT * FROM cari_peminjaman('PIM-001');

SELECT update_peminjaman
('PIM-001',CURRENT_DATE,CURRENT_DATE + INTERVAL '10 days','dipinjam','Update test');

SELECT hapus_peminjaman('PIM-001');

SELECT pinjam_laptop
('USR001','LAP001','PGJ001',CURRENT_DATE,CURRENT_DATE + INTERVAL '5 days','Pinjam via sistem');

-- Testing User
SELECT create_user('Alqan Nazra','alqan@test.com','123456','HC');

SELECT * FROM get_all_users();

SELECT * FROM get_user_by_id('USR_0003');

SELECT * FROM login_user('alqan@test.com','123456');

SELECT update_user('USR_0003','Alqan Update','alqan_update@test.com','IT');

SELECT update_password('USR_0003','password_baru');

SELECT deactivate_user('USR_0003');

-- testing laptop pengadaan 
SELECT tambah_laptop_pengadaan('ASUS ROG STRIX G15',25000000,'RTX 4060',15.6,90,1,1,1,2.3);

SELECT * FROM ambil_laptop_pengadaan();

SELECT update_laptop_pengadaan
('LP_0002','ASUS ROG STRIX G15 UPDATE',26000000,'RTX 4070',16.0,95);

SELECT update_spek_pengadaan('LP_0002',2,2,2);

SELECT hapus_laptop_pengadaan('LP_0004');

-- Note test yet
SELECT * FROM ambil_hasil_saw_pengadaan();
-- Note test yet
SELECT * FROM ambil_hasil_saw_pengadaan('HS-001');

-- testing hasil saw
select buat_hasil_saw('DSS_0004')



-- testing detailhasilsaw
select * from dss_hasilsaw

SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'dss_detailhasilsaw';

SELECT tambah_detail_hasil_saw('SAW_0002', 0.8, 0.9, 1);

SELECT * FROM cari_data_detail_hasil_saw('DHS_0002');

-- ambil semua
SELECT * FROM ambil_semua_data_detail_hasil_saw();

-- hapus
SELECT hapus_detail_hasil_saw('DHS_0001');


-- testing bobot kriteria
select tambah_bobot_kriteria('KRIT_0005','dummy','1');

select * from cari_bobot_kriteria('bobot_0003');

select * from ambil_semua_data_detail_bobot();

select update_bobot_kriteria('bobot_0003',0.3);

select hapus_bobot_kriteria('bobot_0004')

-- Testing Kriteria
select tambah_kriteria('Dummy_v1','Benefit');

select * from ambil_kriteria();

select update_kriteria('K2','Storage','BENEFIT')

-- Testing Laptop Inventori
select * from ambil_spek_laptop('inventori_0002')

select * from ambil_laptop_inventori();

-- Not Test yet
select * from ambil_hasil_saw_inventori('inventori_0002');

select * from update_kondisi_inventori('inventori_0002','Rusak');

select * from update_status_inventori('inventori_0002','Setengah Rusak','Jakarta');

select hapus_laptop_inventori('inventori_0004');

select update_spek_inventori('inventori_0002','2','2','2');

