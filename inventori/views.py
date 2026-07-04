import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.shortcuts import render

from inventori.models import LaptopInventori, Processor, RAM, Storage
from inventori.dto.dto_processor import ProcessorDTO
from inventori.services.processor.create import CreateProcessorService
from inventori.services.processor.read import ReadProcessorService
from inventori.services.processor.update import UpdateProcessorService
from inventori.services.processor.delete import DeleteProcessorService

from inventori.dto.dto_laptop_inventori import LaptopInventoriDTO
from inventori.services.laptop_inventori.create import CreateLaptopInventoriService
from inventori.services.laptop_inventori.read import ReadLaptopInventoriService
from inventori.services.laptop_inventori.update import UpdateLaptopInventoriService
from inventori.services.laptop_inventori.delete import DeleteLaptopInventoriService

from inventori.services.service_pengajuan import PengajuanService
from inventori.services.service_peminjaman import PeminjamanService
from inventori.repositories.dto.dto_pengajuan import PengajuanDTO
from inventori.repositories.dto.dto_peminjaman import PeminjamanDTO

from inventori.services.service_ram import RamService
from inventori.services.service_storage import StorageService
# =============================================
# HELPER: Response standar (JSON)
# =============================================
def success_response(data=None, message="Berhasil", status=200):
    return JsonResponse({"status": "success", "message": message, "data": data}, status=status, safe=False)

def error_response(message="Terjadi kesalahan", status=400):
    return JsonResponse({"status": "error", "message": message}, status=status)

def _parse_body(request):
    return json.loads(request.body)


# =============================================================================
#   PAGE VIEWS (Server-Side Rendering ke Template HTML)
# =============================================================================

# @login_required
def manajemen_laptop_page(request):
    """
    Halaman daftar inventori laptop.
    Mengambil data dari database via ORM lalu render ke template.
    """
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    ram_filter = request.GET.get('ram', '').strip()
    storage_filter = request.GET.get('storage', '').strip()

    try:
        per_page = int(request.GET.get('per_page', 10))
        if per_page not in [10, 15, 25]:
            per_page = 10
    except ValueError:
        per_page = 10

    laptops = LaptopInventori.objects.select_related('id_processor', 'id_ram', 'id_storage').all()

    if search_query:
        from django.db.models import Q
        laptops = laptops.filter(
            Q(nama_laptop__icontains=search_query) |
            Q(no_inventori__icontains=search_query) |
            Q(model__icontains=search_query)
        )

    if status_filter:
        laptops = laptops.filter(status=status_filter)

    if ram_filter:
        laptops = laptops.filter(id_ram__kapasitas_gb=ram_filter)

    if storage_filter:
        laptops = laptops.filter(id_storage__kapasitas_gb=storage_filter)

    laptops = laptops.order_by('id_laptop_inventori')

    from django.core.paginator import Paginator
    paginator = Paginator(laptops, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'laptops': page_obj,
        'total': laptops.count(),
        'search_query': search_query,
        'status_filter': status_filter,
        'ram_filter': ram_filter,
        'storage_filter': storage_filter,
        'per_page': per_page,
    }
    return render(request, 'hc/inventori/manajemenlaptop_hc.html', context)



# @login_required
def pengajuan_page_view(request):
    """
    Halaman daftar pengajuan laptop.
    Mengambil data dari PengajuanService lalu render ke template.
    """
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    start_date_filter = request.GET.get('start_date', '').strip()
    end_date_filter = request.GET.get('end_date', '').strip()
    bulan_filter = request.GET.get('bulan', '').strip()
    active_tab = request.GET.get('tab', 'belum_disetujui').strip().lower()

    try:
        per_page = int(request.GET.get('per_page', 10))
        if per_page not in [10, 15, 25]:
            per_page = 10
    except ValueError:
        per_page = 10

    try:
        service = PengajuanService()
        semua_pengajuan = service.service_ambil_semua_pengajuan()
        
        from inventori.models import User, Peminjaman
        users_dict = {u.id_user: u.nama for u in User.objects.all()}
        
        peminjamans = Peminjaman.objects.all()
        peminjaman_map = {}
        for p in peminjamans:
            pengajuan_id = p.id_pengajuan_id
            if pengajuan_id not in peminjaman_map:
                peminjaman_map[pengajuan_id] = []
            peminjaman_map[pengajuan_id].append(p)

        # Categorize the pengajuan
        belum_disetujui_list = []
        sedang_berlangsung_list = []
        riwayat_selesai_list = []
        
        total_menunggu = 0
        total_disetujui = 0
        total_ditolak = 0

        for p in semua_pengajuan:
            p.user_nama = users_dict.get(p.id_user, f"User {p.id_user}")
            
            p_loans = peminjaman_map.get(p.id_pengajuan, [])
            is_approved = p.status and p.status.lower() in ['disetujui', 'approved', 'selesai']
            is_rejected = p.status and p.status.lower() in ['ditolak', 'rejected']
            is_pending = not is_approved and not is_rejected
            
            if is_pending:
                total_menunggu += 1
            if is_approved:
                total_disetujui += 1
            if is_rejected:
                total_ditolak += 1
            
            # Jika ditolak, langsung hilang (tidak dimasukkan ke list manapun)
            if is_rejected:
                continue

            if not is_approved:
                belum_disetujui_list.append(p)
                p.status_display = 'menunggu'
            else:
                has_completed = (p.status.lower() == 'selesai') or any(l.status.lower() == 'selesai' for l in p_loans)
                if has_completed:
                    riwayat_selesai_list.append(p)
                    p.status_display = 'selesai'
                else:
                    has_ready = any(l.status.lower() == 'ready' for l in p_loans)
                    if has_ready:
                        # Jika belum diambil oleh talent, hold dulu di belum_disetujui_list dengan status 'belum diambil'
                        belum_disetujui_list.append(p)
                        p.status_display = 'belum diambil'
                    else:
                        sedang_berlangsung_list.append(p)
                        has_returned = any(l.status.lower() == 'dikembalikan' for l in p_loans)
                        if has_returned:
                            p.status_display = 'dikembalikan'
                        else:
                            p.status_display = 'dipinjam'

        # Count statistics for each tab/category
        total_belum_disetujui = len(belum_disetujui_list)
        total_sedang_berlangsung = len(sedang_berlangsung_list)
        total_riwayat_selesai = len(riwayat_selesai_list)
        total = total_belum_disetujui + total_sedang_berlangsung + total_riwayat_selesai

        # Select target list based on active tab
        if active_tab == 'sedang_berlangsung':
            filtered_pengajuan = sedang_berlangsung_list
        elif active_tab == 'riwayat_selesai':
            filtered_pengajuan = riwayat_selesai_list
        else:
            active_tab = 'belum_disetujui'
            filtered_pengajuan = belum_disetujui_list

        # Apply filters
        if search_query:
            q_lower = search_query.lower()
            filtered_pengajuan = [
                p for p in filtered_pengajuan
                if q_lower in getattr(p, 'id_pengajuan', '').lower() or
                   q_lower in getattr(p, 'kebutuhan_role', '').lower() or
                   q_lower in getattr(p, 'perusahaan', '').lower() or
                   q_lower in p.user_nama.lower()
            ]

        if status_filter:
            status_map = {
                'menunggu': ['menunggu', 'pending'],
                'disetujui': ['disetujui', 'approved'],
                'ditolak': ['ditolak', 'rejected']
            }
            allowed_statuses = status_map.get(status_filter.lower(), [status_filter.lower()])
            filtered_pengajuan = [
                p for p in filtered_pengajuan
                if getattr(p, 'status', '').lower() in allowed_statuses
            ]

        import datetime
        if start_date_filter:
            try:
                sd = datetime.datetime.strptime(start_date_filter, '%Y-%m-%d').date()
                filtered_pengajuan = [
                    p for p in filtered_pengajuan
                    if p.tanggal_pengajuan and (
                        p.tanggal_pengajuan.date() if isinstance(p.tanggal_pengajuan, datetime.datetime) else p.tanggal_pengajuan
                    ) >= sd
                ]
            except ValueError:
                pass

        if end_date_filter:
            try:
                ed = datetime.datetime.strptime(end_date_filter, '%Y-%m-%d').date()
                filtered_pengajuan = [
                    p for p in filtered_pengajuan
                    if p.tanggal_pengajuan and (
                        p.tanggal_pengajuan.date() if isinstance(p.tanggal_pengajuan, datetime.datetime) else p.tanggal_pengajuan
                    ) <= ed
                ]
            except ValueError:
                pass

        if bulan_filter:
            filtered_pengajuan = [
                p for p in filtered_pengajuan
                if p.bulan and str(p.bulan).startswith(bulan_filter)
            ]

        # Pagination
        try:
            per_page = int(request.GET.get('per_page', 10))
            if per_page not in [10, 15, 25]:
                per_page = 10
        except ValueError:
            per_page = 10

        from django.core.paginator import Paginator
        paginator = Paginator(filtered_pengajuan, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'list_pengajuan': page_obj,
            'total_pengajuan': len(semua_pengajuan),
            'total_menunggu': total_menunggu,
            'total_disetujui': total_disetujui,
            'total_ditolak': total_ditolak,
            'total_belum_disetujui': total_belum_disetujui,
            'total_sedang_berlangsung': total_sedang_berlangsung,
            'total_riwayat_selesai': total_riwayat_selesai,
            'search_query': search_query,
            'status_filter': status_filter,
            'start_date_filter': start_date_filter,
            'end_date_filter': end_date_filter,
            'bulan_filter': bulan_filter,
            'per_page': per_page,
            'active_tab': active_tab,
        }
    except Exception as e:
        messages.error(request, f'Gagal memuat data pengajuan: {str(e)}')
        context = {
            'list_pengajuan': [],
            'total_pengajuan': 0,
            'total_belum_disetujui': 0,
            'total_sedang_berlangsung': 0,
            'total_riwayat_selesai': 0,
            'search_query': search_query,
            'status_filter': status_filter,
            'active_tab': active_tab,
        }

    return render(request, 'hc/inventori/pengajuanlaptop_hc.html', context)


# @login_required
def tambah_laptop_page(request):
    """
    Halaman form tambah laptop baru.
    GET: Tampilkan form dengan dropdown Processor, RAM, Storage dari DB.
    POST: Proses simpan ke database via Service.
    """
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

            raw_baterai = request.POST.get('baterai')
            baterai_val = None
            if raw_baterai:
                match = re.search(r'\d+(?:\.\d+)?', str(raw_baterai))
                if match:
                    try:
                        baterai_val = float(match.group(0))
                    except ValueError:
                        pass

            if not all([request.POST.get('nama_laptop'), request.POST.get('model'), request.POST.get('os'), request.POST.get('lokasi'), request.POST.get('id_processor'), request.POST.get('id_ram'), request.POST.get('id_storage'), layar_val, baterai_val]):
                messages.error(request, 'Gagal menambahkan laptop: Semua kolom wajib diisi!')
                return render(request, 'hc/inventori/tambahlaptop_hc.html', {'processors': processors, 'rams': rams, 'storages': storages})

            raw_kondisi = str(request.POST.get('kondisi', 'baik')).lower()
            clean_kondisi = 'rusak' if 'rusak' in raw_kondisi else 'baik'
            clean_status = request.POST.get('status', 'tersedia')
            if clean_kondisi == 'rusak':
                clean_status = 'rusak'

            dto = LaptopInventoriDTO(
                nama_laptop=request.POST.get('nama_laptop'),
                model=request.POST.get('model'),
                os=request.POST.get('os'),
                kondisi=clean_kondisi,
                status=clean_status,
                lokasi=request.POST.get('lokasi'),
                id_processor=request.POST.get('id_processor') or None,
                id_ram=request.POST.get('id_ram') or None,
                id_storage=request.POST.get('id_storage') or None,
                ukuran_layar=layar_val,
                baterai=baterai_val,
            )
            service = CreateLaptopInventoriService()
            service.execute(dto)
            messages.success(request, 'Laptop berhasil ditambahkan ke inventori!')
            return redirect('manajemen_laptop_hc')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan laptop: {str(e)}')

    context = {
        'processors': processors,
        'rams': rams,
        'storages': storages,
    }
    return render(request, 'hc/inventori/tambahlaptop_hc.html', context)


# @login_required
def detail_laptop_page(request, id_laptop):
    """
    Halaman detail laptop berdasarkan ID.
    GET: Tampilkan detail lengkap laptop beserta spesifikasi.
    POST (update): Update data laptop (kondisi / status).
    DELETE via POST action: Hapus laptop.
    """
    try:
        laptop = LaptopInventori.objects.select_related(
            'id_processor', 'id_ram', 'id_storage'
        ).get(id_laptop_inventori=id_laptop)
    except LaptopInventori.DoesNotExist:
        messages.error(request, 'Laptop tidak ditemukan.')
        return redirect('inventori:manajemen_laptop')

    processors = Processor.objects.all()
    rams = RAM.objects.all()
    storages = Storage.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'hapus':
            try:
                if laptop.status.lower() == 'dipinjam':
                    raise ValueError("Laptop sedang dipinjam oleh talent dan tidak dapat dihapus.")
                service = DeleteLaptopInventoriService()
                service.execute(id_laptop)
                messages.success(request, f'Laptop {laptop.nama_laptop} berhasil dihapus.')
                return redirect('manajemen_laptop_hc')
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
                return redirect('detaillaptop_hc', id_laptop=id_laptop)
            except Exception as e:
                messages.error(request, f'Gagal update: {str(e)}')

    from inventori.models import Peminjaman
    riwayat_peminjaman = Peminjaman.objects.filter(
        id_laptop_inventori_id=id_laptop
    ).select_related('id_user', 'id_pengajuan').order_by('-tanggal_pinjam')
    
    for p in riwayat_peminjaman:
        p.user_nama = p.id_user.nama if p.id_user else '-'
        p.user_role = p.id_user.role if p.id_user else '-'

    peminjam_aktif = Peminjaman.objects.filter(
        id_laptop_inventori_id=id_laptop,
        status__in=['dipinjam', 'aktif']
    ).select_related('id_user').first()

    context = {
        'laptop': laptop,
        'processors': processors,
        'rams': rams,
        'storages': storages,
        'riwayat_peminjaman': riwayat_peminjaman,
        'peminjam_aktif': peminjam_aktif,
    }
    return render(request, 'hc/inventori/detaillaptop_hc.html', context)

# @login_required
def detailpengajuan_hc_view(request):
    id_pengajuan = request.GET.get('id')
    if not id_pengajuan:
        messages.error(request, 'ID Pengajuan tidak diberikan.')
        return redirect('pengajuanlaptop_hc')

    try:
        service = PengajuanService()
        pengajuan = service.service_cari_pengajuan_by_id(id_pengajuan)
        
        if not pengajuan:
            messages.error(request, 'Data pengajuan tidak ditemukan.')
            return redirect('pengajuanlaptop_hc')

        from inventori.models import User, Proyek, Role
        user_obj = User.objects.filter(id_user=pengajuan.id_user).first()
        pengajuan.user_nama = user_obj.nama if user_obj else pengajuan.id_user

        proyek_obj = Proyek.objects.filter(id_proyek=pengajuan.id_proyek).first()
        pengajuan.proyek_nama = proyek_obj.nama_proyek if proyek_obj else "-"

        role_obj = Role.objects.filter(nama_role__iexact=pengajuan.kebutuhan_role).first()
        id_role = role_obj.id_role if role_obj else ""

        from inventori.models import Peminjaman
        pm_obj = Peminjaman.objects.filter(id_pengajuan=id_pengajuan).select_related('id_laptop_inventori').first()
        pengajuan.laptop_dipakai = pm_obj.id_laptop_inventori if pm_obj else None

        if request.method == 'POST':
            action = request.POST.get('action')
            if action in ['disetujui', 'ditolak']:
                from inventori.dto.dto_pengajuan import PengajuanDTO
                id_user = request.user.id_user if hasattr(request.user, 'id_user') else None
                db_status = 'approved' if action == 'disetujui' else 'rejected'
                
                dto = PengajuanDTO(
                    id_pengajuan=id_pengajuan,
                    status=db_status,
                    approved_by=id_user
                )
                service.service_approve_pengajuan(dto)

                if action == 'ditolak':
                    alasan = request.POST.get('alasan_penolakan') or 'Tidak memenuhi syarat'
                    from inventori.models import Pengajuan as PengajuanModel
                    p_obj = PengajuanModel.objects.filter(id_pengajuan=id_pengajuan).first()
                    if p_obj:
                        p_obj.keterangan = f"Ditolak: {alasan}"
                        p_obj.save()

                messages.success(request, f'Pengajuan berhasil di-{action}.')
                return redirect('pengajuanlaptop_hc')

        context = {
            'pengajuan': pengajuan,
            'id_role': id_role,
            'id_proyek': pengajuan.id_proyek or ""
        }
        return render(request, 'hc/inventori/detailpengajuan_hc.html', context)
        
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
        return redirect('pengajuanlaptop_hc')


# @login_required
def setujui_pengajuan_hc_view(request):
    from inventori.models import LaptopInventori
    from inventori.services.service_pengajuan import PengajuanService
    from inventori.repositories.dto.dto_pengajuan import PengajuanDTO
    from inventori.repositories.dto.dto_peminjaman import PeminjamanDTO
    import datetime

    pengajuan_id = request.GET.get('id')
    if not pengajuan_id:
        messages.error(request, 'ID Pengajuan tidak diberikan.')
        return redirect('pengajuanlaptop_hc')

    if request.method == 'POST':
        laptop_id = request.POST.get('laptop_id')
        if not laptop_id:
            messages.error(request, 'Laptop harus dipilih.')
            return redirect(f"{request.path}?id={pengajuan_id}")
        
        try:
            service = PengajuanService()
            pengajuan = service.service_cari_pengajuan_by_id(pengajuan_id)
            if not pengajuan:
                messages.error(request, 'Pengajuan tidak ditemukan.')
                return redirect('pengajuanlaptop_hc')

            # Buat DTO Pengajuan
            id_user = request.user.id_user if (hasattr(request.user, 'id_user') and request.user.id_user) else 'USR-001'
            dto_peng = PengajuanDTO(
                id_pengajuan=pengajuan_id,
                status='approved',
                approved_by=id_user
            )

            # Ambil tanggal jatuh tempo dari form (TC-TRX-17)
            tanggal_jatuh_tempo_str = request.POST.get('tanggal_jatuh_tempo')
            tanggal_jatuh_tempo = None
            if tanggal_jatuh_tempo_str:
                try:
                    tanggal_jatuh_tempo = datetime.datetime.strptime(tanggal_jatuh_tempo_str, '%Y-%m-%d').date()
                except ValueError:
                    pass

            # Buat DTO Peminjaman
            import time
            id_peminjaman = f"PMJ-{int(time.time())}"
            dto_pem = PeminjamanDTO(
                id_peminjaman=id_peminjaman,
                id_pengajuan=pengajuan_id,
                id_user=pengajuan.id_user,
                id_laptop_inventori=laptop_id,
                tanggal_pinjam=datetime.date.today().strftime('%Y-%m-%d'),
                status='dipinjam',
                keterangan='Persetujuan pengajuan laptop'
            )

            # Eksekusi
            service.service_approve_dan_pinjam(dto_peng, dto_pem)

            # Update Peminjaman status to 'ready' dan set jatuh tempo
            from inventori.models import Peminjaman
            peminjaman = Peminjaman.objects.filter(id_pengajuan=pengajuan_id).first()
            if peminjaman:
                peminjaman.status = 'ready'
                if tanggal_jatuh_tempo:
                    peminjaman.tanggal_jatuh_tempo = tanggal_jatuh_tempo
                peminjaman.save()

            messages.success(request, 'Pengajuan berhasil disetujui dan laptop siap diambil oleh Talent.')
            return redirect('pengajuanlaptop_hc')
        except Exception as e:
            messages.error(request, f'Gagal menyetujui pengajuan: {str(e)}')
            return redirect(f"{request.path}?id={pengajuan_id}")

    # GET request
    from inventori.models import Peminjaman
    # Exclude laptops that have an active loan (assigned)
    active_laptop_ids = Peminjaman.objects.filter(status__in=['dipinjam', 'aktif', 'dikembalikan']).values_list('id_laptop_inventori', flat=True)
    laptops = LaptopInventori.objects.filter(status__in=['tersedia', 'Available', 'Tersedia']).exclude(id_laptop_inventori__in=active_laptop_ids).select_related('id_processor', 'id_ram', 'id_storage')
    
    # Map attributes for the template
    for laptop in laptops:
        laptop.id = laptop.id_laptop_inventori
        
        if laptop.id_processor:
            laptop.processor = laptop.id_processor.nama_processor
        else:
            laptop.processor = "-"
            
        if laptop.id_ram:
            laptop.ram = f"{laptop.id_ram.kapasitas_gb} GB {laptop.id_ram.tipe}"
        else:
            laptop.ram = "-"
            
        if laptop.id_storage:
            laptop.storage = f"{laptop.id_storage.kapasitas_gb} GB {laptop.id_storage.tipe}"
        else:
            laptop.storage = "-"
            
        if laptop.ukuran_layar:
            laptop.screen_size = f"{laptop.ukuran_layar} inch"
        else:
            laptop.screen_size = "-"
            
        from dss.models import LaptopPengadaan
        pengadaan = LaptopPengadaan.objects.filter(nama_laptop__icontains=laptop.nama_laptop).first()
        if pengadaan:
            laptop.battery_capacity = f"{int(pengadaan.baterai)} mAh" if pengadaan.baterai else "5000 mAh"
            laptop.weight = f"{pengadaan.berat} kg" if pengadaan.berat else "1.5 kg"
        else:
            laptop.battery_capacity = "5000 mAh"
            laptop.weight = "1.5 kg"

    context = {
        'pengajuan_id': pengajuan_id,
        'laptops': laptops
    }
    return render(request, 'hc/inventori/setujuipengajuan_hc.html', context)

def riwayatpeminjamanlaptop_hc_view(request, id_laptop=None):
    from inventori.services.service_peminjaman import PeminjamanService
    from inventori.models import User, LaptopInventori
    
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    start_date_filter = request.GET.get('start_date', '').strip()
    end_date_filter = request.GET.get('end_date', '').strip()
    periode_filter = request.GET.get('periode', '').strip()
    laptop_id = id_laptop or request.GET.get('laptop_id', '').strip()

    try:
        service = PeminjamanService()
        list_peminjaman = service.service_ambil_semua_peminjaman()
        
        users_dict = {u.id_user: u.nama for u in User.objects.all()}
        users_role_dict = {u.id_user: u.role for u in User.objects.all()}
        laptops_dict = {l.id_laptop_inventori: l.nama_laptop for l in LaptopInventori.objects.all()}
        laptops_kondisi_dict = {l.id_laptop_inventori: l.kondisi for l in LaptopInventori.objects.all()}
        
        from inventori.models import Peminjaman as PeminjamanModel
        import datetime as _dt
        today_hc = _dt.date.today()
        
        # Build a quick lookup by id_peminjaman for full DB records (for tanggal_jatuh_tempo)
        db_peminjaman_map = {
            pm.id_peminjaman: pm for pm in PeminjamanModel.objects.all()
        }
        
        # Fetch rejected pengajuan and merge into list_peminjaman
        from inventori.models import Pengajuan
        rejected_pengajuan = Pengajuan.objects.filter(status__in=['ditolak', 'rejected'])
        
        class MockPeminjaman:
            def __init__(self, p_obj, users_dict, users_role_dict):
                self.id_peminjaman = p_obj.id_pengajuan
                self.id_pengajuan = p_obj
                self.id_user = p_obj.id_user_id
                self.id_laptop_inventori = "-"
                self.tanggal_pinjam = p_obj.tanggal_pengajuan.date() if p_obj.tanggal_pengajuan else None
                self.tanggal_kembali = None
                self.status = "ditolak"
                self.keterangan = p_obj.keterangan
                
                self.user_nama = users_dict.get(p_obj.id_user_id, str(p_obj.id_user))
                self.user_role = users_role_dict.get(p_obj.id_user_id, "-")
                self.laptop_nama = "Pengajuan Ditolak"
                self.no_inventori = "-"
                self.laptop_kondisi = "-"
                self.durasi_hari = None
                self.tanggal_jatuh_tempo = None
                self.sisa_hari = None
                self.kebutuhan_role = p_obj.kebutuhan_role
                self.kebutuhan_requirement = p_obj.kebutuhan_requirement
                self.perusahaan = p_obj.perusahaan

        for rp in rejected_pengajuan:
            list_peminjaman.append(MockPeminjaman(rp, users_dict, users_role_dict))
        
        for p in list_peminjaman:
            if not hasattr(p, 'user_nama'):
                p.user_nama = users_dict.get(p.id_user, p.id_user)
            if not hasattr(p, 'user_role'):
                p.user_role = users_role_dict.get(p.id_user, "-")
            if not hasattr(p, 'laptop_nama'):
                p.laptop_nama = laptops_dict.get(p.id_laptop_inventori, p.id_laptop_inventori)
            if not hasattr(p, 'laptop_kondisi'):
                p.laptop_kondisi = laptops_kondisi_dict.get(p.id_laptop_inventori, "-")
            
            # Fetch details from Pengajuan model if real peminjaman
            if not hasattr(p, 'kebutuhan_role'):
                try:
                    db_p = db_peminjaman_map.get(p.id_peminjaman)
                    if db_p and db_p.id_pengajuan:
                        p.kebutuhan_role = db_p.id_pengajuan.kebutuhan_role
                        p.kebutuhan_requirement = db_p.id_pengajuan.kebutuhan_requirement
                        p.perusahaan = db_p.id_pengajuan.perusahaan
                    else:
                        p.kebutuhan_role = "-"
                        p.kebutuhan_requirement = "-"
                        p.perusahaan = "-"
                except Exception:
                    p.kebutuhan_role = "-"
                    p.kebutuhan_requirement = "-"
                    p.perusahaan = "-"

            # Kalkulasi durasi (TC-TRX-16)
            if not hasattr(p, 'durasi_hari') or p.durasi_hari is None:
                if p.tanggal_pinjam:
                    if p.tanggal_kembali:
                        p.durasi_hari = (p.tanggal_kembali - p.tanggal_pinjam).days
                    else:
                        p.durasi_hari = (today_hc - p.tanggal_pinjam).days
                else:
                    p.durasi_hari = None
            # Ambil jatuh tempo dari DB dan hitung sisa (TC-TRX-17)
            if not hasattr(p, 'tanggal_jatuh_tempo') or p.tanggal_jatuh_tempo is None:
                db_p = db_peminjaman_map.get(p.id_peminjaman)
                p.tanggal_jatuh_tempo = db_p.tanggal_jatuh_tempo if db_p else None
                if p.tanggal_jatuh_tempo:
                    p.sisa_hari = (p.tanggal_jatuh_tempo - today_hc).days
                else:
                    p.sisa_hari = None
            
        total_peminjaman = len(list_peminjaman)
        peminjam_terakhir = "-"
        
        # Sort by tanggal_pinjam desc
        sorted_p = sorted(list_peminjaman, key=lambda x: x.tanggal_pinjam if x.tanggal_pinjam else _dt.date.min, reverse=True)
        if sorted_p:
            peminjam_terakhir = sorted_p[0].user_nama
            
        # Apply filters
        filtered_p = sorted_p
        if laptop_id:
            target_lid = str(laptop_id).strip().lower()
            filtered_p = [p for p in filtered_p if str(getattr(p, 'id_laptop_inventori', '')).strip().lower() == target_lid]
            total_peminjaman = len(filtered_p)
            if filtered_p:
                peminjam_terakhir = filtered_p[0].user_nama
            else:
                peminjam_terakhir = "-"

        if search_query:
            q_lower = search_query.lower()
            filtered_p = [
                p for p in filtered_p
                if q_lower in p.user_nama.lower() or
                   q_lower in p.laptop_nama.lower() or
                   q_lower in getattr(p, 'status', '').lower()
            ]

        if status_filter:
            status_lower = status_filter.lower()
            if status_lower == 'dipinjam':
                allowed = ['dipinjam', 'aktif', 'ready', 'siap_diambil']
            elif status_lower in ['selesai', 'kembali']:
                allowed = ['selesai', 'dikembalikan']
            else:
                allowed = [status_lower]
            filtered_p = [
                p for p in filtered_p
                if getattr(p, 'status', '').lower() in allowed
            ]

        if start_date_filter:
            try:
                sd = _dt.datetime.strptime(start_date_filter, '%Y-%m-%d').date()
                filtered_p = [
                    p for p in filtered_p
                    if p.tanggal_pinjam and p.tanggal_pinjam >= sd
                ]
            except ValueError:
                pass

        if end_date_filter:
            try:
                ed = _dt.datetime.strptime(end_date_filter, '%Y-%m-%d').date()
                filtered_p = [
                    p for p in filtered_p
                    if p.tanggal_pinjam and p.tanggal_pinjam <= ed
                ]
            except ValueError:
                pass

        if periode_filter and periode_filter.isdigit():
            days_ago = int(periode_filter)
            cutoff_date = today_hc - _dt.timedelta(days=days_ago)
            filtered_p = [
                p for p in filtered_p
                if p.tanggal_pinjam and p.tanggal_pinjam >= cutoff_date
            ]

        # Pagination
        try:
            per_page = int(request.GET.get('per_page', 10))
            if per_page not in [10, 15, 25]:
                per_page = 10
        except ValueError:
            per_page = 10

        from django.core.paginator import Paginator
        paginator = Paginator(filtered_p, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'list_peminjaman': page_obj,
            'total_peminjaman': total_peminjaman,
            'peminjam_terakhir': peminjam_terakhir,
            'search_query': search_query,
            'status_filter': status_filter,
            'start_date_filter': start_date_filter,
            'end_date_filter': end_date_filter,
            'periode_filter': periode_filter,
            'laptop_id': laptop_id,
            'per_page': per_page,
        }
        return render(request, 'hc/inventori/riwayatpeminjamanlaptop_hc.html', context)
    except Exception as e:
        import traceback; traceback.print_exc()
        messages.error(request, f'Gagal memuat riwayat: {str(e)}')
        return redirect('manajemen_laptop_hc')

# @login_required
def editdatalaptop_hc_view(request, id_laptop):
    try:
        laptop = LaptopInventori.objects.get(id_laptop_inventori=id_laptop)
    except LaptopInventori.DoesNotExist:
        messages.error(request, 'Laptop tidak ditemukan.')
        return redirect('manajemen_laptop_hc')

    if request.method == 'POST':
        try:
            update_service = UpdateLaptopInventoriService()
            kondisi = request.POST.get('kondisi')
            status = request.POST.get('status')
            lokasi = request.POST.get('lokasi')
            baterai = request.POST.get('baterai')
            ukuran_layar = request.POST.get('ukuran_layar')


            if laptop.status.lower() == 'dipinjam' and status and status.lower() != 'dipinjam':
                raise ValueError("Laptop sedang aktif dipinjam dan tidak dapat diubah statusnya.")

            if kondisi:
                kondisi_clean = 'rusak' if 'rusak' in str(kondisi).lower() else 'baik'
                update_service.update_kondisi(id_laptop, kondisi_clean)
                if kondisi_clean == 'rusak':
                    status = 'rusak'
                    update_service.update_status(id_laptop, 'rusak', lokasi)
            if status and kondisi != 'rusak':
                update_service.update_status(id_laptop, status, lokasi)

            # Update spesifikasi
            id_processor = request.POST.get('id_processor')
            id_ram = request.POST.get('id_ram')
            id_storage = request.POST.get('id_storage')

            if baterai:
                laptop.baterai = baterai
                laptop.save()

            if ukuran_layar:
                laptop.ukuran_layar = ukuran_layar
                laptop.save()
            
            if id_processor and id_ram and id_storage:
                dto = LaptopInventoriDTO(
                    nama_laptop=laptop.nama_laptop,
                    model=laptop.model,
                    os=laptop.os,   
                    kondisi='rusak' if kondisi and 'rusak' in str(kondisi).lower() else (laptop.kondisi if not kondisi else 'baik'),
                    status=status or laptop.status,
                    lokasi=lokasi or laptop.lokasi,
                    id_processor=id_processor,
                    id_ram=id_ram,
                    id_storage=id_storage,
                    id_laptop_inventori=id_laptop,
                    baterai=baterai,
                    ukuran_layar=ukuran_layar
                )
                update_service.update_spek(dto)

            messages.success(request, 'Data laptop berhasil diperbarui.')
            return redirect('detaillaptop_hc', id_laptop=id_laptop)
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
    return render(request, 'hc/inventori/editdatalaptop_hc.html', context)


# =============================================================================
#   1. PROCESSOR CRUD API (JSON)
# =============================================================================

@csrf_exempt
@require_http_methods(["GET", "POST"])
def processor_list_create(request):
    try:
        if request.method == "GET":
            service = ReadProcessorService()
            data = service.ambil_semua()
            data_list = [dict(row) for row in data] if data else []
            return success_response(data_list)

        elif request.method == "POST":
            service = CreateProcessorService()
            body = _parse_body(request)
            dto = ProcessorDTO(
                nama_processor=body.get("nama_processor"),
                manufacturer=body.get("manufacturer"),
                model=body.get("model"),
                cores=body.get("cores"),
                threads=body.get("threads"),
                base_clock=body.get("base_clock"),
                max_clock=body.get("max_clock"),
                arsitektur=body.get("arsitektur"),
                keterangan=body.get("keterangan")
            )
            res = service.execute(dto)
            return success_response(None, res, 201)
    except Exception as e:
        return error_response(str(e), 500)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def processor_detail(request, id_processor):
    try:
        if request.method == "GET":
            service = ReadProcessorService()
            data = service.ambil_by_id(id_processor)
            if not data:
                return error_response("Processor tidak ditemukan", 404)
            return success_response(dict(data))

        elif request.method == "PUT":
            service = UpdateProcessorService()
            body = _parse_body(request)
            dto = ProcessorDTO(
                id_processor=id_processor,
                nama_processor=body.get("nama_processor"),
                manufacturer=body.get("manufacturer"),
                model=body.get("model"),
                cores=body.get("cores"),
                threads=body.get("threads"),
                base_clock=body.get("base_clock"),
                max_clock=body.get("max_clock"),
                arsitektur=body.get("arsitektur"),
                keterangan=body.get("keterangan")
            )
            res = service.execute(dto)
            return success_response(None, res)

        elif request.method == "DELETE":
            service = DeleteProcessorService()
            res = service.execute(id_processor)
            return success_response(None, res)
    except Exception as e:
        return error_response(str(e), 500)


# =============================================================================
#   2. LAPTOP INVENTORI CRUD API (JSON)
# =============================================================================

@csrf_exempt
@require_http_methods(["GET", "POST"])
def laptop_list_create(request):
    try:
        if request.method == "GET":
            service = ReadLaptopInventoriService()
            data = service.ambil_semua()
            data_list = [dict(row) for row in data] if data else []
            return success_response(data_list)

        elif request.method == "POST":
            service = CreateLaptopInventoriService()
            body = _parse_body(request)
            dto = LaptopInventoriDTO(
                nama_laptop=body.get("nama_laptop"),
                model=body.get("model"),
                os=body.get("os"),
                kondisi=body.get("kondisi", "baik"),
                status=body.get("status", "tersedia"),
                lokasi=body.get("lokasi"),
                id_processor=body.get("id_processor"),
                id_ram=body.get("id_ram"),
                id_storage=body.get("id_storage"),
                ukuran_layar=body.get("ukuran_layar")
            )
            res = service.execute(dto)
            return success_response(None, res, 201)
    except Exception as e:
        return error_response(str(e), 500)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def laptop_detail(request, id_laptop):
    try:
        if request.method == "GET":
            service = ReadLaptopInventoriService()
            data = service.ambil_spek_by_id(id_laptop)
            if not data:
                return error_response("Laptop tidak ditemukan", 404)
            return success_response(dict(data))

        elif request.method == "PUT":
            service = UpdateLaptopInventoriService()
            body = _parse_body(request)
            if "kondisi" in body:
                service.update_kondisi(id_laptop, body["kondisi"])
            if "status" in body:
                service.update_status(id_laptop, body["status"], body.get("lokasi"))
            return success_response(None, "Laptop berhasil diupdate")

        elif request.method == "DELETE":
            service = DeleteLaptopInventoriService()
            res = service.execute(id_laptop)
            return success_response(None, res)
    except Exception as e:
        return error_response(str(e), 500)


# =============================================================================
#   3. Pengajuan Views
# =============================================================================

@csrf_exempt
def tambah_pengajuan_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            dto = PengajuanDTO(
                id_user=body.get("id_user"),
                kebutuhan_role=body.get("kebutuhan_role"),
                kebutuhan_requirement=body.get("kebutuhan_requirement"),
                bulan=body.get("bulan"),
                keterangan=body.get("keterangan"),
                perusahaan=body.get("perusahaan"),
                id_proyek=body.get("id_proyek")
            )
            service = PengajuanService()
            result = service.service_tambah_pengajuan(dto)
            return JsonResponse({"message": result})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def list_pengajuan_view(request):
    if request.method == "GET":
        try:
            service = PengajuanService()
            data = service.service_ambil_semua_pengajuan()
            return JsonResponse({"data": [d.__dict__ for d in data]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


# =============================================================================
#   4. Peminjaman Views
# =============================================================================

@csrf_exempt
def tambah_peminjaman_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            dto = PeminjamanDTO(
                id_user=body.get("id_user"),
                id_laptop_inventori=body.get("id_laptop_inventori"),
                tanggal_pinjam=body.get("tanggal_pinjam"),
                tanggal_kembali=body.get("tanggal_kembali"),
                status=body.get("status"),
                keterangan=body.get("keterangan")
            )
            service = PeminjamanService()
            result = service.tambah_peminjaman(dto)
            return JsonResponse({"message": result})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def list_peminjaman_view(request):
    if request.method == "GET":
        try:
            service = PeminjamanService()
            data = service.ambil_semua_peminjaman()
            return JsonResponse({"data": [d.__dict__ for d in data]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)

def detail_peminjaman_view(request, id_peminjaman):
    if request.method == "GET":
        try:
            service = PeminjamanService()
            data = service.cari_peminjaman(id_peminjaman)

            if not data:
                return JsonResponse({"error": "Data tidak ditemukan"}, status=404)

            return JsonResponse(data.__dict__)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def update_peminjaman_view(request):
    if request.method == "PUT":
        try:
            body = json.loads(request.body)
            
            dto = PeminjamanDTO(
                id_peminjaman=body.get("id_peminjaman"),
                tanggal_pinjam=body.get("tanggal_pinjam"),
                tanggal_kembali=body.get("tanggal_kembali"),
                status=body.get("status"),
                keterangan=body.get("keterangan")
            )
            
            service = PeminjamanService()
            result = service.update_pengajuan(dto)
            
            return JsonResponse({"message": result})
        except Exception as e:  
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def hapus_peminjaman_view(request, id_peminjaman):
    if request.method == "DELETE":
        try:
            service = PeminjamanService()
            result = service.hapus_peminjaman(id_peminjaman)
            
            return JsonResponse({"message": result})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def pinjam_laptop_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            dto = PeminjamanDTO(
                id_user=body.get("id_user"),
                id_laptop_inventori=body.get("id_laptop_inventori"),
                id_pengajuan=body.get("id_pengajuan"),
                tanggal_pinjam=body.get("tanggal_pinjam"),
                tanggal_kembali=body.get("tanggal_kembali"),
                keterangan=body.get("keterangan")
            )

            service = PeminjamanService()
            result = service.pinjam_laptop(dto)

            return JsonResponse({"message": result})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def pengembalian_laptop_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            dto = PeminjamanDTO(
                id_peminjaman=body.get("id_peminjaman"),
                lokasi=body.get("lokasi"),
                keterangan=body.get("keterangan")
            )

            service = PeminjamanService()
            result = service.pengembalian_laptop(dto)

            return JsonResponse({"message": result})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def sync_status_laptop_view(request):
    if request.method == "POST":
        try:
            service = PeminjamanService()
            result = service.sync_status_laptop()

            return JsonResponse({"message": result})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
def laptop_by_lokasi_view(request):
    if request.method == "GET":
        try:
            service = PeminjamanService()
            data = service.ambil_laptop_by_lokasi()

            return JsonResponse({"data": data})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
def laptop_dashboard(request):
    service = ReadLaptopInventoriService()
    data = service.ambil_semua()

    data_list = [dict(row) for row in data] if data else []

    # NORMALISASI DATA (anti error)
    for row in data_list:
        row["status"] = (row.get("status") or "").lower()
        row["nama_laptop"] = row.get("nama_laptop") or "-"
        row["model"] = row.get("model") or "-"
        row["no_inventori"] = row.get("no_inventori") or "-"

    return render(request, "hc/dashboard/laptop_dashboard.html", {
        "laptops": data_list
    })

def tambahlaptop_hc_view(request):
    service_storage = StorageService()
    service_ram = RamService()
    service_processor = ReadProcessorService()

    data_storage = service_storage.service_ambil_storage()
    data_ram = service_ram.service_ambil_ram()
    data_processor = service_processor.ambil_processor()

    for row in data_processor:
        row["display"] = f"{row.get('nama_processor','-')}"

    for row in data_ram:
        row["display"] = f"{row.get('kapasitas_gb','-')} GB {row.get('tipe','-')}"

    for row in data_storage:
        row["display"] = f"{row.get('kapasitas_gb','-')} GB {row.get('tipe','-')}"

    return render(request, "inventori/tambahlaptop_hc.html", {
        "processor": data_processor,
        "ram": data_ram,
        "storage": data_storage
    })

def assign_laptop_hc_view(request):
    from inventori.models import Pengajuan, LaptopInventori, Peminjaman, User as InvUser
    from inventori.services.service_pengajuan import PengajuanService
    from inventori.dto.dto_pengajuan import PengajuanDTO
    from inventori.dto.dto_peminjaman import PeminjamanDTO
    import datetime, time

    laptop_id = request.GET.get('laptop_id') or request.POST.get('laptop_id') or request.GET.get('id_laptop')
    pengajuan_id = request.GET.get('id_pengajuan') or request.POST.get('id_pengajuan') or request.session.get('id_pengajuan')

    if not laptop_id:
        messages.error(request, 'Laptop belum dipilih.')
        return redirect('hasilrekomendasi_hc')

    if not pengajuan_id:
        messages.error(request, 'Silakan pilih pengajuan / user terlebih dahulu.')
        return redirect('hasilrekomendasi_hc')

    try:
        service = PengajuanService()
        pengajuan = service.service_cari_pengajuan_by_id(pengajuan_id)
        if not pengajuan:
            messages.error(request, 'Data pengajuan tidak ditemukan.')
            return redirect('hasilrekomendasi_hc')

        id_user_hc = request.user.id_user if (hasattr(request.user, 'id_user') and request.user.id_user) else 'USR-001'
        dto_peng = PengajuanDTO(
            id_pengajuan=pengajuan_id,
            status='approved',
            approved_by=id_user_hc
        )

        id_peminjaman = f"PMJ-{int(time.time())}"
        dto_pem = PeminjamanDTO(
            id_peminjaman=id_peminjaman,
            id_pengajuan=pengajuan_id,
            id_user=pengajuan.id_user,
            id_laptop_inventori=laptop_id,
            tanggal_pinjam=datetime.date.today().strftime('%Y-%m-%d'),
            status='dipinjam',
            keterangan='Assign laptop dari hasil rekomendasi DSS'
        )

        service.service_approve_dan_pinjam(dto_peng, dto_pem)

        peminjaman = Peminjaman.objects.filter(id_pengajuan=pengajuan_id).first()
        if peminjaman:
            peminjaman.status = 'ready'
            peminjaman.save()

        user_obj = InvUser.objects.filter(id_user=pengajuan.id_user).first()
        user_nama = user_obj.nama if user_obj else pengajuan.id_user

        messages.success(request, f'Laptop {laptop_id} berhasil di-assign ke {user_nama} (Pengajuan {pengajuan_id})!')
        if 'id_pengajuan' in request.session:
            del request.session['id_pengajuan']
        return redirect('pengajuanlaptop_hc')

    except Exception as e:
        messages.error(request, f'Gagal melakukan assign laptop: {str(e)}')
        return redirect('hasilrekomendasi_hc')

