from django.core.management.base import BaseCommand
from datetime import date

from inventori.models import (
    User, Processor, RAM, Storage,
    LaptopInventori, Pengajuan, Peminjaman, RiwayatAktivitas
)

from dss.models import (
    Kriteria, BobotKriteria,
    DSSProses, NilaiAlternatif,
    HasilSAW, DetailHasilSAW,
    LaptopPengadaan
)


class Command(BaseCommand):
    help = 'Seeder FULL semua tabel (Inventori + DSS)'

    def handle(self, *args, **kwargs):

        # =============================
        # 1. MASTER HARDWARE
        # =============================
        processor, _ = Processor.objects.get_or_create(
            model="i7-1165G7",
            defaults={
                "nama_processor": "Intel Core i7",
                "manufacturer": "Intel",
                "cores": 4,
                "threads": 8,
                "base_clock": 2.8,
                "max_clock": 4.7,
                "arsitektur": "x64"
            }
        )

        ram, _ = RAM.objects.get_or_create(
            kapasitas_gb=16,
            tipe="DDR4"
        )

        storage, _ = Storage.objects.get_or_create(
            kapasitas_gb=512,
            tipe="SSD"
        )

        # =============================
        # 2. USER
        # =============================
        user, _ = User.objects.get_or_create(
            id_user="USR-001",
            defaults={
                "nama": "Admin HC",
                "email": "admin@mail.com",
                "password": "123456",
                "role": "HC"
            }
        )

        approver, _ = User.objects.get_or_create(
            id_user="USR-002",
            defaults={
                "nama": "Manager IT",
                "email": "manager@mail.com",
                "password": "123456",
                "role": "IT"
            }
        )

        # =============================
        # 3. LAPTOP INVENTORI
        # =============================
        laptop, _ = LaptopInventori.objects.get_or_create(
            id_laptop_inventori="INV-001",
            defaults={
                "no_inventori": "LTP-001",
                "nama_laptop": "Lenovo ThinkPad T14",
                "model": "T14 Gen 2",
                "os": "Windows 11",
                "kondisi": "baik",
                "status": "tersedia",
                "lokasi": "Bandung",
                "processor": processor,
                "ram": ram,
                "storage": storage,
                "ukuran_layar": 14.0
            }
        )

        # =============================
        # 4. PENGAJUAN
        # =============================
        pengajuan, _ = Pengajuan.objects.get_or_create(
            id_pengajuan="PGJ-001",
            defaults={
                "user": user,
                "kebutuhan_role": "backend",
                "kebutuhan_requirement": "Butuh laptop untuk development",
                "bulan": date.today(),
                "perusahaan": "PT Padepokan 79",
                "status": "approved",
                "approved_by": approver
            }
        )

        # =============================
        # 5. PEMINJAMAN
        # =============================
        peminjaman, _ = Peminjaman.objects.get_or_create(
            id_peminjaman="PMJ-001",
            defaults={
                "pengajuan": pengajuan,
                "user": user,
                "laptop": laptop,
                "tanggal_pinjam": date.today(),
                "status": "dipinjam"
            }
        )

        # =============================
        # 6. RIWAYAT AKTIVITAS
        # =============================
        RiwayatAktivitas.objects.get_or_create(
            id_aktivitas="ACT-001",
            defaults={
                "user": user,
                "laptop": laptop,
                "jenis_aktivitas": "PINJAM",
                "keterangan": "Laptop dipinjam oleh user"
            }
        )

        # =============================
        # 7. KRITERIA DSS
        # =============================
        k1, _ = Kriteria.objects.get_or_create(
            id_kriteria="K1",
            defaults={
                "nama_kriteria": "Harga",
                "tipe_kriteria": "cost"
            }
        )

        k2, _ = Kriteria.objects.get_or_create(
            id_kriteria="K2",
            defaults={
                "nama_kriteria": "RAM",
                "tipe_kriteria": "benefit"
            }
        )

        # =============================
        # 8. BOBOT
        # =============================
        bobot1, _ = BobotKriteria.objects.get_or_create(
            id_bobot="B1",
            defaults={
                "kriteria": k1,
                "role": "backend",
                "nilai_bobot": 0.4
            }
        )

        bobot2, _ = BobotKriteria.objects.get_or_create(
            id_bobot="B2",
            defaults={
                "kriteria": k2,
                "role": "backend",
                "nilai_bobot": 0.6
            }
        )

        # =============================
        # 9. DSS PROSES
        # =============================
        dss, _ = DSSProses.objects.get_or_create(
            id_dss="DSS-001",
            defaults={
                "user": user,
                "bobot": bobot1,
                "role_dss": "backend",
                "jenis_dss": "pengadaan"
            }
        )

        # =============================
        # 10. LAPTOP PENGADAAN
        # =============================
        laptop_pengadaan, _ = LaptopPengadaan.objects.get_or_create(
            id_laptop_pengadaan="LP-001",
            defaults={
                "processor": processor,
                "ram": ram,
                "storage": storage,
                "nama_laptop": "ASUS ROG",
                "harga": 15000000,
                "gpu": "RTX 3050",
                "ukuran_layar": 15.6,
                "baterai": 5000,
                "berat": 1.8
            }
        )

        # =============================
        # 11. ALTERNATIF DSS
        # =============================
        alternatif, _ = NilaiAlternatif.objects.get_or_create(
            id_alternatif="ALT-001",
            defaults={
                "dss": dss,
                "laptop_inventori": laptop,
                "id_laptop_pengadaan": laptop_pengadaan.id_laptop_pengadaan,
                "sumber_data": "inventori"
            }
        )

        # =============================
        # 12. HASIL SAW
        # =============================
        hasil, _ = HasilSAW.objects.get_or_create(
            id_hasil="HS-001",
            defaults={
                "dss": dss
            }
        )

        # =============================
        # 13. DETAIL HASIL SAW
        # =============================
        DetailHasilSAW.objects.get_or_create(
            id_detail="DHS-001",
            defaults={
                "hasil": hasil,
                "nilai_normalisasi": 0.8,
                "nilai_preferensi": 0.9,
                "ranking": 1
            }
        )

        self.stdout.write(self.style.SUCCESS("🔥 Seeder FULL berhasil dijalankan!"))