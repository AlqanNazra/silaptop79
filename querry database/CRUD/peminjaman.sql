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

CREATE OR REPLACE FUNCTION tambah_peminjaman(
    f_id_user VARCHAR,f_id_laptop_inventori VARCHAR,f_tanggal_pinjam DATE,
    f_tanggal_kembali DATE,f_status VARCHAR,f_keterangan TEXT)
RETURNS VOID AS $$
BEGIN 
    INSERT INTO inventori_peminjaman(
        id_peminjaman,id_user,id_laptop_inventori,
        tanggal_pinjam,tanggal_kembali,status,keterangan
    )
    VALUES (
        f_generate_id('PIM','inventori_peminjaman','id_piminjaman'),f_id_user,f_id_laptop_inventori,f_tanggal_pinjam,
        f_tanggal_kembali,f_status,f_keterangan);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_semua_peminjaman()
RETURNS TABLE (
    id_peminjaman VARCHAR,
    id_user VARCHAR,
    id_laptop_inventori VARCHAR,
    tanggal_pinjam DATE,
    tanggal_kembali DATE,
    status VARCHAR,
    keterangan TEXT
) AS $$
BEGIN 
    RETURN QUERY
    SELECT 
        p.id_peminjaman::VARCHAR,
        p.user_id::VARCHAR,
        p.laptop_id::VARCHAR,
        p.tanggal_pinjam,
        p.tanggal_kembali,
        p.status::VARCHAR,
        p.keterangan::TEXT
    FROM inventori_peminjaman p;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION cari_peminjaman(f_id_peminjaman VARCHAR(100))
RETURNS TABLE (
    id_peminjaman VARCHAR,
    id_user VARCHAR,
    id_laptop_inventori VARCHAR,
    tanggal_pinjam DATE,
    tanggal_kembali DATE,
    status VARCHAR,
    keterangan TEXT
) AS $$
BEGIN 
    RETURN QUERY
    SELECT 
        p.id_peminjaman::VARCHAR,
        p.user_id::VARCHAR,
        p.laptop_id::VARCHAR,
        p.tanggal_pinjam,
        p.tanggal_kembali,
        p.status::VARCHAR,
        p.keterangan::TEXT
    FROM inventori_peminjaman p
    WHERE p.id_peminjaman = f_id_peminjaman;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_peminjaman(f_id_peminjaman VARCHAR(100), f_tanggal_pinjam DATE, f_tanggal_kembali DATE, f_status VARCHAR(50), f_keterangan TEXT)
RETURNS TEXT AS $$
BEGIN
    UPDATE inventori_peminjaman
    SET tanggal_pinjam = f_tanggal_pinjam, tanggal_kembali = f_tanggal_kembali, status = f_status, keterangan = f_keterangan 
    WHERE id_peminjaman = f_id_peminjaman;
    RETURN 'Pemimjaman berhasil diupdate!';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE function hapus_peminjaman(f_id_peminjaman VARCHAR(100))
RETURNS TEXT As $$
BEGIN
    DELETE FROM inventori_peminjaman WHERE id_peminjaman = f_id_peminjaman;
    RETURN 'DATA pemimjaman dengan id' || f_id_peminjaman || ' berhasil dihapus,';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION pinjam_laptop(
    f_id_user VARCHAR,
    f_id_laptop VARCHAR,
    f_id_pengajuan VARCHAR,
    f_tanggal_pinjam DATE,
    f_tanggal_kembali DATE,
    f_keterangan TEXT
)
RETURNS TEXT AS $$
DECLARE
    v_status VARCHAR;
    v_status_pengajuan VARCHAR;
BEGIN
    -- cek status laptop
    SELECT status INTO v_status
    FROM inventori_laptopinventori
    WHERE id_laptop_inventori = f_id_laptop;

    IF NOT FOUND THEN
        RETURN 'Laptop tidak ditemukan';
    END IF;

    IF v_status != 'tersedia' THEN
        RETURN 'Laptop tidak tersedia';
    END IF;

    IF EXISTS (
        SELECT 1 FROM inventori_peminjaman
        WHERE laptop_id = f_id_laptop
        AND status = 'dipinjam'
    ) THEN
        RETURN 'Laptop sedang dipinjam';
    END IF;

    -- cek pengajuan
    SELECT status INTO v_status_pengajuan
    FROM inventori_pengajuan
    WHERE id_pengajuan = f_id_pengajuan;

    IF v_status_pengajuan != 'approved' THEN
        RETURN 'Pengajuan belum disetujui';
    END IF;

    -- insert peminjaman
    INSERT INTO inventori_peminjaman(
        id_peminjaman,
        pengajuan_id,
        user_id,
        laptop_id,
        tanggal_pinjam,
        tanggal_kembali,
        status,
        keterangan
    )
    VALUES (
        f_generate_id('PIM','inventori_peminjaman','id_peminjaman'),
        f_id_pengajuan,
        f_id_user,
        f_id_laptop,
        f_tanggal_pinjam,
        f_tanggal_kembali,
        'dipinjam',
        f_keterangan
    );

    -- update laptop
    UPDATE inventori_laptopinventori
    SET status = 'dipinjam'
    WHERE id_laptop_inventori = f_id_laptop;

    RETURN 'Peminjaman berhasil';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION pengembalian_laptop(
    f_id_peminjaman VARCHAR,
    f_lokasi VARCHAR,
    f_keterangan TEXT
)
RETURNS TEXT AS $$
DECLARE
    v_id_laptop VARCHAR;
BEGIN 
    SELECT laptop_id INTO v_id_laptop 
    FROM inventori_peminjaman 
    WHERE id_peminjaman = f_id_peminjaman;

    IF NOT FOUND THEN
        RETURN 'Data peminjaman tidak ditemukan';
    END IF;

    UPDATE inventori_peminjaman
    SET status = 'selesai',
        tanggal_kembali = CURRENT_DATE,
        keterangan = f_keterangan
    WHERE id_peminjaman = f_id_peminjaman;

    UPDATE inventori_laptopinventori
    SET status = 'tersedia',
        lokasi = f_lokasi
    WHERE id_laptop_inventori = v_id_laptop;

    RETURN 'Laptop berhasil dikembalikan';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION rusak_laptop(f_id_laptop VARCHAR,status VARCHAR,f_kondisi VARCHAR)
RETURNS TEXT AS $$
BEGIN
    Update inventori_laptopinventori
    SET status = 'rusak' , kondisi = f_kondisi
    WHERE id_laptop_inventori = f_id_laptop;
    RETURN 'Status laptop' || id_laptop_inventori || 'Sudah diupdate';
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sync_status_laptop()
RETURNS VOID AS $$
BEGIN
    UPDATE inventori_laptopinventori l
    SET status = CASE
        WHEN EXISTS (
            SELECT 1 FROM peminjaman p
            WHERE p.id_laptop_inventori = l.id_laptop_inventori
            AND p.status = 'rusak'
        ) THEN 'dipinjam'
        ELSE 'tersedia'
    END;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION ambil_laptop_by_lokasi()
RETURNS TABLE (
    no_inventori VARCHAR,
    nama_laptop VARCHAR,
    kondisi VARCHAR,
    status VARCHAR,
    lokasi VARCHAR,
    tanggal_pinjam DATE,
    tanggal_kembali DATE
)
AS $$
BEGIN 
    RETURN QUERY
    SELECT 
        li.no_inventori,
        li.nama_laptop,
        li.kondisi,
        li.status,
        li.lokasi,
        p.tanggal_pinjam,
        p.tanggal_kembali
    FROM inventori_laptopinventori li
    LEFT JOIN peminjaman p
        ON p.id_laptop_inventori = li.id_laptop_inventori;
END;
$$ LANGUAGE plpgsql;
