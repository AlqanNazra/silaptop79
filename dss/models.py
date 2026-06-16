from django.db import models
from inventori.models import User, LaptopInventori

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
    
    golongan_kriteria = models.CharField(max_length=255)

class BobotKriteria(models.Model):
    id_bobot = models.CharField(primary_key=True, max_length=100)
    id_kriteria = models.ForeignKey(
        Kriteria,
        db_column="kriteria_id",
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=100
    )

    nilai_bobot = models.FloatField()

class DSSProses(models.Model):
    id_dss = models.CharField(primary_key=True, max_length=100)

    id_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    id_bobot = models.ForeignKey(BobotKriteria, on_delete=models.CASCADE, db_column='bobot_id')

    role_dss = models.CharField(max_length=100)
    jenis_dss = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id_dss} - {self.role_dss} ({self.jenis_dss})"

class LaptopAlternatif(models.Model):
    id_alternatif_laptop = models.CharField(primary_key=True, max_length=100)

    model_alternatif = models.TextField()

    brand_alternatif = models.TextField()

    id_dss = models.ForeignKey(DSSProses, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand_alternatif} {self.model_alternatif}"

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

    class Meta:
        db_table = "dss_nilaialternatif"

    def __str__(self):
        return self.id_nilai_alternatif

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

    def __str__(self):
        return f"Hasil SAW {self.id_hasil} ({self.tanggal_proses})"
    
class LaptopPengadaan(models.Model):
    id_laptop_pengadaan = models.CharField(primary_key=True, max_length=100)

    id_processor = models.ForeignKey(
        'inventori.Processor',
        db_column='processor_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    id_ram = models.ForeignKey(
        'inventori.RAM',
        db_column='ram_id',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    id_storage = models.ForeignKey(
        'inventori.Storage',
        db_column='storage_id',
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

    class Meta:
        db_table = "dss_laptoppengadaan"

    def __str__(self):
        return self.nama_laptop

class DetailHasilSAW(models.Model):
    id_detail = models.CharField(primary_key=True, max_length=100)

    id_hasil = models.ForeignKey(
        HasilSAW, 
        on_delete=models.CASCADE,
        related_name='detail_set',
        db_column='id_hasil'
    )
    
    nilai_normalisasi = models.FloatField()

    nilai_preferensi = models.FloatField()

    ranking = models.IntegerField()

    class Meta:
        db_table = 'dss_detailhasilsaw' 

    def __str__(self):
        return f"Detail {self.id_detail} - Rank {self.ranking}"