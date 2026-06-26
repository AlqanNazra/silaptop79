INSERT INTO auth_user (
    username,
    password,
    first_name,
    last_name,
    email,
    is_staff,
    is_superuser,
    is_active,
    date_joined
)
VALUES
(
    'USR_0001',
    '123456',
    'Admin',
    'HC',
    'hc@laptop79.com',
    TRUE,
    FALSE,
    TRUE,
    CURRENT_TIMESTAMP
),
(
    'USR_0002',
    '123456',
    'Admin',
    'IT Infrastruktur',
    'it@laptop79.com',
    TRUE,
    FALSE,
    TRUE,
    CURRENT_TIMESTAMP
),
(
    'USR_0003',
    '123456',
    'Talent',
    '',
    'talent@laptop79.com',
    FALSE,
    FALSE,
    TRUE,
    CURRENT_TIMESTAMP
);

select * from auth_user

select * from inventori_pengajuan

select * from inventori_peminjaman

ALTER TABLE inventori_peminjaman
RENAME COLUMN pengajuan_id TO id_pengajuan;

ALTER TABLE inventori_peminjaman
RENAME COLUMN user_id TO id_user;

ALTER TABLE inventori_peminjaman
RENAME COLUMN id_laptop TO id_laptop_inventori;

ALTER TABLE inventori_peminjaman
ADD CONSTRAINT fk_peminjaman_laptop
FOREIGN KEY (id_laptop_inventori)
REFERENCES inventori_laptopinventori(id_laptop_inventori);

ALTER TABLE inventori_peminjaman
ADD CONSTRAINT fk_peminjaman_pengajuan
FOREIGN KEY (id_pengajuan)
REFERENCES inventori_pengajuan(id_pengajuan);

ALTER TABLE inventori_peminjaman
ADD CONSTRAINT fk_peminjaman_user
FOREIGN KEY (id_user)
REFERENCES inventori_user(id_user);

select * from inventori_riwayataktivitas

ALTER TABLE inventori_riwayataktivitas
RENAME COLUMN laptop_id TO id_laptop;

ALTER TABLE inventori_riwayataktivitas
RENAME COLUMN user_id TO id_user;

ALTER TABLE inventori_peminjaman
ADD COLUMN tanggal_jatuh_tempo DATE;

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'inventori_pengajuan'
ORDER BY ordinal_position;

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name='inventori_pengajuan';