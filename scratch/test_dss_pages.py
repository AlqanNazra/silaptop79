import os
import django

import sys
import os
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()

# Coba ambil user pertama
user = User.objects.first()
if user:
    client.force_login(user)

print("--- Testing /hc/input-kriteria/ ---")
try:
    response = client.get('/hc/input-kriteria/')
    print(f"Status Code: {response.status_code}")
    if response.status_code >= 500:
        print(response.content[:1000].decode('utf-8'))
except Exception as e:
    import traceback
    traceback.print_exc()

print("\n--- Testing /hc/hasil-rekomendasi/ ---")
try:
    # Set session values to simulate rank page access
    session = client.session
    session['selected_role_teknologi'] = 'some_role'
    session['ranking_sesuai'] = []
    session['ranking_alternatif'] = []
    session['jenis_rekomendasi'] = 'inventori'
    session.save()
    
    response = client.get('/hc/hasil-rekomendasi/')
    print(f"Status Code: {response.status_code}")
    if response.status_code >= 500:
        print(response.content[:2000].decode('utf-8'))
except Exception as e:
    import traceback
    traceback.print_exc()

print("\n--- Testing POST /hc/input-kriteria/ (DSS SAW) ---")
try:
    from inventori.models import Proyek, RoleTeknologi
    proyek = Proyek.objects.first()
    role_tek = RoleTeknologi.objects.first()
    
    if proyek and role_tek:
        post_data = {
            "jenis_rekomendasi": "inventori",
            "id_proyek": proyek.id_proyek,
            "id_role_teknologi": role_tek.id_role_teknologi,
            "min_processor_score": "50",
            "min_ram": "8",
            "min_storage": "256",
            "min_harga": "5000000",
            "bobot_processor": "0.3",
            "bobot_ram": "0.2",
            "bobot_storage": "0.2",
            "bobot_berat": "0.1",
            "bobot_layar": "0.1",
            "bobot_baterai": "0.1",
            "action": "hitung"
        }
        response = client.post('/hc/input-kriteria/', post_data)
        print(f"POST Status Code: {response.status_code}")
        if response.status_code == 302:
            print(f"Redirected to: {response.url}")
            # Follow redirect to hasil-rekomendasi
            follow_resp = client.get(response.url)
            print(f"Redirect Target Status Code: {follow_resp.status_code}")
            if follow_resp.status_code >= 500:
                print(follow_resp.content[:2000].decode('utf-8'))
        elif response.status_code >= 500:
            print(response.content[:2000].decode('utf-8'))
    else:
        print("Skipping POST test: Proyek or RoleTeknologi empty in DB.")
except Exception as e:
    import traceback
    traceback.print_exc()

print("\n--- Testing GET /inventori/setujui-pengajuan/?id=PNJ_0001 ---")
try:
    response = client.get('/inventori/setujui-pengajuan/?id=PNJ_0001')
    print(f"Status Code: {response.status_code}")
    if response.status_code >= 500:
        print(response.content[:2000].decode('utf-8'))
except Exception as e:
    import traceback
    traceback.print_exc()

print("\n--- Testing POST /inventori/setujui-pengajuan/ (Confirm/Approve Laptop) ---")
try:
    from inventori.models import LaptopInventori, Pengajuan
    laptop = LaptopInventori.objects.filter(status__in=['tersedia', 'Available', 'Tersedia']).first()
    # Let's ensure there is a pending pengajuan
    pengajuan, _ = Pengajuan.objects.get_or_create(
        id_pengajuan="PNJ_TEST_0001",
        defaults={
            "id_user_id": "U003", # using seed U003
            "kebutuhan_role": "Backend Developer",
            "kebutuhan_requirement": "Test",
            "bulan": "2026-06-16",
            "perusahaan": "PT Solusi",
            "status": "pending"
        }
    )
    # Reset status to pending just in case it was approved in previous test runs
    pengajuan.status = "pending"
    pengajuan.save()
    
    if laptop and pengajuan:
        print(f"Approving Pengajuan {pengajuan.id_pengajuan} with Laptop {laptop.id_laptop_inventori}")
        post_data = {
            "laptop_id": laptop.id_laptop_inventori
        }
        response = client.post(f'/inventori/setujui-pengajuan/?id={pengajuan.id_pengajuan}', post_data)
        print(f"POST Status Code: {response.status_code}")
        
        # Print django messages
        from django.contrib.messages import get_messages
        messages_list = list(get_messages(response.wsgi_request))
        print("Messages:")
        for msg in messages_list:
            print(f"- {msg.level_tag}: {msg.message}")
            
        if response.status_code == 302:
            print(f"Redirected to: {response.url}")
        elif response.status_code >= 500:
            print(response.content[:2000].decode('utf-8'))
    else:
        print("Skipping POST test: No available laptop or pengajuan.")
except Exception as e:
    import traceback
    traceback.print_exc()


print("\n--- Testing /it/input-kriteria/ ---")
try:
    response = client.get('/it/input-kriteria/')
    print(f"Status Code: {response.status_code}")
    if response.status_code >= 500:
        print(response.content[:1000].decode('utf-8'))
except Exception as e:
    import traceback
    traceback.print_exc()

print("\n--- Testing /it/hasil-rekomendasi/ ---")
try:
    response = client.get('/it/hasil-rekomendasi/')
    print(f"Status Code: {response.status_code}")
    if response.status_code >= 500:
        print(response.content[:2000].decode('utf-8'))
except Exception as e:
    import traceback
    traceback.print_exc()

