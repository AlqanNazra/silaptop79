import os
import sys
import django

sys.path.append("/Users/dafffc/Documents/SiLaptop79/silaptop79")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from django.test import Client
from inventori.models import User, Pengajuan, Peminjaman, LaptopInventori

def run_test():
    client = Client()
    
    # 0. Cleanup old test data
    print("Cleaning up old test data...")
    Peminjaman.objects.filter(id_peminjaman='TEST-PMJ-01').delete()
    LaptopInventori.objects.filter(id_laptop_inventori='TEST-LAP-01').delete()
    Pengajuan.objects.filter(id_user='U003').exclude(id_pengajuan='REQ-001').delete()
    print("Cleanup complete!")
    
    # 1. Login
    print("Testing Login...")
    login_success = client.login(username='U003', password='123456')
    assert login_success, "Login failed for U003!"
    print("Login success!")

    # 2. Submit Pengajuan
    print("\nTesting Pengajuan Laptop POST...")
    response = client.post('/talent/pengajuan-laptop/', {
        'departemen': 'it',
        'role': 'developer',
        'spesifikasi': 'MacBook Air M3, 16GB RAM',
        'alasan': 'Kebutuhan pengembangan sistem'
    })
    assert response.status_code == 302, f"Expected redirect, got status code {response.status_code}"
    print("POST request completed successfully!")

    # Verify database record
    user_requests = Pengajuan.objects.filter(id_user='U003').exclude(id_pengajuan='REQ-001')
    assert user_requests.count() > 0, "No new pengajuan record found in database!"
    new_req = user_requests.first()
    print(f"Successfully verified new pengajuan in database: ID={new_req.id_pengajuan}, Role={new_req.kebutuhan_role}, Status={new_req.status}")

    # 3. Verify Riwayat Peminjaman view GET
    print("\nTesting Riwayat Peminjaman GET...")
    response = client.get('/talent/riwayat-peminjaman/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Riwayat Peminjaman loaded successfully!")

    # 4. Verify Pengembalian Laptop
    print("\nTesting Pengembalian Laptop...")
    # First, let's make sure U003 has an active peminjaman in the database.
    # If not, let's create a dummy active laptop and peminjaman for U003 to test.
    active_pmj = Peminjaman.objects.filter(id_user='U003', status='dipinjam').first()
    if not active_pmj:
        print("No active peminjaman found for U003, creating a dummy one...")
        laptop = LaptopInventori.objects.filter(status='tersedia').first()
        if not laptop:
            laptop = LaptopInventori.objects.create(
                id_laptop_inventori='TEST-LAP-01',
                no_inventori='TEST-SN-999',
                nama_laptop='Test Laptop',
                model='Test Model',
                os='macOS',
                kondisi='baik',
                status='tersedia',
                lokasi='Kantor Pusat'
            )
        
        active_pmj = Peminjaman.objects.create(
            id_peminjaman='TEST-PMJ-01',
            id_pengajuan=new_req,
            id_user=User.objects.get(id_user='U003'),
            id_laptop_inventori=laptop,
            tanggal_pinjam='2026-06-01',
            status='dipinjam',
            keterangan='Peminjaman aktif untuk test'
        )
        laptop.status = 'dipinjam'
        laptop.save()

    print(f"Active laptop found: {active_pmj.id_laptop_inventori.nama_laptop} (SN: {active_pmj.id_laptop_inventori.no_inventori})")

    # Get Return Page
    response = client.get('/talent/pengembalian/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Pengembalian GET page loaded successfully!")

    # Post Return
    response = client.post('/talent/pengembalian/', {
        'alasan': 'Selesai Kontrak/Proyek',
        'catatan': 'Semua data telah dibersihkan.',
        'kondisi': 'good'
    })
    assert response.status_code == 302, f"Expected redirect after return post, got {response.status_code}"
    print("Pengembalian POST request completed successfully!")

    # Verify return database updates
    active_pmj.refresh_from_db()
    assert active_pmj.status == 'selesai', f"Expected peminjaman status to be 'selesai', got {active_pmj.status}"
    
    laptop = active_pmj.id_laptop_inventori
    laptop.refresh_from_db()
    assert laptop.status == 'tersedia', f"Expected laptop status to be 'tersedia', got {laptop.status}"
    print("Database values successfully verified! Return process works perfectly!")

if __name__ == '__main__':
    run_test()
