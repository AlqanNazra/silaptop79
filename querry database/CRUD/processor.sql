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