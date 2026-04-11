from django.db import models

# =============================================
# 1. USERS
# =============================================
class User(models.Model):
    id_user = models.CharField(primary_key=True, max_length=15)
    nama = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.nama


# =============================================
# 2. MASTER HARDWARE
# =============================================
class Processor(models.Model):
    nama_processor = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    cores = models.IntegerField()
    threads = models.IntegerField()
    base_clock = models.FloatField()
    max_clock = models.FloatField()
    arsitektur = models.CharField(max_length=100)
    keterangan = models.TextField(null=True, blank=True)


class RAM(models.Model):
    kapasitas_gb = models.IntegerField()
    tipe = models.CharField(max_length=50)
    keterangan = models.TextField(null=True, blank=True)


class Storage(models.Model):
    kapasitas_gb = models.IntegerField()
    tipe = models.CharField(max_length=100)


# =============================================
# 3. LAPTOP INVENTORI
# =============================================
class LaptopInventori(models.Model):
    id_laptop_inventori = models.CharField(primary_key=True, max_length=100)
    no_inventori = models.CharField(max_length=100, unique=True)
    nama_laptop = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    os = models.CharField(max_length=100)

    kondisi = models.CharField(
        max_length=50,
        choices=[
            ('baik', 'Baik'),
            ('rusak ringan', 'Rusak Ringan'),
            ('rusak berat', 'Rusak Berat'),
        ]
    )

    status = models.CharField(
        max_length=50,
        choices=[
            ('tersedia', 'Tersedia'),
            ('dipinjam', 'Dipinjam'),
            ('rusak', 'Rusak'),
        ]
    )

    lokasi = models.CharField(max_length=255)

    processor = models.ForeignKey(Processor, on_delete=models.SET_NULL, null=True)
    ram = models.ForeignKey(RAM, on_delete=models.SET_NULL, null=True)
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True)

    ukuran_layar = models.FloatField(null=True, blank=True)


# =============================================
# 4. PENGAJUAN
# =============================================
class Pengajuan(models.Model):
    id_pengajuan = models.CharField(primary_key=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kebutuhan_role = models.CharField(max_length=100)
    kebutuhan_requirement = models.TextField()
    bulan = models.DateField()
    keterangan = models.TextField(null=True, blank=True)
    perusahaan = models.TextField()

    status = models.CharField(max_length=20, default='pending')
    tanggal_pengajuan = models.DateTimeField(auto_now_add=True)
    tanggal_approval = models.DateTimeField(null=True, blank=True)

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approver'
    )


# =============================================
# 5. PEMINJAMAN
# =============================================
class Peminjaman(models.Model):
    id_peminjaman = models.CharField(primary_key=True, max_length=100)
    pengajuan = models.ForeignKey(Pengajuan, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    laptop = models.ForeignKey(LaptopInventori, on_delete=models.CASCADE)

    tanggal_pinjam = models.DateField()
    tanggal_kembali = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=50)
    keterangan = models.TextField(null=True, blank=True)


# =============================================
# 6. RIWAYAT AKTIVITAS
# =============================================
class RiwayatAktivitas(models.Model):
    id_aktivitas = models.CharField(primary_key=True, max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    laptop = models.ForeignKey(LaptopInventori, on_delete=models.CASCADE)

    jenis_aktivitas = models.CharField(max_length=100)
    keterangan = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)