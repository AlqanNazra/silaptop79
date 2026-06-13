from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
import datetime

# ==========================================
# 1. HUMAN CAPITAL (HC) VIEWS
# ==========================================

def dashboard_hc_view(request):
    return render(request, 'hc/dashboard/dashboard_hc.html')

def manajemenlaptop_hc_view(request):
    return render(request, 'hc/inventori/manajemenlaptop_hc.html')

def pengajuanlaptop_hc_view(request):
    from inventori.services.service_pengajuan import PengajuanService
    from inventori.repositories.dto.dto_pengajuan import PengajuanDTO
    
    list_pengajuan = []
    try:
        service = PengajuanService()
        list_pengajuan = service.ambil_semua_pengajuan()
    except Exception:
        pass
        
    if not list_pengajuan:
        mock_pengajuan = PengajuanDTO(
            id_pengajuan=1,
            id_user=1,
            kebutuhan_role="Engineering",
            kebutuhan_requirement="MacBook Pro M3 Max",
            bulan="Oktober",
            keterangan="Kebutuhan software development berat.",
            perusahaan="Tujuh Sembilan",
            status="Pending",
            tanggal_pengajuan=datetime.date(2023, 10, 24)
        )
        list_pengajuan = [mock_pengajuan]
        
    context = {
        'list_pengajuan': list_pengajuan,
        'total_pengajuan': len(list_pengajuan),
        'total_pending': sum(1 for p in list_pengajuan if p.status.lower() == 'pending'),
        'total_disetujui': sum(1 for p in list_pengajuan if p.status.lower() == 'approved'),
        'total_ditolak': sum(1 for p in list_pengajuan if p.status.lower() == 'rejected'),
    }
    return render(request, 'hc/inventori/pengajuanlaptop_hc.html', context)

def detailpengajuan_hc_view(request):
    from inventori.services.service_pengajuan import PengajuanService
    from inventori.repositories.dto.dto_pengajuan import PengajuanDTO
    
    if request.method == 'POST':
        return redirect('pengajuanlaptop_hc')
        
    pengajuan_id = request.GET.get('id')
    pengajuan = None
    if pengajuan_id:
        try:
            service = PengajuanService()
            pengajuan = service.cari_pengajuan_by_id(int(pengajuan_id))
        except Exception:
            pass
            
    if not pengajuan:
        pengajuan = PengajuanDTO(
            id_pengajuan=1,
            id_user=1,
            kebutuhan_role="Engineering",
            kebutuhan_requirement="MacBook Pro M3 Max",
            bulan="Oktober",
            keterangan="Kebutuhan software development berat. Proyek terbaru memerlukan kompilasi kernel dan menjalankan multiple virtual containers secara simultan. Perangkat saat ini mengalami bottleneck pada RAM dan CPU thermal throttling.",
            perusahaan="Tujuh Sembilan",
            status="Pending",
            tanggal_pengajuan=datetime.date(2023, 10, 24)
        )
        
    return render(request, 'hc/inventori/detailpengajuan_hc.html', {'pengajuan': pengajuan})

def setujui_pengajuan_hc_view(request):
    from inventori.models import LaptopInventori
    
    pengajuan_id = request.GET.get('id', '1')
    
    if request.method == 'POST':
        return redirect('pengajuanlaptop_hc')
        
    available_laptops = []
    try:
        available_laptops = LaptopInventori.objects.filter(status__iexact='Available')
    except Exception:
        pass
        
    # Standard fallback laptops for select dropdown
    fallback_laptops = [
        {
            'id': '1',
            'nama_laptop': 'MacBook Pro 14 M3 Max',
            'processor': 'Apple M3 Max',
            'ram': '36GB Unified',
            'storage': '1TB SSD NVMe',
            'screen_size': '14-inch Liquid Retina XDR',
            'battery_capacity': '3000',
            'weight': '1,6'
        },
        {
            'id': '2',
            'nama_laptop': 'ThinkPad X1 Carbon Gen 10',
            'processor': 'Intel Core i7-1260P',
            'ram': '16GB LPDDR5',
            'storage': '512GB SSD NVMe',
            'screen_size': '14-inch IPS WUXGA',
            'battery_capacity': '2800',
            'weight': '1,12'
        },
        {
            'id': '3',
            'nama_laptop': 'Dell XPS 15 9520',
            'processor': 'Intel Core i9-12900H',
            'ram': '32GB DDR5',
            'storage': '1TB SSD NVMe',
            'screen_size': '15.6-inch OLED 3.5K',
            'battery_capacity': '3200',
            'weight': '1,96'
        }
    ]
    
    laptops_data = []
    if available_laptops:
        for idx, lap in enumerate(available_laptops):
            laptops_data.append({
                'id': str(lap.id_laptop),
                'nama_laptop': lap.nama_laptop,
                'processor': lap.id_processor.nama_processor if lap.id_processor else 'Intel Core i7',
                'ram': lap.id_ram.kapasitas_ram if lap.id_ram else '16GB',
                'storage': lap.id_storage.kapasitas_storage if lap.id_storage else '512GB SSD',
                'screen_size': '14-inch Liquid Retina XDR' if 'MacBook' in lap.nama_laptop else '14-inch FHD',
                'battery_capacity': '3000' if 'MacBook' in lap.nama_laptop else '2800',
                'weight': '1,6' if 'MacBook' in lap.nama_laptop else '1,3'
            })
    else:
        laptops_data = fallback_laptops
        
    return render(request, 'hc/inventori/setujuipengajuan_hc.html', {
        'pengajuan_id': pengajuan_id,
        'laptops': laptops_data
    })

def tambahlaptop_hc_view(request):
    return render(request, 'hc/inventori/tambahlaptop_hc.html')

def detaillaptop_hc_view(request):
    return render(request, 'hc/inventori/detaillaptop_hc.html')

def riwayatpeminjamanlaptop_hc_view(request):
    return render(request, 'hc/inventori/riwayatpeminjamanlaptop_hc.html')

def editdatalaptop_hc_view(request):
    return render(request, 'hc/inventori/editdatalaptop_hc.html')

def editriwayatpeminjamanlaptop_hc_view(request):
    return render(request, 'hc/inventori/editriwayatpeminjamanlaptop_hc.html')

def inputkriteria_hc_view(request):
    from inventori.models import Proyek
    import json
    proyek_qs = Proyek.objects.prefetch_related('roles__teknologi').all()
    proyek_data = []
    for p in proyek_qs:
        roles_data = []
        for r in p.roles.all():
            techs = [t.nama_teknologi for t in r.teknologi.all()]
            roles_data.append({
                'id_role': r.id_role,
                'nama_role': r.nama_role,
                'teknologi': techs
            })
        proyek_data.append({
            'id_proyek': p.id_proyek,
            'nama_proyek': p.nama_proyek,
            'roles': roles_data
        })
    proyek_json = json.dumps(proyek_data)
    return render(request, 'hc/dss/inputkriteria_hc.html', {'proyek_json': proyek_json})

def hasilrekomendasi_hc_view(request):
    return render(request, 'hc/dss/hasilrekomendasi_hc.html')

def detailrekomendasi_hc_view(request):
    return render(request, 'hc/dss/detailrekomendasi_hc.html')

def detailrekomendasiscrapping_hc_view(request):
    return render(request, 'hc/dss/detailrekomendasiscrapping_hc.html')

def notifikasi_hc_view(request):
    return render(request, 'hc/inventori/notifikasi_hc.html')


# ==========================================
# 2. INFORMATION TECHNOLOGY (IT) VIEWS (START FROM SCRATCH)
# ==========================================

def dashboard_it_view(request):
    return render(request, 'it/dashboard/dashboard_it.html')

def manajemenlaptop_it_view(request):
    return render(request, 'it/inventori/manajemenlaptop_it.html')

def pengajuanlaptop_it_view(request):
    from inventori.services.service_pengajuan import PengajuanService
    from inventori.repositories.dto.dto_pengajuan import PengajuanDTO
    
    list_pengajuan = []
    try:
        service = PengajuanService()
        list_pengajuan = service.ambil_semua_pengajuan()
    except Exception:
        pass
        
    if not list_pengajuan:
        mock_pengajuan = PengajuanDTO(
            id_pengajuan=1,
            id_user=1,
            kebutuhan_role="Engineering",
            kebutuhan_requirement="MacBook Pro M3 Max",
            bulan="Oktober",
            keterangan="Kebutuhan software development berat.",
            perusahaan="Tujuh Sembilan",
            status="Pending",
            tanggal_pengajuan=datetime.date(2023, 10, 24)
        )
        mock_pengajuan.status_it = "waiting" # Menunggu Antrean
        list_pengajuan = [mock_pengajuan]
        
    context = {
        'list_pengajuan': list_pengajuan,
    }
    return render(request, 'it/inventori/pengajuanlaptop_it.html', context)

def detailpengajuan_it_view(request):
    from inventori.services.service_pengajuan import PengajuanService
    from inventori.repositories.dto.dto_pengajuan import PengajuanDTO
    
    if request.method == 'POST':
        return redirect('pengajuanlaptop_it')
        
    pengajuan_id = request.GET.get('id')
    pengajuan = None
    if pengajuan_id:
        try:
            service = PengajuanService()
            pengajuan = service.cari_pengajuan_by_id(int(pengajuan_id))
        except Exception:
            pass
            
    if not pengajuan:
        pengajuan = PengajuanDTO(
            id_pengajuan=1,
            id_user=1,
            kebutuhan_role="Engineering",
            kebutuhan_requirement="MacBook Pro M3 Max",
            bulan="Oktober",
            keterangan="Kebutuhan software development berat. Proyek terbaru memerlukan kompilasi kernel dan menjalankan multiple virtual containers secara simultan. Perangkat saat ini mengalami bottleneck pada RAM dan CPU thermal throttling.",
            perusahaan="Tujuh Sembilan",
            status="Pending",
            tanggal_pengajuan=datetime.date(2023, 10, 24)
        )
        
    return render(request, 'it/inventori/detailpengajuan_it.html', {'pengajuan': pengajuan})

def setujui_pengajuan_it_view(request):
    from inventori.models import LaptopInventori
    
    pengajuan_id = request.GET.get('id', '1')
    
    if request.method == 'POST':
        return redirect('pengajuanlaptop_it')
        
    available_laptops = []
    try:
        available_laptops = LaptopInventori.objects.filter(status__iexact='Available')
    except Exception:
        pass
        
    # Standard fallback laptops for select dropdown
    fallback_laptops = [
        {
            'id': '1',
            'nama_laptop': 'MacBook Pro 14 M3 Max',
            'processor': 'Apple M3 Max',
            'ram': '36GB Unified',
            'storage': '1TB SSD NVMe',
            'screen_size': '14-inch Liquid Retina XDR',
            'battery_capacity': '3000',
            'weight': '1,6'
        },
        {
            'id': '2',
            'nama_laptop': 'ThinkPad X1 Carbon Gen 10',
            'processor': 'Intel Core i7-1260P',
            'ram': '16GB LPDDR5',
            'storage': '512GB SSD NVMe',
            'screen_size': '14-inch IPS WUXGA',
            'battery_capacity': '2800',
            'weight': '1,12'
        },
        {
            'id': '3',
            'nama_laptop': 'Dell XPS 15 9520',
            'processor': 'Intel Core i9-12900H',
            'ram': '32GB DDR5',
            'storage': '1TB SSD NVMe',
            'screen_size': '15.6-inch OLED 3.5K',
            'battery_capacity': '3200',
            'weight': '1,96'
        }
    ]
    
    laptops_data = []
    if available_laptops:
        for idx, lap in enumerate(available_laptops):
            laptops_data.append({
                'id': str(lap.id_laptop),
                'nama_laptop': lap.nama_laptop,
                'processor': lap.id_processor.nama_processor if lap.id_processor else 'Intel Core i7',
                'ram': lap.id_ram.kapasitas_ram if lap.id_ram else '16GB',
                'storage': lap.id_storage.kapasitas_storage if lap.id_storage else '512GB SSD',
                'screen_size': '14-inch Liquid Retina XDR' if 'MacBook' in lap.nama_laptop else '14-inch FHD',
                'battery_capacity': '3000' if 'MacBook' in lap.nama_laptop else '2800',
                'weight': '1,6' if 'MacBook' in lap.nama_laptop else '1,3'
            })
    else:
        laptops_data = fallback_laptops
        
    return render(request, 'it/inventori/setujuipengajuan_it.html', {
        'pengajuan_id': pengajuan_id,
        'laptops': laptops_data
    })

def tambahlaptop_it_view(request):
    return render(request, 'it/inventori/tambahlaptop_it.html')

def tambahspek_it_view(request):
    from inventori.models import Processor, RAM, Storage
    import uuid

    if request.method == 'POST':
        action = request.POST.get('action')
        try:
            if action == 'tambah_processor':
                p = Processor.objects.create(
                    id_processor=str(uuid.uuid4())[:8],
                    nama_processor=request.POST.get('nama_processor', ''),
                    manufacturer=request.POST.get('manufacturer', ''),
                    model=request.POST.get('model', ''),
                    cores=int(request.POST.get('cores') or 0),
                    threads=int(request.POST.get('threads') or 0),
                    base_clock=float(request.POST.get('base_clock') or 0.0),
                    max_clock=float(request.POST.get('max_clock') or 0.0),
                    arsitektur=request.POST.get('arsitektur', 'x86_64'),
                    keterangan=request.POST.get('keterangan', '')
                )
                messages.success(request, f'Processor {p.nama_processor} berhasil ditambahkan!')
            elif action == 'tambah_ram':
                r = RAM.objects.create(
                    id_ram=str(uuid.uuid4())[:8],
                    kapasitas_gb=int(request.POST.get('kapasitas_gb') or 0),
                    tipe=request.POST.get('tipe', ''),
                    keterangan=request.POST.get('keterangan', '')
                )
                messages.success(request, f'RAM {r.kapasitas_gb}GB berhasil ditambahkan!')
            elif action == 'tambah_storage':
                s = Storage.objects.create(
                    id_storage=str(uuid.uuid4())[:8],
                    kapasitas_gb=int(request.POST.get('kapasitas_gb') or 0),
                    tipe=request.POST.get('tipe', '')
                )
                messages.success(request, f'Storage {s.kapasitas_gb}GB berhasil ditambahkan!')
            return redirect('tambahspek_it')
        except Exception as e:
            messages.error(request, f'Gagal menyimpan data: {str(e)}')

    return render(request, 'it/dss/tambahspek_it.html')

def detaillaptop_it_view(request):
    return render(request, 'it/inventori/detaillaptop_it.html')

def riwayatpeminjamanlaptop_it_view(request):
    return render(request, 'it/inventori/riwayatpeminjamanlaptop_it.html')

def editdatalaptop_it_view(request):
    return render(request, 'it/inventori/editdatalaptop_it.html')

def inputkriteria_it_view(request):
    from inventori.models import Proyek
    import json
    proyek_qs = Proyek.objects.prefetch_related('roles__teknologi').all()
    proyek_data = []
    for p in proyek_qs:
        roles_data = []
        for r in p.roles.all():
            techs = [t.nama_teknologi for t in r.teknologi.all()]
            roles_data.append({
                'id_role': r.id_role,
                'nama_role': r.nama_role,
                'teknologi': techs
            })
        proyek_data.append({
            'id_proyek': p.id_proyek,
            'nama_proyek': p.nama_proyek,
            'roles': roles_data
        })
    proyek_json = json.dumps(proyek_data)
    return render(request, 'it/dss/inputkriteria_it.html', {'proyek_json': proyek_json})

def hasilrekomendasi_it_view(request):
    return render(request, 'it/dss/hasilrekomendasi_it.html')

def detailrekomendasi_it_view(request):
    return HttpResponse("<h3>IT Detail Rekomendasi - Mulai dari Awal</h3>")

def detailrekomendasiscrapping_it_view(request):
    return HttpResponse("<h3>IT Detail Scraping - Mulai dari Awal</h3>")

def notifikasi_it_view(request):
    return render(request, 'it/inventori/notifikasi_it.html')

# Procurement management views for IT
def manajemenpengadaan_it_view(request):
    return render(request, 'it/inventori/manajemenpengadaan_it.html')

def detailpengadaan_it_view(request):
    return render(request, 'it/inventori/detailpengadaan_it.html')

def editpengadaan_it_view(request):
    return render(request, 'it/inventori/editpengadaan_it.html')

def manajemenproyek_it_view(request):
    from inventori.models import Proyek
    proyek_list = Proyek.objects.prefetch_related('roles__teknologi').all()
    return render(request, 'it/inventori/manajemenproyek_it.html', {'proyek_list': proyek_list})

def tambahproyek_it_view(request):
    from inventori.models import Proyek, RoleProyek, TeknologiRole
    import uuid

    if request.method == 'POST':
        try:
            nama_proyek = request.POST.get('nama_proyek')
            role_names = request.POST.getlist('role_names[]')
            role_techs = request.POST.getlist('role_techs[]')

            # Create Proyek
            proyek = Proyek.objects.create(
                id_proyek=str(uuid.uuid4())[:8],
                nama_proyek=nama_proyek
            )

            # Create Roles and Technologies
            for name, tech_str in zip(role_names, role_techs):
                if name.strip():
                    role_obj = RoleProyek.objects.create(
                        id_role=str(uuid.uuid4())[:8],
                        proyek=proyek,
                        nama_role=name.strip()
                    )
                    # Split comma-separated techs
                    techs = [t.strip() for t in tech_str.split(',') if t.strip()]
                    for t in techs:
                        TeknologiRole.objects.create(
                            id_teknologi=str(uuid.uuid4())[:8],
                            role_proyek=role_obj,
                            nama_teknologi=t
                        )

            messages.success(request, f'Proyek "{nama_proyek}" berhasil ditambahkan!')
            return redirect('manajemen_proyek_it')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan proyek: {str(e)}')

    return render(request, 'it/inventori/tambahproyek_it.html')

def editproyek_it_view(request, id_proyek):
    from inventori.models import Proyek, RoleProyek, TeknologiRole
    import uuid

    try:
        proyek = Proyek.objects.prefetch_related('roles__teknologi').get(id_proyek=id_proyek)
    except Proyek.DoesNotExist:
        messages.error(request, 'Proyek tidak ditemukan.')
        return redirect('manajemen_proyek_it')

    if request.method == 'POST':
        try:
            proyek.nama_proyek = request.POST.get('nama_proyek')
            proyek.save()

            # Delete old roles and their technologies
            proyek.roles.all().delete()

            # Re-create roles and technologies
            role_names = request.POST.getlist('role_names[]')
            role_techs = request.POST.getlist('role_techs[]')

            for name, tech_str in zip(role_names, role_techs):
                if name.strip():
                    role_obj = RoleProyek.objects.create(
                        id_role=str(uuid.uuid4())[:8],
                        proyek=proyek,
                        nama_role=name.strip()
                    )
                    techs = [t.strip() for t in tech_str.split(',') if t.strip()]
                    for t in techs:
                        TeknologiRole.objects.create(
                            id_teknologi=str(uuid.uuid4())[:8],
                            role_proyek=role_obj,
                            nama_teknologi=t
                        )

            messages.success(request, f'Proyek "{proyek.nama_proyek}" berhasil diperbarui!')
            return redirect('manajemen_proyek_it')
        except Exception as e:
            messages.error(request, f'Gagal memperbarui proyek: {str(e)}')

    return render(request, 'it/inventori/editproyek_it.html', {'proyek': proyek})

def hapusproyek_it_view(request, id_proyek):
    from inventori.models import Proyek

    if request.method == 'POST':
        try:
            proyek = Proyek.objects.get(id_proyek=id_proyek)
            nama = proyek.nama_proyek
            proyek.delete()
            messages.success(request, f'Proyek "{nama}" berhasil dihapus!')
        except Proyek.DoesNotExist:
            messages.error(request, 'Proyek tidak ditemukan.')
        except Exception as e:
            messages.error(request, f'Gagal menghapus proyek: {str(e)}')

    return redirect('manajemen_proyek_it')


# ==========================================
# 3. TALENT VIEWS
# ==========================================

def dashboard_talent_view(request):
    return render(request, 'talent/dashboard/dashboard_talent.html')

def pengajuanlaptop_talent_view(request):
    return render(request, 'talent/inventori/pengajuanlaptop_talent.html')

def riwayatpeminjamanlaptop_talent_view(request):
    return render(request, 'talent/inventori/riwayatpeminjamanlaptop_talent.html')

def pengembalianlaptop_talent_view(request):
    return render(request, 'talent/inventori/pengembalianlaptop_talent.html')

def detaillaptop_talent_view(request):
    return render(request, 'talent/inventori/detaillaptop_talent.html')


