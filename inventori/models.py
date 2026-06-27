from django.db import models
from django.utils import timezone

class User(models.Model):
    id_user = models.CharField(primary_key=True, max_length=15)
    nama = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=50)
    departemen = models.CharField(max_length=100, default='Non IT')

    def __str__(self):
        return self.nama

class Processor(models.Model):

    id_processor = models.CharField(primary_key=True, max_length=100)
    nama_processor = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    cores = models.IntegerField()
    threads = models.IntegerField()
    base_clock = models.FloatField()
    max_clock = models.FloatField()
    arsitektur = models.CharField(max_length=100)
    processor_score = models.IntegerField(default=0)

    keterangan = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = "inventori_processor"

class RAM(models.Model):
    id_ram = models.CharField(primary_key=True, max_length=100)

    kapasitas_gb = models.IntegerField()
    tipe = models.CharField(max_length=50)
    keterangan = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = "inventori_ram"

class Storage(models.Model):
    id_storage = models.CharField(primary_key=True, max_length=100)

    kapasitas_gb = models.IntegerField()
    tipe = models.CharField(max_length=100)

    class Meta:
        db_table = "inventori_storage"

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

    id_processor = models.ForeignKey(Processor, on_delete=models.SET_NULL, null=True, db_column='id_processor')
    id_ram = models.ForeignKey(RAM, on_delete=models.SET_NULL, null=True, db_column='id_ram')
    id_storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, null=True, db_column='id_storage')

    ukuran_layar = models.FloatField(null=True, blank=True)
    baterai = models.CharField(max_length=50, null=True, blank=True)  # Kapasitas baterai, e.g. "70 Wh"

    def save(self, *args, **kwargs):
        if self.kondisi:
            self.kondisi = str(self.kondisi).replace('_', ' ').strip().lower()
            if self.kondisi == 'rusak':
                self.kondisi = 'rusak ringan'
            if self.kondisi in ['rusak ringan', 'rusak berat']:
                self.status = 'rusak'
        if self.status:
            self.status = str(self.status).strip().lower()
        super().save(*args, **kwargs)

class Pengajuan(models.Model):
    id_pengajuan = models.CharField(primary_key=True, max_length=100)

    id_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user')
    kebutuhan_role = models.CharField(max_length=100)
    kebutuhan_requirement = models.TextField()
    bulan = models.DateField()
    keterangan = models.TextField(null=True, blank=True)
    perusahaan = models.TextField()

    status = models.CharField(max_length=20, default='menunggu')
    tanggal_pengajuan = models.DateTimeField(auto_now_add=True)
    tanggal_approval = models.DateTimeField(null=True, blank=True)
    id_proyek = models.ForeignKey(
        'Proyek',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_proyek'
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approver',
        db_column='approved_by'
    )

class Peminjaman(models.Model):
    id_peminjaman = models.CharField(primary_key=True, max_length=100)
    id_pengajuan = models.ForeignKey(Pengajuan,on_delete=models.CASCADE,db_column='id_pengajuan')
    id_user = models.ForeignKey(User,on_delete=models.CASCADE,db_column='id_user')
    id_laptop_inventori = models.ForeignKey(LaptopInventori,on_delete=models.CASCADE,db_column='id_laptop_inventori')
    tanggal_pinjam = models.DateField()
    tanggal_kembali = models.DateField(null=True, blank=True)
    tanggal_jatuh_tempo = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50)
    keterangan = models.TextField(null=True, blank=True)
    class Meta:
        db_table = "inventori_peminjaman"

class RiwayatAktivitas(models.Model):
    id_aktivitas = models.CharField(primary_key=True, max_length=100)

    id_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user')
    id_laptop_inventori = models.ForeignKey(LaptopInventori, on_delete=models.CASCADE, db_column='id_laptop')

    jenis_aktivitas = models.CharField(max_length=100)
    keterangan = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

class Role(models.Model):
    id_role = models.CharField(primary_key=True,max_length=20)
    nama_role = models.CharField(max_length=100,unique=True)
    min_ram = models.IntegerField(default=0)
    min_storage = models.IntegerField(default=0)
    nama_processor = models.CharField(max_length=20)
    min_processor_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = "inventori_role"
    def __str__(self):
        return self.nama_role

class Teknologi(models.Model):

    id_teknologi = models.CharField(
        primary_key=True,
        max_length=20
    )

    nama_teknologi = models.CharField(
        max_length=100,
        unique=True
    )

    kategori = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        db_table = "inventori_teknologi"

    def __str__(self):
        return self.nama_teknologi

class RoleTeknologi(models.Model):

    id_role_teknologi = models.CharField(
        primary_key=True,
        max_length=30
    )

    role = models.ForeignKey(
        Role,
        db_column="id_role",
        on_delete=models.CASCADE,
        related_name="teknologi_role"
    )

    teknologi = models.ForeignKey(
        Teknologi,
        db_column="id_teknologi",
        on_delete=models.CASCADE
    )

    is_default = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        db_table = "role_teknologi"

        unique_together = (
            "role",
            "teknologi"
        )

    def __str__(self):

        return (
            f"{self.role.nama_role}"
            f" - "
            f"{self.teknologi.nama_teknologi}"
        )

# =============================================
# 7. PROYEK
# =============================================
class Proyek(models.Model):
    id_proyek = models.CharField(primary_key=True, max_length=100)
    nama_proyek = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_proyek

class ProjectRole(models.Model):

    id_project_role = models.CharField(
        primary_key=True,
        max_length=50
    )

    proyek = models.ForeignKey(
        Proyek,
        db_column="id_proyek",
        on_delete=models.CASCADE,
        related_name="roles"
    )

    role = models.ForeignKey(
        Role,
        db_column="id_role",
        on_delete=models.CASCADE
    )

    persentase_role = models.FloatField()

    class Meta:
        db_table = "inventori_project_role"

class ProjectTechnology(models.Model):

    id_project_technology = models.CharField(
        primary_key=True,
        max_length=50
    )

    proyek = models.ForeignKey(
        Proyek,
        on_delete=models.CASCADE
    )

    teknologi = models.ForeignKey(
        Teknologi,
        on_delete=models.CASCADE
    )

    class Meta:

        db_table = "inventori_project_teknologi"

        unique_together = (
            "proyek",
            "teknologi"
        )
# class RoleProyek(models.Model):
#     id_role = models.CharField(primary_key=True, max_length=100)

#     proyek = models.ForeignKey(
#         Proyek,
#         on_delete=models.CASCADE,
#         related_name='roles'
#     )

#     nama_role = models.CharField(max_length=255)

#     class Meta:
#         db_table = "inventori_project_role"

class TeknologiRole(models.Model):
    id_teknologi = models.CharField(primary_key=True, max_length=100)
    role_proyek = models.ForeignKey(ProjectRole, on_delete=models.CASCADE, related_name='teknologi')
    nama_teknologi = models.CharField(max_length=255)

    def __str__(self):
        return self.nama_teknologi
