import os
import sys
import django

sys.path.append("/Users/dafffc/Documents/SiLaptop79/silaptop79")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from django.test import Client
from inventori.models import User, LaptopInventori, Processor, RAM, Storage, Pengajuan, Peminjaman

def run_test():
    client = Client()
    
    # 1. Login as U001 (Admin HC)
    print("Testing Login...")
    login_success = client.login(username='U001', password='123456')
    assert login_success, "Login failed for U001!"
    print("Login success!")

    # 2. View Dashboard HC
    print("\nTesting Dashboard HC GET...")
    response = client.get('/hc/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Dashboard HC loaded successfully!")

    # 3. View Manajemen Laptop Page
    print("\nTesting Manajemen Laptop GET...")
    response = client.get('/hc/manajemen-laptop/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Manajemen Laptop page loaded successfully!")

    # 4. View Tambah Laptop Page
    print("\nTesting Tambah Laptop GET...")
    response = client.get('/hc/tambah-laptop/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Tambah Laptop GET page loaded successfully!")

    # 5. POST Tambah Laptop
    print("\nTesting Tambah Laptop POST...")
    # Get random specifications from DB if available
    proc = Processor.objects.first()
    ram = RAM.objects.first()
    st = Storage.objects.first()
    
    laptop_data = {
        'nama_laptop': 'Test Audit Laptop HC',
        'model': 'Audit-2026',
        'os': 'Windows 11',
        'kondisi': 'baik',
        'status': 'tersedia',
        'lokasi': 'Kantor Bandung',
        'id_processor': proc.id_processor if proc else '',
        'id_ram': ram.id_ram if ram else '',
        'id_storage': st.id_storage if st else '',
        'ukuran_layar': '14'
    }
    
    # Let's delete any duplicate test laptop first
    LaptopInventori.objects.filter(nama_laptop='Test Audit Laptop HC').delete()

    response = client.post('/hc/tambah-laptop/', laptop_data)
    # Redirect to manajemen-laptop page expected
    if response.status_code == 200:
        from django.contrib.messages import get_messages
        msg_list = list(get_messages(response.wsgi_request))
        print("DEBUG Tambah Laptop Messages:")
        for m in msg_list:
            print(f"- [{m.tags}] {m.message}")
    assert response.status_code == 302, f"Expected 302 redirect, got {response.status_code}"
    print(f"Tambah Laptop POST status code: {response.status_code}")
    
    # Verify in DB
    new_laptop = LaptopInventori.objects.filter(nama_laptop='Test Audit Laptop HC').first()
    assert new_laptop is not None, "Test laptop was not created in database!"
    print(f"Verified new laptop created in DB: ID={new_laptop.id_laptop_inventori}, SN={new_laptop.no_inventori}")

    # 6. View Detail Laptop Page
    print("\nTesting Detail Laptop GET...")
    detail_url = f'/hc/detail-laptop/{new_laptop.id_laptop_inventori}/'
    response = client.get(detail_url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Detail Laptop GET page loaded successfully!")

    # 7. POST Detail Laptop - Update Status/Kondisi
    print("\nTesting Detail Laptop UPDATE POST...")
    response = client.post(detail_url, {
        'action': 'update',
        'kondisi': 'rusak',
        'status': 'tersedia',
        'lokasi': 'Head Office',
        'id_processor': proc.id_processor,
        'id_ram': ram.id_ram,
        'id_storage': st.id_storage,
    })
    assert response.status_code == 302
    new_laptop.refresh_from_db()
    assert new_laptop.kondisi == 'rusak', f"Expected kondisi 'rusak', got {new_laptop.kondisi}"
    assert new_laptop.status == 'perbaikan', f"Expected status 'perbaikan', got {new_laptop.status}"
    print("Laptop status and kondisi successfully updated in database!")

    # 8. View Edit Laptop Page
    print("\nTesting Edit Laptop GET...")
    edit_url = f'/hc/edit-laptop/{new_laptop.id_laptop_inventori}/'
    response = client.get(edit_url)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Edit Laptop GET page loaded successfully!")

    # 9. POST Edit Laptop - Update specs
    print("\nTesting Edit Laptop POST...")
    # Get alternative specs
    proc_alt = Processor.objects.last()
    ram_alt = RAM.objects.last()
    st_alt = Storage.objects.last()
    
    response = client.post(edit_url, {
        'kondisi': 'baik',
        'status': 'tersedia',
        'lokasi': 'Kantor Bandung',
        'id_processor': proc_alt.id_processor if proc_alt else '',
        'id_ram': ram_alt.id_ram if ram_alt else '',
        'id_storage': st_alt.id_storage if st_alt else ''
    })
    assert response.status_code in [200, 302], f"Expected 200 or 302, got {response.status_code}"
    
    # Verify specifications updated
    new_laptop.refresh_from_db()
    if proc_alt:
        assert new_laptop.id_processor_id == proc_alt.id_processor, "Processor not updated!"
    print("Laptop specifications successfully updated in database!")

    # 10. POST Detail Laptop - Delete Laptop
    print("\nTesting Delete Laptop POST...")
    response = client.post(detail_url, {
        'action': 'hapus'
    })
    assert response.status_code in [200, 302], f"Expected 200 or 302, got {response.status_code}"
    
    # Verify deleted
    deleted_laptop = LaptopInventori.objects.filter(nama_laptop='Test Audit Laptop HC').first()
    assert deleted_laptop is None, "Laptop was not deleted from database!"
    print("Laptop successfully deleted from database!")

    # 11. View Pengajuan Laptop Page
    print("\nTesting Pengajuan Laptop GET...")
    response = client.get('/hc/pengajuan-laptop/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Pengajuan Laptop GET page loaded successfully!")

    # 12. Create test pengajuan and test Detail Pengajuan
    print("\nTesting Detail Pengajuan GET and POST...")
    # Clean up any duplicate test pengajuan
    Pengajuan.objects.filter(id_pengajuan='TEST-REQ-HC').delete()
    
    # Create mock pengajuan for test
    test_req = Pengajuan.objects.create(
        id_pengajuan='TEST-REQ-HC',
        id_user=User.objects.get(id_user='USR-003'),
        kebutuhan_role='developer',
        kebutuhan_requirement='Intel i7, 16GB RAM',
        status='menunggu',
        bulan='2026-06-01',
        keterangan='Untuk developer baru',
        perusahaan='Tujuh Sembilan'
    )
    
    detail_pengajuan_url = f'/hc/detail-pengajuan/?id={test_req.id_pengajuan}'
    response = client.get(detail_pengajuan_url)
    if response.status_code != 200:
        from django.contrib.messages import get_messages
        msg_list = list(get_messages(response.wsgi_request))
        print("REDIRECT MESSAGES:", [m.message for m in msg_list])
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Detail Pengajuan GET page loaded successfully!")

    # Approve Pengajuan POST
    response = client.post(detail_pengajuan_url, {
        'action': 'disetujui'
    })
    
    from django.contrib.messages import get_messages
    msg_list = list(get_messages(response.wsgi_request))
    print("DEBUG Detail Pengajuan POST:")
    print(f"- Status Code: {response.status_code}")
    for m in msg_list:
        print(f"- [{m.tags}] {m.message}")
        
    assert response.status_code in [200, 302], f"Expected 200 or 302, got {response.status_code}"
    
    # Verify in DB
    test_req.refresh_from_db()
    assert test_req.status == 'disetujui', f"Expected status 'disetujui', got {test_req.status}"
    print("Pengajuan successfully disetujui!")

    # Clean up test pengajuan
    test_req.delete()
    print("Cleaned up test pengajuan.")

    # 13. View Riwayat Peminjaman
    print("\nTesting Riwayat Peminjaman GET...")
    response = client.get('/hc/riwayat-peminjaman/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Riwayat Peminjaman page loaded successfully!")

    # 14. View Input Kriteria DSS Page
    print("\nTesting Input Kriteria GET...")
    response = client.get('/hc/input-kriteria/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Input Kriteria GET page loaded successfully!")

    # 15. POST Input Kriteria
    print("\nTesting Input Kriteria POST...")
    response = client.post('/hc/input-kriteria/', {
        'bobot_processor': '8',
        'bobot_ram': '6',
        'bobot_storage': '5',
        'bobot_berat': '3',
        'bobot_layar': '4',
        'bobot_baterai': '7'
    })
    assert response.status_code in [200, 302], f"Expected 200 or 302, got {response.status_code}"
    print("Input Kriteria POST request completed successfully!")

    # 16. View Hasil Rekomendasi Page
    print("\nTesting Hasil Rekomendasi GET...")
    response = client.get('/hc/hasil-rekomendasi/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Hasil Rekomendasi GET page loaded successfully!")

    # 17. View Detail Rekomendasi Page
    print("\nTesting Detail Rekomendasi GET...")
    response = client.get('/hc/detail-rekomendasi/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Detail Rekomendasi GET page loaded successfully!")

    # 18. View Detail Scrapping Page
    print("\nTesting Detail Scrapping GET...")
    response = client.get('/hc/detail-scrapping/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Detail Scrapping GET page loaded successfully!")

    print("\nALL HC AUDIT TESTS COMPLETED SUCCESSFULLY!")

if __name__ == '__main__':
    run_test()
