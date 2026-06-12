from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from inventori.models import (
    User, Processor, RAM, Storage,
    LaptopInventori, Pengajuan, Peminjaman, RiwayatAktivitas
)
from dss.models import (
    Kriteria, BobotKriteria,
    DSSProses, NilaiAlternatif, LaptopAlternatif,
    HasilSAW, DetailHasilSAW,
    LaptopPengadaan
)

class Command(BaseCommand):
    help = 'Comprehensive Database Seeder for SiLaptop79'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Starting Database Seeding...")

        # 1. USERS
        users_data = [
            {"id_user": "USR-001", "nama": "Admin Human Capital", "email": "admin.hc@silaptop.com", "password": "password123", "role": "HC"},
            {"id_user": "USR-002", "nama": "IT Manager", "email": "manager.it@silaptop.com", "password": "password123", "role": "IT"},
            {"id_user": "USR-003", "nama": "Ahmad Dani", "email": "ahmad.dani@silaptop.com", "password": "password123", "role": "Employee"},
            {"id_user": "USR-004", "nama": "Siti Aminah", "email": "siti.aminah@silaptop.com", "password": "password123", "role": "Employee"},
        ]
        users = {}
        for u_data in users_data:
            user, created = User.objects.get_or_create(id_user=u_data["id_user"], defaults=u_data)
            users[u_data["id_user"]] = user
            if created: self.stdout.write(f"   Created User: {u_data['nama']}")

        # 2. MASTER HARDWARE
        # Processors
        processors_data = [
            {"id_processor": "PROC-001", "nama_processor": "Intel Core i7", "manufacturer": "Intel", "model": "i7-1165G7", "cores": 4, "threads": 8, "base_clock": 2.8, "max_clock": 4.7, "arsitektur": "x64"},
            {"id_processor": "PROC-002", "nama_processor": "AMD Ryzen 7", "manufacturer": "AMD", "model": "Ryzen 7 5800U", "cores": 8, "threads": 16, "base_clock": 1.9, "max_clock": 4.4, "arsitektur": "x64"},
            {"id_processor": "PROC-003", "nama_processor": "Apple M1", "manufacturer": "Apple", "model": "M1 8-Core", "cores": 8, "threads": 8, "base_clock": 3.2, "max_clock": 3.2, "arsitektur": "ARM"},
        ]
        processors = {}
        for p_data in processors_data:
            proc, created = Processor.objects.get_or_create(id_processor=p_data["id_processor"], defaults=p_data)
            processors[p_data["id_processor"]] = proc
            if created: self.stdout.write(f"   Created Processor: {p_data['model']}")

        # RAM
        rams_data = [
            {"id_ram": "RAM-001", "kapasitas_gb": 8, "tipe": "DDR4"},
            {"id_ram": "RAM-002", "kapasitas_gb": 16, "tipe": "DDR4"},
            {"id_ram": "RAM-003", "kapasitas_gb": 32, "tipe": "LPDDR4X"},
        ]
        rams = {}
        for r_data in rams_data:
            ram, created = RAM.objects.get_or_create(id_ram=r_data["id_ram"], defaults=r_data)
            rams[r_data["id_ram"]] = ram
            if created: self.stdout.write(f"   Created RAM: {r_data['kapasitas_gb']}GB")

        # Storage
        storages_data = [
            {"id_storage": "STR-001", "kapasitas_gb": 256, "tipe": "SSD NVMe"},
            {"id_storage": "STR-002", "kapasitas_gb": 512, "tipe": "SSD NVMe"},
            {"id_storage": "STR-003", "kapasitas_gb": 1024, "tipe": "SSD NVMe"},
        ]
        storages = {}
        for s_data in storages_data:
            st, created = Storage.objects.get_or_create(id_storage=s_data["id_storage"], defaults=s_data)
            storages[s_data["id_storage"]] = st
            if created: self.stdout.write(f"   Created Storage: {s_data['kapasitas_gb']}GB")

        # 3. LAPTOP INVENTORI
        laptops_data = [
            {
                "id_laptop_inventori": "LTP-INV-001", "no_inventori": "INV/2024/001", "nama_laptop": "ThinkPad T14", "model": "Gen 2",
                "os": "Windows 11", "kondisi": "baik", "status": "tersedia", "lokasi": "Office Jakarta",
                "id_processor": processors["PROC-001"], "id_ram": rams["RAM-002"], "id_storage": storages["STR-002"], "ukuran_layar": 14.0
            },
            {
                "id_laptop_inventori": "LTP-INV-002", "no_inventori": "INV/2024/002", "nama_laptop": "MacBook Air", "model": "M1 2020",
                "os": "macOS Sonoma", "kondisi": "baik", "status": "dipinjam", "lokasi": "Remote",
                "id_processor": processors["PROC-003"], "id_ram": rams["RAM-001"], "id_storage": storages["STR-001"], "ukuran_layar": 13.3
            },
            {
                "id_laptop_inventori": "LTP-INV-003", "no_inventori": "INV/2024/003", "nama_laptop": "Dell Latitude 5420", "model": "5420",
                "os": "Windows 10", "kondisi": "baik", "status": "tersedia", "lokasi": "Office Bandung",
                "id_processor": processors["PROC-002"], "id_ram": rams["RAM-002"], "id_storage": storages["STR-002"], "ukuran_layar": 14.0
            },
        ]
        laptops = {}
        for l_data in laptops_data:
            laptop, created = LaptopInventori.objects.get_or_create(id_laptop_inventori=l_data["id_laptop_inventori"], defaults=l_data)
            laptops[l_data["id_laptop_inventori"]] = laptop
            if created: self.stdout.write(f"   Created Laptop: {l_data['nama_laptop']}")

        # 4. PENGAJUAN
        pengajuan_data = [
            {
                "id_pengajuan": "PGJ-001", "id_user": users["USR-003"], "kebutuhan_role": "Backend Developer",
                "kebutuhan_requirement": "Needs high performance for Docker and compilation", "bulan": date.today(),
                "perusahaan": "PT Solusi Teknologi", "status": "approved", "approved_by": users["USR-002"]
            },
            {
                "id_pengajuan": "PGJ-002", "id_user": users["USR-004"], "kebutuhan_role": "UI/UX Designer",
                "kebutuhan_requirement": "Needs good screen color accuracy", "bulan": date.today(),
                "perusahaan": "PT Solusi Teknologi", "status": "pending"
            },
        ]
        pengajuans = {}
        for pg_data in pengajuan_data:
            pg, created = Pengajuan.objects.get_or_create(id_pengajuan=pg_data["id_pengajuan"], defaults=pg_data)
            pengajuans[pg_data["id_pengajuan"]] = pg
            if created: self.stdout.write(f"   Created Pengajuan: {pg_data['id_pengajuan']}")

        # 5. PEMINJAMAN
        if "PGJ-001" in pengajuans and "LTP-INV-002" in laptops:
            peminjaman, created = Peminjaman.objects.get_or_create(
                id_peminjaman="PMJ-001",
                defaults={
                    "id_pengajuan": pengajuans["PGJ-001"],
                    "id_user": users["USR-003"],
                    "id_laptop_inventori": laptops["LTP-INV-002"],
                    "tanggal_pinjam": date.today() - timedelta(days=5),
                    "status": "dipinjam"
                }
            )
            if created: self.stdout.write("   Created Peminjaman: PMJ-001")

        # 6. KRITERIA DSS
        kriteria_data = [
            {"id_kriteria": "K1", "nama_kriteria": "Harga", "tipe_kriteria": "cost", "golongan_kriteria": "Ekonomi"},
            {"id_kriteria": "K2", "nama_kriteria": "Kapasitas RAM", "tipe_kriteria": "benefit", "golongan_kriteria": "Performa"},
            {"id_kriteria": "K3", "nama_kriteria": "Kapasitas Storage", "tipe_kriteria": "benefit", "golongan_kriteria": "Penyimpanan"},
            {"id_kriteria": "K4", "nama_kriteria": "Berat", "tipe_kriteria": "cost", "golongan_kriteria": "Mobilitas"},
        ]
        kriterias = {}
        for k_data in kriteria_data:
            k, created = Kriteria.objects.get_or_create(id_kriteria=k_data["id_kriteria"], defaults=k_data)
            kriterias[k_data["id_kriteria"]] = k
            if created: self.stdout.write(f"   Created Kriteria: {k_data['nama_kriteria']}")

        # 7. BOBOT KRITERIA
        roles = ["Backend Developer", "UI/UX Designer"]
        bobots = {}
        for role in roles:
            for i, (kid, k) in enumerate(kriterias.items()):
                bid = f"B-{role[:2].upper()}-{kid}"
                # Sample weights: RAM/Storage higher for backend, Weight/Price for others
                weight = 0.25 # Default
                if role == "Backend Developer":
                    if kid == "K2": weight = 0.4
                    if kid == "K3": weight = 0.3
                    if kid == "K1": weight = 0.2
                    if kid == "K4": weight = 0.1
                
                b, created = BobotKriteria.objects.get_or_create(
                    id_bobot=bid,
                    defaults={"id_kriteria": k, "role": role, "nilai_bobot": weight}
                )
                bobots[bid] = b

        # 8. LAPTOP PENGADAAN
        pengadaan_data = [
            {
                "id_laptop_pengadaan": "LP-001", "nama_laptop": "ASUS Vivobook 14", "harga": 8500000,
                "id_processor": processors["PROC-001"], "id_ram": rams["RAM-001"], "id_storage": storages["STR-002"],
                "ukuran_layar": 14.0, "baterai": 42.0, "berat": 1.4
            },
            {
                "id_laptop_pengadaan": "LP-002", "nama_laptop": "HP Pavilion 15", "harga": 10500000,
                "id_processor": processors["PROC-002"], "id_ram": rams["RAM-002"], "id_storage": storages["STR-002"],
                "ukuran_layar": 15.6, "baterai": 50.0, "berat": 1.75
            },
        ]
        for lp_data in pengadaan_data:
            lp, created = LaptopPengadaan.objects.get_or_create(id_laptop_pengadaan=lp_data["id_laptop_pengadaan"], defaults=lp_data)
            if created: self.stdout.write(f"   Created Laptop Pengadaan: {lp_data['nama_laptop']}")

        self.stdout.write(self.style.SUCCESS("✨ Database Seeding Completed Successfully!"))
