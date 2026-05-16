from django.db import models
from django.utils import timezone

from inventori.models import (
    User,
    Teknologi,
    RoleTeknologi,
    Processor,
    RAM,
    Storage
)

# =====================================================
# 1. KRITERIA
# =====================================================

class Kriteria(models.Model):

    BENEFIT = "benefit"
    COST = "cost"

    TIPE_CHOICES = [
        (BENEFIT, "Benefit"),
        (COST, "Cost")
    ]

    id_kriteria = models.CharField(
        primary_key=True,
        max_length=100
    )

    nama_kriteria = models.CharField(
        max_length=255
    )

    tipe_kriteria = models.CharField(
        max_length=20,
        choices=TIPE_CHOICES
    )

    golongan_kriteria = models.CharField(
        max_length=255
    )

    teknologi = models.ForeignKey(
        Teknologi,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        db_table = "dss_kriteria"

    def __str__(self):
        return self.nama_kriteria


# =====================================================
# 2. BOBOT KRITERIA
# =====================================================

class BobotKriteria(models.Model):

    id_bobot = models.CharField(
        primary_key=True,
        max_length=100
    )

    role_teknologi = models.ForeignKey(
        RoleTeknologi,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    kriteria = models.ForeignKey(
        Kriteria,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    nilai_bobot = models.FloatField()

    nilai_swara = models.FloatField(
        null=True,
        blank=True
    )

    versi = models.IntegerField(default=1)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:

        db_table = "dss_bobotkriteria"

        indexes = [
            models.Index(
                fields=[
                    "role_teknologi",
                    "is_active"
                ]
            )
        ]

    def __str__(self):
        return self.id_bobot


# =====================================================
# 3. DSS PROSES
# =====================================================

class DSSProses(models.Model):

    id_dss = models.CharField(
        primary_key=True,
        max_length=100
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    bobot = models.ForeignKey(
        BobotKriteria,
        on_delete=models.CASCADE
    )

    role_dss = models.CharField(
        max_length=100
    )

    jenis_dss = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "dss_dssproses"

    def __str__(self):
        return self.id_dss


# =====================================================
# 4. LAPTOP ALTERNATIF
# =====================================================

class LaptopAlternatif(models.Model):

    id_alternatif_laptop = models.CharField(
        primary_key=True,
        max_length=100
    )

    model_alternatif = models.TextField()

    brand_alternatif = models.TextField()

    dss = models.ForeignKey(
        DSSProses,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "dss_laptopalternatif"

    def __str__(self):
        return self.model_alternatif


# =====================================================
# 5. NILAI ALTERNATIF
# =====================================================

class NilaiAlternatif(models.Model):

    id_nilai_alternatif = models.CharField(
        primary_key=True,
        max_length=100
    )

    nilai_alternatif = models.FloatField()

    nilai_normalisasi = models.FloatField(
        null=True,
        blank=True
    )

    alternatif = models.ForeignKey(
        LaptopAlternatif,
        on_delete=models.CASCADE
    )

    bobot = models.ForeignKey(
        BobotKriteria,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "dss_nilaialternatif"

    def __str__(self):
        return self.id_nilai_alternatif


# =====================================================
# 6. HASIL SAW
# =====================================================

class HasilSAW(models.Model):

    id_hasil = models.CharField(
        primary_key=True,
        max_length=100
    )

    dss = models.ForeignKey(
        DSSProses,
        on_delete=models.CASCADE
    )

    nilai_alternatif = models.ForeignKey(
        NilaiAlternatif,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    tanggal_proses = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "dss_hasilsaw"

    def __str__(self):
        return self.id_hasil


# =====================================================
# 7. LAPTOP PENGADAAN
# =====================================================

class LaptopPengadaan(models.Model):

    id_laptop_pengadaan = models.CharField(
        primary_key=True,
        max_length=100
    )

    processor = models.ForeignKey(
        Processor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    ram = models.ForeignKey(
        RAM,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    storage = models.ForeignKey(
        Storage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    nama_laptop = models.CharField(
        max_length=255
    )

    harga = models.IntegerField()

    gpu = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    ukuran_layar = models.FloatField()

    baterai = models.FloatField()

    berat = models.FloatField()

    class Meta:
        db_table = "dss_laptoppengadaan"

    def __str__(self):
        return self.nama_laptop


# =====================================================
# 8. DETAIL HASIL SAW
# =====================================================

class DetailHasilSAW(models.Model):

    id_detail = models.CharField(
        primary_key=True,
        max_length=100
    )

    hasil = models.ForeignKey(
        HasilSAW,
        on_delete=models.CASCADE,
        related_name='detail_set'
    )

    nilai_normalisasi = models.FloatField()

    nilai_preferensi = models.FloatField()

    ranking = models.IntegerField()

    class Meta:
        db_table = "dss_detailhasilsaw"

    def __str__(self):
        return f"{self.id_detail} - Rank {self.ranking}"