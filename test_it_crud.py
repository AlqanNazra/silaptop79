import os
import django
from django.test import Client
from django.urls import reverse

def run_tests():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
    django.setup()

    from django.test.utils import setup_test_environment
    setup_test_environment()

    from inventori.models import User, LaptopInventori, Processor, RAM, Storage, Pengajuan
    from django.contrib.auth.models import User as DjangoUser

    # Ensure IT user exists in CustomUser database
    it_user, created = User.objects.get_or_create(
        id_user='U002',
        defaults={
            'nama': 'Admin IT',
            'email': 'it@silaptop79.com',
            'password': 'password_baru',
            'role': 'IT'
        }
    )
    if not created:
        it_user.password = 'password_baru'
        it_user.role = 'IT'
        it_user.save()

    print("IT User U002 verified/created.")

    client = Client()
    # Log in
    logged_in = client.login(username='U002', password='password_baru')
    if not logged_in:
        print("Failed to login with backend. Let's authenticate manually by forcing login.")
        # Force login if standard login fails due to password hashing differences
        django_user, _ = DjangoUser.objects.get_or_create(username='U002')
        django_user.id_user = 'U002'
        django_user.nama = 'Admin IT'
        django_user.role = 'IT'
        client.force_login(django_user, backend='core.auth_backend.InventoriAuthBackend')
    else:
        print("Logged in successfully using client.login!")

    # 1. Dashboard IT
    print("Testing IT Dashboard...")
    response = client.get(reverse('dashboard_it'))
    assert response.status_code == 200, f"Dashboard IT failed: {response.status_code}"
    assert 'total_laptop' in response.context, "total_laptop not in context"
    assert 'total_pengajuan' in response.context, "total_pengajuan not in context"
    print("IT Dashboard OK.")

    # 2. Manajemen Laptop IT
    print("Testing Manajemen Laptop IT...")
    response = client.get(reverse('manajemen_laptop_it'))
    assert response.status_code == 200, f"Manajemen Laptop IT failed: {response.status_code}"
    assert 'laptops' in response.context, "laptops not in context"
    print("Manajemen Laptop IT OK.")

    # Get hardware items for laptop creation
    proc = Processor.objects.first()
    if not proc:
        proc = Processor.objects.create(
            nama_processor="Intel Core i7", manufacturer="Intel", model="i7-13700H",
            cores=14, threads=20, base_clock=2.4, max_clock=5.0, arsitektur="Raptor Lake"
        )
    ram = RAM.objects.first()
    if not ram:
        ram = RAM.objects.create(kapasitas_gb=16, tipe="DDR5")
    storage = Storage.objects.first()
    if not storage:
        storage = Storage.objects.create(kapasitas_gb=512, tipe="SSD")

    # 3. Tambah Laptop IT
    print("Testing Tambah Laptop...")
    laptop_data = {
        'nama_laptop': 'Test Laptop AntiGravity',
        'model': 'Asus',
        'os': 'Windows 11 Pro',
        'kondisi': 'baik',
        'status': 'tersedia',
        'lokasi': 'HQ room 101',
        'id_processor': proc.id_processor,
        'id_ram': ram.id_ram,
        'id_storage': storage.id_storage,
        'ukuran_layar': '14.0'
    }
    response = client.post(reverse('tambahlaptop_it'), laptop_data)
    assert response.status_code == 302, f"Tambah Laptop POST failed: {response.status_code}"
    
    new_laptop = LaptopInventori.objects.filter(nama_laptop='Test Laptop AntiGravity').first()
    assert new_laptop is not None, "Laptop was not created in database"
    print(f"Tambah Laptop OK. Created laptop ID: {new_laptop.id_laptop_inventori}")

    # 4. Detail Laptop IT
    print("Testing Detail Laptop...")
    response = client.get(reverse('detaillaptop_it', kwargs={'id_laptop': new_laptop.id_laptop_inventori}))
    assert response.status_code == 200, f"Detail Laptop GET failed: {response.status_code}"
    assert response.context['laptop'].nama_laptop == 'Test Laptop AntiGravity', "Incorrect laptop details"
    print("Detail Laptop GET OK.")

    # 5. Edit Laptop IT
    print("Testing Edit Laptop POST...")
    edit_data = {
        'kondisi': 'rusak',
        'status': 'dipinjam',
        'lokasi': 'Branch B',
        'id_processor': proc.id_processor,
        'id_ram': ram.id_ram,
        'id_storage': storage.id_storage,
    }
    response = client.post(reverse('editdatalaptop_it', kwargs={'id_laptop': new_laptop.id_laptop_inventori}), edit_data)
    assert response.status_code == 302, f"Edit Laptop POST failed: {response.status_code}"
    
    new_laptop.refresh_from_db()
    assert new_laptop.kondisi == 'rusak', f"Kondisi not updated: {new_laptop.kondisi}"
    assert new_laptop.status == 'dipinjam', f"Status not updated: {new_laptop.status}"
    assert new_laptop.lokasi == 'Branch B', f"Lokasi not updated: {new_laptop.lokasi}"
    print("Edit Laptop POST OK.")

    # 6. Delete Laptop IT
    print("Testing Delete Laptop (via POST action=hapus in detail view)...")
    response = client.post(
        reverse('detaillaptop_it', kwargs={'id_laptop': new_laptop.id_laptop_inventori}),
        {'action': 'hapus'}
    )
    assert response.status_code == 302, f"Delete Laptop POST failed: {response.status_code}"
    assert not LaptopInventori.objects.filter(id_laptop_inventori=new_laptop.id_laptop_inventori).exists(), "Laptop still exists in DB"
    print("Delete Laptop OK.")

    # 7. Pengajuan Laptop IT list
    print("Testing Pengajuan Laptop List...")
    response = client.get(reverse('pengajuanlaptop_it'))
    assert response.status_code == 200, f"Pengajuan List failed: {response.status_code}"
    print("Pengajuan List OK.")

    # 8. Detail Pengajuan IT (GET and POST Approve/Reject)
    pengajuan = Pengajuan.objects.first()
    if not pengajuan:
        pengajuan = Pengajuan.objects.create(
            id_user=it_user,
            kebutuhan_role="Software Engineer",
            kebutuhan_requirement="Core i7, 16GB RAM",
            status="menunggu",
            keterangan="Urgent request for test"
        )
    print(f"Testing Detail Pengajuan ID: {pengajuan.id_pengajuan}...")
    response = client.get(f"{reverse('detailpengajuan_it')}?id={pengajuan.id_pengajuan}")
    assert response.status_code == 200, f"Detail Pengajuan GET failed: {response.status_code}"
    
    response = client.post(f"{reverse('detailpengajuan_it')}?id={pengajuan.id_pengajuan}", {'action': 'disetujui'})
    assert response.status_code == 302, f"Detail Pengajuan POST approve failed: {response.status_code}"
    
    pengajuan.refresh_from_db()
    assert pengajuan.status == 'disetujui', f"Pengajuan status not disetujui: {pengajuan.status}"
    print("Detail Pengajuan OK.")

    # 9. DSS Input Kriteria IT
    print("Testing DSS Input Kriteria IT...")
    response = client.get(reverse('inputkriteria_it'))
    assert response.status_code == 200, f"Input Kriteria GET failed: {response.status_code}"
    
    weights_data = {
        'bobot_processor': '8',
        'bobot_ram': '6',
        'bobot_storage': '5',
        'bobot_berat': '3',
        'bobot_layar': '2',
        'bobot_baterai': '7',
    }
    response = client.post(reverse('inputkriteria_it'), weights_data)
    assert response.status_code == 302, f"Input Kriteria POST failed: {response.status_code}"
    print("DSS Input Kriteria IT OK.")

    # 10. DSS Hasil Rekomendasi IT
    print("Testing DSS Hasil Rekomendasi IT...")
    response = client.get(reverse('hasilrekomendasi_it'))
    assert response.status_code == 200, f"Hasil Rekomendasi GET failed: {response.status_code}"
    assert 'ranking' in response.context, "ranking not in context"
    assert len(response.context['ranking']) > 0, "ranking is empty"
    print("DSS Hasil Rekomendasi IT OK.")

    # 11. DSS Detail Rekomendasi IT
    first_rank_id = response.context['ranking'][0]['id']
    print(f"Testing DSS Detail Rekomendasi ID: {first_rank_id}...")
    response = client.get(f"{reverse('detailrekomendasi_it')}?id={first_rank_id}")
    assert response.status_code == 200, f"Detail Rekomendasi GET failed: {response.status_code}"
    assert response.context['laptop']['id'] == first_rank_id
    print("DSS Detail Rekomendasi IT OK.")

    # 12. DSS Detail Scrapping IT
    print(f"Testing DSS Detail Scrapping ID: {first_rank_id}...")
    response = client.get(f"{reverse('detailrekomendasiscrapping_it')}?id={first_rank_id}")
    assert response.status_code == 200, f"Detail Scrapping GET failed: {response.status_code}"
    assert response.context['laptop']['id'] == first_rank_id
    print("DSS Detail Scrapping IT OK.")

    # 13. Riwayat Peminjaman Laptop IT
    print("Testing Riwayat Peminjaman Laptop IT...")
    response = client.get(reverse('riwayatpeminjamanlaptop_it'))
    assert response.status_code == 200, f"Riwayat Peminjaman failed: {response.status_code}"
    assert 'list_peminjaman' in response.context
    print("Riwayat Peminjaman Laptop IT OK.")

    print("\nALL IT CRUD AND VIEW TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()
