-- =====================================================
-- ALTER TABLE NOTIFIKASI
-- =====================================================
CREATE TABLE notifikasi (
    id_notifikasi VARCHAR(20) PRIMARY KEY,
    id_user VARCHAR(20) NOT NULL,

    judul_notifikasi VARCHAR(200) NOT NULL,
    pesan_notifikasi TEXT NOT NULL,

    jenis_notifikasi VARCHAR(30) NOT NULL,
    prioritas VARCHAR(20) NOT NULL,

    sumber_notifikasi VARCHAR(30) NOT NULL,

    status_baca BOOLEAN DEFAULT FALSE,

    tanggal_kirim TIMESTAMP DEFAULT NOW(),
    tanggal_baca TIMESTAMP,

    is_deleted BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT fk_notifikasi_user
    FOREIGN KEY (id_user)
    REFERENCES "User"(id_user)
    ON UPDATE CASCADE
    ON DELETE CASCADE,

    CONSTRAINT chk_jenis_notifikasi
    CHECK (
        jenis_notifikasi IN (
            'APPROVAL',
            'REJECT',
            'PEMINJAMAN',
            'PENGEMBALIAN',
            'DSS_RESULT',
            'WARNING',
            'SYSTEM'
        )
    ),

    CONSTRAINT chk_prioritas_notifikasi
    CHECK (
        prioritas IN (
            'LOW',
            'MEDIUM',
            'HIGH',
            'URGENT'
        )
    ),

    CONSTRAINT chk_sumber_notifikasi
    CHECK (
        sumber_notifikasi IN (
            'PENGAJUAN',
            'PEMINJAMAN',
            'DSS',
            'INVENTORI',
            'SYSTEM'
        )
    )
);


CREATE OR REPLACE FUNCTION kirim_notifikasi(
    p_id_notifikasi VARCHAR,
    p_id_user VARCHAR,
    p_judul VARCHAR,
    p_pesan TEXT,
    p_jenis VARCHAR,
    p_prioritas VARCHAR,
    p_sumber VARCHAR
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_user INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_user
    FROM "User"
    WHERE id_user = p_id_user;

    IF v_user = 0 THEN
        RAISE EXCEPTION 'User tidak ditemukan';
    END IF;

    INSERT INTO notifikasi(
        id_notifikasi,
        id_user,
        judul_notifikasi,
        pesan_notifikasi,
        jenis_notifikasi,
        status_baca,
        tanggal_kirim,
        prioritas,
        sumber_notifikasi
    )
    VALUES(
        p_id_notifikasi,
        p_id_user,
        p_judul,
        p_pesan,
        p_jenis,
        FALSE,
        NOW(),
        p_prioritas,
        p_sumber
    );

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION hapus_notifikasi(
    p_id_notifikasi VARCHAR
)
RETURNS BOOLEAN AS
$$
BEGIN

    UPDATE notifikasi
    SET is_deleted = TRUE
    WHERE id_notifikasi = p_id_notifikasi;

    RETURN TRUE;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_notifikasi_by_user(
    p_id_user VARCHAR
)
RETURNS TABLE(
    id_notifikasi VARCHAR,
    judul VARCHAR,
    pesan TEXT,
    jenis VARCHAR,
    status_baca BOOLEAN,
    tanggal_kirim TIMESTAMP
)
AS
$$
BEGIN

    RETURN QUERY

    SELECT
        n.id_notifikasi,
        n.judul_notifikasi,
        n.pesan_notifikasi,
        n.jenis_notifikasi,
        n.status_baca,
        n.tanggal_kirim
    FROM notifikasi n
    WHERE n.id_user = p_id_user
    AND n.is_deleted = FALSE
    ORDER BY n.tanggal_kirim DESC;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION validate_target_notifikasi(
    p_id_user VARCHAR
)
RETURNS BOOLEAN AS
$$
DECLARE
    v_exist INTEGER;
BEGIN

    SELECT COUNT(*)
    INTO v_exist
    FROM "User"
    WHERE id_user = p_id_user;

    RETURN v_exist > 0;

END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_latest_notification(
    p_id_user VARCHAR
)
RETURNS TABLE(
    id_notifikasi VARCHAR,
    judul VARCHAR,
    tanggal TIMESTAMP
)
AS
$$
BEGIN

    RETURN QUERY

    SELECT
        id_notifikasi,
        judul_notifikasi,
        tanggal_kirim
    FROM notifikasi
    WHERE id_user = p_id_user
    ORDER BY tanggal_kirim DESC
    LIMIT 1;

END;
$$ LANGUAGE plpgsql;
