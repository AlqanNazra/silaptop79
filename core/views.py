from django.shortcuts import render, redirect
from django.http import HttpResponse

# ==========================================
# 1. HUMAN CAPITAL (HC) VIEWS
# ==========================================

from inventori.models import LaptopInventori, Processor, RAM, Storage, User
from inventori.services.service_pengajuan import PengajuanService
from inventori.services.service_peminjaman import PeminjamanService
from inventori.dto.dto_laptop_inventori import LaptopInventoriDTO
from inventori.services.laptop_inventori.create import CreateLaptopInventoriService
from inventori.services.laptop_inventori.update import UpdateLaptopInventoriService
from inventori.services.laptop_inventori.delete import DeleteLaptopInventoriService
from django.contrib import messages
from inventori.dto.dto_pengajuan import PengajuanDTO
from inventori.dto.dto_peminjaman import PeminjamanDTO

def dashboard_hc_view(request):
    try:
        total_laptop = LaptopInventori.objects.count()
        service = PengajuanService()
        semua_pengajuan = service.service_ambil_semua_pengajuan()
        total_pengajuan = len(semua_pengajuan)
        pengajuan_pending = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'pending')
    except Exception:
        total_laptop = 0
        total_pengajuan = 0
        pengajuan_pending = 0

    context = {
        'total_laptop': total_laptop,
        'total_pengajuan': total_pengajuan,
        'pengajuan_pending': pengajuan_pending,
    }
    return render(request, 'hc/dashboard/dashboard_hc.html', context)
def manajemenlaptop_hc_view(request):
    return render(request, 'hc/inventori/manajemenlaptop_hc.html')

def pengajuanlaptop_it_view(request):
    try:
        service = PengajuanService()
        semua_pengajuan = service.service_ambil_semua_pengajuan()
        
        # Sort by date descending
        semua_pengajuan.sort(key=lambda x: x.tanggal_pengajuan, reverse=True)
        
        # Calculate statistics
        total_pengajuan = len(semua_pengajuan)
        total_pending = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'pending')
        total_disetujui = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'approved')
        total_ditolak = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'rejected')

        context = {
            'list_pengajuan': semua_pengajuan,
            'total_pengajuan': total_pengajuan,
            'total_pending': total_pending,
            'total_disetujui': total_disetujui,
            'total_ditolak': total_ditolak,
        }
    except Exception as e:
        context = {
            'error_message': f'Gagal memuat data pengajuan: {str(e)}',
            'list_pengajuan': [],
            'total_pengajuan': 0,
            'total_pending': 0,
            'total_disetujui': 0,
            'total_ditolak': 0,
        }

    return render(request, 'it/inventori/pengajuanlaptop_it.html', context)

def detailpengajuan_it_view(request):
    id_pengajuan = request.GET.get('id')
    if not id_pengajuan:
        messages.error(request, 'ID Pengajuan tidak diberikan.')
        return redirect('pengajuanlaptop_it')

    try:
        service = PengajuanService()
        pengajuan = service.service_cari_pengajuan_by_id(id_pengajuan)
        
        if not pengajuan:
            messages.error(request, 'Data pengajuan tidak ditemukan.')
            return redirect('pengajuanlaptop_it')

        user_obj = User.objects.filter(id_user=pengajuan.id_user).first()
        pengajuan.user_nama = user_obj.nama if user_obj else pengajuan.id_user

        if request.method == 'POST':
            action = request.POST.get('action')
            if action in ['approved', 'rejected']:
                user_id = request.user.id_user if hasattr(request.user, 'id_user') else None
                
                dto = PengajuanDTO(
                    id_pengajuan=id_pengajuan,
                    status=action,
                    approved_by=user_id
                )
                service.service_approve_pengajuan(dto)
                messages.success(request, f'Pengajuan berhasil di-{action}.')
                return redirect('pengajuanlaptop_it')

        context = {
            'pengajuan': pengajuan
        }
        return render(request, 'it/inventori/detailpengajuan_it.html', context)
        
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
        return redirect('pengajuanlaptop_it')

def tambahlaptop_it_view(request):
    processors = Processor.objects.all()
    rams = RAM.objects.all()
    storages = Storage.objects.all()

    if request.method == 'POST':
        try:
            import re
            raw_layar = request.POST.get('ukuran_layar')
            layar_val = None
            if raw_layar:
                match = re.search(r'\d+(?:\.\d+)?', str(raw_layar))
                if match:
                    try:
                        layar_val = float(match.group(0))
                    except ValueError:
                        pass

            dto = LaptopInventoriDTO(
                nama_laptop=request.POST.get('nama_laptop'),
                model=request.POST.get('model'),
                os=request.POST.get('os'),
                kondisi=request.POST.get('kondisi', 'baik'),
                status=request.POST.get('status', 'tersedia'),
                lokasi=request.POST.get('lokasi'),
                id_processor=request.POST.get('id_processor') or None,
                id_ram=request.POST.get('id_ram') or None,
                id_storage=request.POST.get('id_storage') or None,
                ukuran_layar=layar_val,
            )
            service = CreateLaptopInventoriService()
            service.execute(dto)
            messages.success(request, 'Laptop berhasil ditambahkan ke inventori!')
            return redirect('manajemen_laptop_it')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan laptop: {str(e)}')

    context = {
        'processors': processors,
        'rams': rams,
        'storages': storages,
    }
    return render(request, 'it/inventori/tambahlaptop_it.html', context)

def detaillaptop_it_view(request, id_laptop):
    try:
        laptop = LaptopInventori.objects.select_related(
            'id_processor', 'id_ram', 'id_storage'
        ).get(id_laptop_inventori=id_laptop)
    except LaptopInventori.DoesNotExist:
        messages.error(request, 'Laptop tidak ditemukan.')
        return redirect('manajemen_laptop_it')

    processors = Processor.objects.all()
    rams = RAM.objects.all()
    storages = Storage.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'hapus':
            try:
                service = DeleteLaptopInventoriService()
                service.execute(id_laptop)
                messages.success(request, f'Laptop {laptop.nama_laptop} berhasil dihapus.')
                return redirect('manajemen_laptop_it')
            except Exception as e:
                messages.error(request, f'Gagal menghapus: {str(e)}')

        elif action == 'update':
            try:
                update_service = UpdateLaptopInventoriService()
                kondisi = request.POST.get('kondisi')
                status = request.POST.get('status')
                lokasi = request.POST.get('lokasi')

                if kondisi:
                    update_service.update_kondisi(id_laptop, kondisi)
                if status:
                    update_service.update_status(id_laptop, status, lokasi)

                messages.success(request, 'Data laptop berhasil diperbarui.')
                return redirect('detaillaptop_it', id_laptop=id_laptop)
            except Exception as e:
                messages.error(request, f'Gagal update: {str(e)}')

    context = {
        'laptop': laptop,
        'processors': processors,
        'rams': rams,
        'storages': storages,
    }
    return render(request, 'it/inventori/detaillaptop_it.html', context)

def riwayatpeminjamanlaptop_it_view(request):
    try:
        service = PeminjamanService()
        riwayat_list = service.service_ambil_semua_peminjaamn()
        
        users_dict = {u.id_user: u.nama for u in User.objects.all()}
        users_role_dict = {u.id_user: u.role for u in User.objects.all()}
        laptops_dict = {l.id_laptop_inventori: l.nama_laptop for l in LaptopInventori.objects.all()}
        
        for p in riwayat_list:
            p.user_nama = users_dict.get(p.id_user, p.id_user)
            p.user_role = users_role_dict.get(p.id_user, "-")
            p.laptop_nama = laptops_dict.get(p.id_laptop_inventori, p.id_laptop_inventori)
            
        total_peminjaman = len(riwayat_list)
        peminjam_terakhir = "-"
        sorted_p = sorted(riwayat_list, key=lambda x: str(x.tanggal_pinjam) if x.tanggal_pinjam else "", reverse=True)
        if sorted_p:
            peminjam_terakhir = sorted_p[0].user_nama
            
        context = {
            'list_peminjaman': riwayat_list,
            'total_peminjaman': total_peminjaman,
            'peminjam_terakhir': peminjam_terakhir,
        }
    except Exception as e:
        messages.error(request, f'Gagal memuat riwayat: {str(e)}')
        context = {
            'list_peminjaman': [],
            'total_peminjaman': 0,
            'peminjam_terakhir': "-",
        }
    return render(request, 'it/inventori/riwayatpeminjamanlaptop_it.html', context)

def editdatalaptop_hc_view(request):
    return render(request, 'hc/inventori/editdatalaptop_hc.html')

def inputkriteria_hc_view(request):
    import sys
    import os
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_path not in sys.path:
        sys.path.append(base_path)
    from simulate_saw import BASE_BOBOT_RAW

    if request.method == 'POST':
        try:
            b_processor = float(request.POST.get('bobot_processor', 7))
            b_ram = float(request.POST.get('bobot_ram', 5))
            b_storage = float(request.POST.get('bobot_storage', 4))
            b_berat = float(request.POST.get('bobot_berat', 2))
            b_layar = float(request.POST.get('bobot_layar', 2))
            b_baterai = float(request.POST.get('bobot_baterai', 6))

            raw_weights = [
                {"id_kriteria": "K01", "nama_kriteria": "processor", "tipe_kriteria": "benefit", "nilai_bobot": b_processor},
                {"id_kriteria": "K02", "nama_kriteria": "ram",       "tipe_kriteria": "benefit", "nilai_bobot": b_ram},
                {"id_kriteria": "K03", "nama_kriteria": "storage",   "tipe_kriteria": "benefit", "nilai_bobot": b_storage},
                {"id_kriteria": "K04", "nama_kriteria": "berat",     "tipe_kriteria": "cost",    "nilai_bobot": b_berat},
                {"id_kriteria": "K05", "nama_kriteria": "layar",     "tipe_kriteria": "benefit", "nilai_bobot": b_layar},
                {"id_kriteria": "K06", "nama_kriteria": "baterai",   "tipe_kriteria": "benefit", "nilai_bobot": b_baterai},
            ]
            request.session['dss_raw_weights'] = raw_weights
            return redirect('hasilrekomendasi_hc')
        except Exception as e:
    processors = Processor.objects.all()
    rams = RAM.objects.all()
    storages = Storage.objects.all()

    context = {
        'processors': processors,
        'rams': rams,
        'storages': storages,
    }
    return render(request, 'hc/dss/inputkriteria_hc.html', context)

def hasilrekomendasi_hc_view(request):
    import sys
    import os
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_path not in sys.path:
        sys.path.append(base_path)
    from simulate_saw import DUMMY_LAPTOPS, DummySawService, BASE_BOBOT_RAW

    raw_weights = request.session.get('dss_raw_weights', BASE_BOBOT_RAW)
    service = DummySawService(raw_weights)
    
    data_pre = [d.copy() for d in DUMMY_LAPTOPS]
    data_normalisasi = service.normalisasi_saw(data_pre)
    hasil_saw = service.hitung_saw_data(data_normalisasi, ["dummy_role"])
    ranking = service.ranking_saw(hasil_saw)
    
    laptop_map = {l['id']: l for l in DUMMY_LAPTOPS}
    for i, item in enumerate(ranking, start=1):
        item["rank"] = i
        item["detail"] = laptop_map.get(item["id"])

    context = {
        'ranking': ranking,
        'top_3': ranking[:3],
        'total_alternatif': len(ranking),
        'rata_rata_harga': 15000000,
        'skor_tertinggi': ranking[0]['skor'] if ranking else 0,
    }
    return render(request, 'hc/dss/hasilrekomendasi_hc.html', context)

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
    try:
        total_laptop = LaptopInventori.objects.count()
        service = PengajuanService()
        semua_pengajuan = service.service_ambil_semua_pengajuan()
        total_pengajuan = len(semua_pengajuan)
        pengajuan_pending = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'pending')
    except Exception:
        total_laptop = 0
        total_pengajuan = 0
        pengajuan_pending = 0

    context = {
        'total_laptop': total_laptop,
        'total_pengajuan': total_pengajuan,
        'pengajuan_pending': pengajuan_pending,
    }
    return render(request, 'it/dashboard/dashboard_it.html', context)

def manajemenlaptop_it_view(request):
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    laptops = LaptopInventori.objects.select_related('id_processor', 'id_ram', 'id_storage').all()

    if search_query:
        laptops = laptops.filter(nama_laptop__icontains=search_query) | \
                  laptops.filter(no_inventori__icontains=search_query)

    if status_filter:
        laptops = laptops.filter(status=status_filter)

    context = {
        'laptops': laptops,
        'total': laptops.count(),
        'search_query': search_query,
        'status_filter': status_filter,
    }
    return render(request, 'it/inventori/manajemenlaptop_it.html', context)



def editdatalaptop_it_view(request, id_laptop):
    try:
        laptop = LaptopInventori.objects.get(id_laptop_inventori=id_laptop)
    except LaptopInventori.DoesNotExist:
        messages.error(request, 'Laptop tidak ditemukan.')
        return redirect('manajemen_laptop_it')

    if request.method == 'POST':
        try:
            update_service = UpdateLaptopInventoriService()
            kondisi = request.POST.get('kondisi')
            status = request.POST.get('status')
            lokasi = request.POST.get('lokasi')

            if kondisi:
                update_service.update_kondisi(id_laptop, kondisi)
            if status:
                update_service.update_status(id_laptop, status, lokasi)

            # Update spesifikasi
            id_processor = request.POST.get('id_processor')
            id_ram = request.POST.get('id_ram')
            id_storage = request.POST.get('id_storage')
            
            if id_processor and id_ram and id_storage:
                dto = LaptopInventoriDTO(
                    nama_laptop=laptop.nama_laptop,
                    model=laptop.model,
                    os=laptop.os,
                    kondisi=kondisi or laptop.kondisi,
                    status=status or laptop.status,
                    lokasi=lokasi or laptop.lokasi,
                    id_processor=id_processor,
                    id_ram=id_ram,
                    id_storage=id_storage,
                    id_laptop_inventori=id_laptop
                )
                update_service.update_spek(dto)

            messages.success(request, 'Data laptop berhasil diperbarui.')
            return redirect('detaillaptop_it', id_laptop=id_laptop)
        except Exception as e:
            messages.error(request, f'Gagal mengupdate laptop: {str(e)}')

    processors = Processor.objects.all()
    rams = RAM.objects.all()
    storages = Storage.objects.all()
    
    context = {
        'laptop': laptop,
        'processors': processors,
        'rams': rams,
        'storages': storages,
    }
    return render(request, 'it/inventori/editdatalaptop_it.html', context)

def inputkriteria_it_view(request):
    import sys
    import os
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_path not in sys.path:
        sys.path.append(base_path)
    from simulate_saw import BASE_BOBOT_RAW

    if request.method == 'POST':
        try:
            b_processor = float(request.POST.get('bobot_processor', 7))
            b_ram = float(request.POST.get('bobot_ram', 5))
            b_storage = float(request.POST.get('bobot_storage', 4))
            b_berat = float(request.POST.get('bobot_berat', 2))
            b_layar = float(request.POST.get('bobot_layar', 2))
            b_baterai = float(request.POST.get('bobot_baterai', 6))

            raw_weights = [
                {"id_kriteria": "K01", "nama_kriteria": "processor", "tipe_kriteria": "benefit", "nilai_bobot": b_processor},
                {"id_kriteria": "K02", "nama_kriteria": "ram",       "tipe_kriteria": "benefit", "nilai_bobot": b_ram},
                {"id_kriteria": "K03", "nama_kriteria": "storage",   "tipe_kriteria": "benefit", "nilai_bobot": b_storage},
                {"id_kriteria": "K04", "nama_kriteria": "berat",     "tipe_kriteria": "cost",    "nilai_bobot": b_berat},
                {"id_kriteria": "K05", "nama_kriteria": "layar",     "tipe_kriteria": "benefit", "nilai_bobot": b_layar},
                {"id_kriteria": "K06", "nama_kriteria": "baterai",   "tipe_kriteria": "benefit", "nilai_bobot": b_baterai},
            ]
            request.session['dss_raw_weights'] = raw_weights
            return redirect('hasilrekomendasi_it')
        except Exception as e:
            messages.error(request, f'Gagal memproses kriteria: {str(e)}')

    processors = Processor.objects.all()
    rams = RAM.objects.all()
    storages = Storage.objects.all()

    context = {
        'processors': processors,
        'rams': rams,
        'storages': storages,
    }
    return render(request, 'it/dss/inputkriteria_it.html', context)

def hasilrekomendasi_it_view(request):
    import sys
    import os
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_path not in sys.path:
        sys.path.append(base_path)
    from simulate_saw import DUMMY_LAPTOPS, DummySawService, BASE_BOBOT_RAW

    raw_weights = request.session.get('dss_raw_weights', BASE_BOBOT_RAW)
    service = DummySawService(raw_weights)
    
    data_pre = [d.copy() for d in DUMMY_LAPTOPS]
    data_normalisasi = service.normalisasi_saw(data_pre)
    hasil_saw = service.hitung_saw_data(data_normalisasi, ["dummy_role"])
    ranking = service.ranking_saw(hasil_saw)
    
    laptop_map = {l['id']: l for l in DUMMY_LAPTOPS}
    for i, item in enumerate(ranking, start=1):
        item["rank"] = i
        item["detail"] = laptop_map.get(item["id"])

    context = {
        'ranking': ranking,
        'top_3': ranking[:3],
        'total_alternatif': len(ranking),
        'rata_rata_harga': 15000000,
        'skor_tertinggi': ranking[0]['skor'] if ranking else 0,
    }
    return render(request, 'it/dss/hasilrekomendasi_it.html', context)

def detailrekomendasi_it_view(request):
    import sys
    import os
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_path not in sys.path:
        sys.path.append(base_path)
    from simulate_saw import DUMMY_LAPTOPS

    laptop_id = request.GET.get('id')
    laptop = next((l for l in DUMMY_LAPTOPS if l['id'] == laptop_id), None)
    if not laptop:
        messages.error(request, 'Laptop tidak ditemukan.')
        return redirect('hasilrekomendasi_it')

    context = {
        'laptop': laptop
    }
    return render(request, 'it/dss/detailrekomendasi_it.html', context)

def detailrekomendasiscrapping_it_view(request):
    import sys
    import os
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_path not in sys.path:
        sys.path.append(base_path)
    from simulate_saw import DUMMY_LAPTOPS

    laptop_id = request.GET.get('id')
    laptop = next((l for l in DUMMY_LAPTOPS if l['id'] == laptop_id), None)
    if not laptop:
        messages.error(request, 'Laptop tidak ditemukan.')
        return redirect('hasilrekomendasi_it')

    context = {
        'laptop': laptop
    }
    return render(request, 'it/dss/detailrekomendasiscrapping_it.html', context)

def notifikasi_it_view(request):
    return render(request, 'it/inventori/notifikasi_it.html')


# ==========================================
# 3. TALENT VIEWS
# ==========================================

def dashboard_talent_view(request):
    try:
        user_id = request.user.id_user if hasattr(request.user, 'id_user') else None
        
        service_pengajuan = PengajuanService()
        semua_pengajuan = service_pengajuan.service_ambil_semua_pengajuan()
        if user_id:
            semua_pengajuan = [p for p in semua_pengajuan if getattr(p, 'id_user', None) == user_id]
            
        total_pending = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'pending')
        total_ditolak = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'rejected')
        total_disetujui = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'approved')
        
        service_peminjaman = PeminjamanService()
        semua_peminjaman = service_peminjaman.service_ambil_semua_peminjaman()
        if user_id:
            semua_peminjaman = [p for p in semua_peminjaman if getattr(p, 'id_user', None) == user_id]
            
        total_selesai = sum(1 for p in semua_peminjaman if p.status and p.status.lower() in ['selesai', 'dikembalikan'])
        
        semua_pengajuan.sort(key=lambda x: x.tanggal_pengajuan, reverse=True)
        recent_pengajuan = semua_pengajuan[:5]

        context = {
            'total_pending': total_pending,
            'total_ditolak': total_ditolak,
            'total_disetujui': total_disetujui,
            'total_selesai': total_selesai,
            'recent_pengajuan': recent_pengajuan
        }
    except Exception as e:
        context = {
            'error_message': str(e),
            'total_pending': 0,
            'total_ditolak': 0,
            'total_disetujui': 0,
            'total_selesai': 0,
            'recent_pengajuan': []
        }
    return render(request, 'talent/dashboard/dashboard_talent.html', context)

def pengajuanlaptop_talent_view(request):
    try:
        user_id = request.user.id_user if hasattr(request.user, 'id_user') else None
        service = PengajuanService()

        if request.method == 'POST':
            from datetime import datetime
            departemen = request.POST.get('departemen') or 'Internal'
            role = request.POST.get('role') or 'Unknown'
            spesifikasi = request.POST.get('spesifikasi') or '-'
            alasan = request.POST.get('alasan') or '-'

            dto = PengajuanDTO(
                id_user=user_id,
                kebutuhan_role=role,
                kebutuhan_requirement=spesifikasi,
                bulan=datetime.now().date(),
                keterangan=alasan,
                perusahaan=departemen,
                status='pending'
            )
            # The method is named service_tambah_peminjaman but actually creates pengajuan
            service.service_tambah_peminjaman(dto)
            messages.success(request, 'Pengajuan laptop berhasil dikirim.')
            return redirect('dashboard_talent')

        semua_pengajuan = service.service_ambil_semua_pengajuan()
        if user_id:
            semua_pengajuan = [p for p in semua_pengajuan if getattr(p, 'id_user', None) == user_id]
            
        semua_pengajuan.sort(key=lambda x: x.tanggal_pengajuan, reverse=True)
        
        context = {
            'list_pengajuan': semua_pengajuan,
            'total_pengajuan': len(semua_pengajuan),
        }
    except Exception as e:
        messages.error(request, f'Gagal mengirim pengajuan: {str(e)}')
        context = {
            'error_message': f'Gagal memuat data pengajuan: {str(e)}',
            'list_pengajuan': [],
            'total_pengajuan': 0,
        }
    return render(request, 'talent/inventori/pengajuanlaptop_talent.html', context)

def detaillaptop_talent_view(request):
    user_id = request.user.id_user if hasattr(request.user, 'id_user') else None
    service = PeminjamanService()
    active_laptop = None
    try:
        riwayat_list = service.service_ambil_semua_peminjaman()
        if user_id:
            riwayat_list = [p for p in riwayat_list if getattr(p, 'id_user', None) == user_id]
        
        active_peminjaman = next((r for r in riwayat_list if r.status and r.status.lower() in ['dipinjam', 'aktif']), None)
        if active_peminjaman:
            active_laptop = LaptopInventori.objects.select_related('id_processor', 'id_ram', 'id_storage').filter(id_laptop_inventori=active_peminjaman.id_laptop_inventori).first()
    except Exception as e:
        messages.error(request, f'Gagal memuat detail laptop: {str(e)}')

    context = {
        'laptop': active_laptop
    }
    return render(request, 'talent/inventori/detaillaptop_talent.html', context)

def riwayatpeminjamanlaptop_talent_view(request):
    try:
        user_id = request.user.id_user if hasattr(request.user, 'id_user') else None
        service = PeminjamanService()
        riwayat_list = service.service_ambil_semua_peminjaman()
        
        if user_id:
            riwayat_list = [p for p in riwayat_list if getattr(p, 'id_user', None) == user_id]
            
        total_peminjaman = len(riwayat_list)
        total_aktif = sum(1 for r in riwayat_list if r.status and r.status.lower() in ['dipinjam', 'aktif'])
        total_selesai = sum(1 for r in riwayat_list if r.status and r.status.lower() in ['selesai', 'dikembalikan'])
        
        # Populate laptop details for each peminjaman
        for p in riwayat_list:
            laptop = LaptopInventori.objects.filter(id_laptop_inventori=p.id_laptop_inventori).first()
            if laptop:
                p.nama_laptop = laptop.nama_laptop
                p.no_inventori = laptop.no_inventori
            else:
                p.nama_laptop = "Unknown Laptop"
                p.no_inventori = p.id_laptop_inventori

        active_peminjaman = next((r for r in riwayat_list if r.status and r.status.lower() in ['dipinjam', 'aktif']), None)
        active_laptop = None
        if active_peminjaman:
            active_laptop = LaptopInventori.objects.filter(id_laptop_inventori=active_peminjaman.id_laptop_inventori).first()
            
        context = {
            'riwayat_list': riwayat_list,
            'total_peminjaman': total_peminjaman,
            'total_aktif': total_aktif,
            'total_selesai': total_selesai,
            'active_peminjaman': active_peminjaman,
            'active_laptop': active_laptop,
        }
    except Exception as e:
        context = {
            'error_message': f'Gagal memuat riwayat: {str(e)}',
            'riwayat_list': [],
            'total_peminjaman': 0,
            'total_aktif': 0,
            'total_selesai': 0,
            'active_peminjaman': None,
            'active_laptop': None,
        }
    return render(request, 'talent/inventori/riwayatpeminjamanlaptop_talent.html', context)

def pengembalianlaptop_talent_view(request):
    user_id = request.user.id_user if hasattr(request.user, 'id_user') else None
    if not user_id:
        messages.error(request, 'Anda harus login terlebih dahulu.')
        return redirect('login')

    service = PeminjamanService()
    try:
        riwayat_list = service.service_ambil_semua_peminjaman()
        if user_id:
            riwayat_list = [p for p in riwayat_list if getattr(p, 'id_user', None) == user_id]
        
        active_peminjaman = next((r for r in riwayat_list if r.status and r.status.lower() in ['dipinjam', 'aktif']), None)
        
        if request.method == 'POST':
            if not active_peminjaman:
                messages.error(request, 'Gagal memproses pengembalian: Anda tidak memiliki peminjaman aktif.')
                return redirect('riwayatpeminjamanlaptop_talent')
            
            alasan = request.POST.get('alasan') or 'Selesai Kontrak/Proyek'
            catatan = request.POST.get('catatan') or ''
            kondisi = request.POST.get('kondisi') or 'good'
            
            if kondisi == 'good':
                db_kondisi = 'baik'
            elif kondisi == 'damaged':
                db_kondisi = 'rusak_ringan'
            else:
                db_kondisi = 'rusak_berat'
                
            laptop = LaptopInventori.objects.filter(id_laptop_inventori=active_peminjaman.id_laptop_inventori).first()
            lokasi = laptop.lokasi if laptop else 'Kantor Pusat'
            
            dto = PeminjamanDTO(
                id_peminjaman=active_peminjaman.id_peminjaman,
                keterangan=f"{alasan} - {catatan}",
                status='selesai'
            )
            dto.lokasi = lokasi
            
            service.service_pengembalian_laptop(dto)
            
            if laptop:
                if db_kondisi != 'baik':
                    laptop.kondisi = db_kondisi
                    laptop.status = 'rusak'
                else:
                    laptop.status = 'tersedia'
                laptop.save()
            
            messages.success(request, 'Pengembalian perangkat berhasil diajukan.')
            return redirect('riwayatpeminjamanlaptop_talent')
            
        if not active_peminjaman:
            messages.error(request, 'Anda tidak memiliki perangkat aktif yang perlu dikembalikan.')
            return redirect('riwayatpeminjamanlaptop_talent')
            
        active_laptop = LaptopInventori.objects.filter(id_laptop_inventori=active_peminjaman.id_laptop_inventori).first()
        
        context = {
            'active_peminjaman': active_peminjaman,
            'active_laptop': active_laptop,
        }
        return render(request, 'talent/inventori/pengembalianlaptop_talent.html', context)
        
    except Exception as e:
        import traceback; traceback.print_exc()
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
        return redirect('riwayatpeminjamanlaptop_talent')

def editdatalaptop_talent_view(request):
    return HttpResponse("<h3>Talent Edit Laptop - Mulai dari Awal</h3>")

def inputkriteria_talent_view(request):
    return HttpResponse("<h3>Talent Input Kriteria - Mulai dari Awal</h3>")

def hasilrekomendasi_talent_view(request):
    return HttpResponse("<h3>Talent Hasil Rekomendasi - Mulai dari Awal</h3>")

def detailrekomendasi_talent_view(request):
    return HttpResponse("<h3>Talent Detail Rekomendasi - Mulai dari Awal</h3>")

def detailrekomendasiscrapping_talent_view(request):
    return HttpResponse("<h3>Talent Detail Scraping - Mulai dari Awal</h3>")

def login_redirect_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    role = getattr(request.user, 'role', '').upper()
    if role == 'HC':
        return redirect('dashboardhc')
    elif role == 'IT':
        return redirect('dashboard_it')
    elif role in ('TALENT', 'EMPLOYEE'):
        return redirect('dashboard_talent')
    return redirect('dashboardhc')

def home_view(request):
    return login_redirect_view(request)


# Procurement management views for IT (Added to fix NoReverseMatch)
def manajemenpengadaan_it_view(request):
    return render(request, 'it/inventori/manajemenpengadaan_it.html')

def detailpengadaan_it_view(request):
    return render(request, 'it/inventori/detailpengadaan_it.html')

def editpengadaan_it_view(request):
    return render(request, 'it/inventori/editpengadaan_it.html')

def setujui_pengajuan_it_view(request):
    from inventori.models import LaptopInventori
    pengajuan_id = request.GET.get('id', '1')
    available_laptops = LaptopInventori.objects.filter(status__iexact='Available')
    return render(request, 'it/inventori/setujuipengajuan_it.html', {
        'pengajuan_id': pengajuan_id,
        'laptops': available_laptops
    })


