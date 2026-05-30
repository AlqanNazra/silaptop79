from django.db import models
from inventori.models import User, LaptopInventori


# =============================================
# 1. KRITERIA
# =============================================
class Kriteria(models.Model):
    id_kriteria = models.CharField(primary_key=True, max_length=100)

    nama_kriteria = models.CharField(max_length=255)

    tipe_kriteria = models.CharField(
        max_length=20,
        choices=[
            ('benefit', 'Benefit'),
            ('cost', 'Cost')
        ]
    )


# =============================================
# 2. BOBOT KRITERIA (SWARA)
# =============================================
class BobotKriteria(models.Model):
    id_bobot = models.CharField(primary_key=True, max_length=100)

    id_kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE)

    role = models.CharField(max_length=100)
    nilai_bobot = models.FloatField()


# =============================================
# 3. DSS PROSES
# =============================================
class DSSProses(models.Model):
    id_dss = models.CharField(primary_key=True, max_length=100)

    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_bobot = models.ForeignKey(BobotKriteria, on_delete=models.CASCADE)

    role_dss = models.CharField(max_length=100)
    jenis_dss = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)


# =============================================
# 4. LAPTOP ALTERNATIF (NEW - sesuai SQL)
# =============================================
class LaptopAlternatif(models.Model):
    id_alternatif_laptop = models.CharField(primary_key=True, max_length=100)

    model_alternatif = models.TextField()
    brand_alternatif = models.TextField()

    id_dss = models.ForeignKey(DSSProses, on_delete=models.CASCADE)


# =============================================
# 5. NILAI ALTERNATIF (NEW - SAW CORE)
# =============================================
class NilaiAlternatif(models.Model):
    id_nilai_alternatif = models.CharField(primary_key=True, max_length=100)

    nilai_alternatif = models.FloatField()
    nilai_normalisasi = models.FloatField()

    id_alternatif_laptop = models.ForeignKey(
        LaptopAlternatif,
        on_delete=models.CASCADE
    )

    id_bobot = models.ForeignKey(
        BobotKriteria,
        on_delete=models.CASCADE
    )


# =============================================
# 6. HASIL SAW (UPDATED)
# =============================================
class HasilSAW(models.Model):
    id_hasil = models.CharField(primary_key=True, max_length=100)

    id_dss = models.ForeignKey(DSSProses, on_delete=models.CASCADE)

    tanggal_proses = models.DateTimeField(auto_now_add=True)

    id_nilai_alternatif = models.ForeignKey(
        NilaiAlternatif,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )


# =============================================
# 7. LAPTOP PENGADAAN (SCRAPING)
# =============================================
class LaptopPengadaan(models.Model):
    id_laptop_pengadaan = models.CharField(primary_key=True, max_length=100)

    id_processor = models.ForeignKey(
        'inventori.Processor',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    id_ram = models.ForeignKey(
        'inventori.RAM',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    id_storage = models.ForeignKey(
        'inventori.Storage',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    nama_laptop = models.CharField(max_length=255)
    harga = models.IntegerField()
    gpu = models.CharField(max_length=255, null=True, blank=True)

    ukuran_layar = models.FloatField()
    baterai = models.FloatField()
    berat = models.FloatField()

    def __str__(self):
        return self.nama_laptop


# =============================================
# 8. ALTERNATIF DSS (ADDED FOR SEEDER/COMPATIBILITY)
# =============================================
class AlternatifDSS(models.Model):
    id_alternatif = models.CharField(primary_key=True, max_length=100)
    dss = models.ForeignKey(DSSProses, on_delete=models.CASCADE)
    id_laptop_pengadaan = models.CharField(max_length=100, null=True, blank=True)
    laptop_inventori = models.ForeignKey(LaptopInventori, on_delete=models.CASCADE, null=True, blank=True)
    sumber_data = models.CharField(max_length=100)

    class Meta:
        db_table = 'dss_alternatifdss'


# =============================================
# 9. DETAIL HASIL SAW (ADDED FOR SEEDER/COMPATIBILITY)
# =============================================
class DetailHasilSAW(models.Model):
    id_detail = models.CharField(primary_key=True, max_length=100)
    hasil = models.ForeignKey(HasilSAW, on_delete=models.CASCADE)
    nilai_normalisasi = models.FloatField()
    nilai_preferensi = models.FloatField()
    ranking = models.IntegerField()

    class Meta:
        db_table = 'dss_detailhasilsaw'