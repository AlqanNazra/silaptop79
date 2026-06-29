import datetime
import json
import traceback
from urllib import request
import uuid

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import connection, transaction

from dss.models import BobotKriteria
from dss.repositories.dto.dto_bobot_kriteria import BobotKriteriaDTO
from dss.repositories.dto.dto_laptop_pengadaan import FilterPengadaanDTO
from dss.repositories.repositori_bobot_kriteria import BobotKriteriaRepository
from dss.repositories.repositori_bobot_kriteria import BobotKriteriaRepository
from dss.repositories.repositori_laptop_pengadaan import LaptopPengadaanRepository
from dss.services.service_agregiasi import AggregationService
from dss.services.service_bobotkriteria import ServiceBobotKriteria
from dss.services.service_swara import ServiceSwara
from inventori.dto.dto_projectrole import ProjectRoleDTO
from inventori.dto.dto_proyek import ProyekDTO
from inventori.dto.dto_role import RoleDTO
from inventori.dto.dto_role_teknologi import RoleTeknologiDTO
from inventori.dto.dto_teknologi import TeknologiDTO
from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository
from inventori.repositories.repositori_projectrole import ProjectRoleRepository
from inventori.repositories.repositori_proyek import ProyekRepository
from inventori.repositories.repositori_teknologi import TeknologiRepository
from inventori.services.service_projectrole import ProjectRoleService
from inventori.services.service_proyek import ProyekService
from inventori.services.service_teknologi import TeknologiService
from .db import get_connection
from inventori.repositories.repositori_projectrole import ProjectRoleRepository
from inventori.services.service_projectrole import ProjectRoleService
from inventori.dto.dto_projectrole import ProjectRoleDTO
from django.http import JsonResponse
from inventori.services.processor.read import ReadProcessorService

# ==========================================
# 1. HUMAN CAPITAL (HC) VIEWS
# ==========================================

from inventori.models import LaptopInventori, Processor, RAM, Role, Storage, Teknologi, TeknologiRole, User
from inventori.services.service_pengajuan import PengajuanService
from inventori.services.service_peminjaman import PeminjamanService
from inventori.dto.dto_laptop_inventori import FilterInventoriDTO, LaptopInventoriDTO
from inventori.services.laptop_inventori.create import CreateLaptopInventoriService
from inventori.services.laptop_inventori.update import UpdateLaptopInventoriService
from inventori.services.laptop_inventori.delete import DeleteLaptopInventoriService
from django.contrib import messages
from django.db import connection
from inventori.dto.dto_pengajuan import PengajuanDTO
from inventori.dto.dto_peminjaman import PeminjamanDTO
from inventori.models import (
    Proyek,
    RoleTeknologi,
    ProjectRole,
    ProjectTechnology
)
from dss.repositories.repositori_kriteria import KriteriaRepository
from silaptop79.db import get_connection
from inventori.repositories.repositori_role_teknologi import RoleTeknologiRepository
from inventori.repositories.repositori_role import RoleRepository
from inventori.services.service_role_teknologi import RoleTeknologiService
from inventori.services.service_role import RoleService
from django.contrib import messages
from inventori.models import RoleTeknologi
from inventori.repositories.dto.dto_laptop_inventori import FilterInventoriDTO
from dss.services.service_saw import Servicesaw
from django.core.paginator import Paginator



def dashboard_hc_view(request):
    try:
        total_laptop = LaptopInventori.objects.count()
        service = PengajuanService()
        semua_pengajuan = service.service_ambil_semua_pengajuan()
        total_pengajuan = len(semua_pengajuan)
        pengajuan_menunggu = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'menunggu')

        # Ambil data peminjaman
        peminjaman_service = PeminjamanService()
        peminjaman_list = peminjaman_service.service_ambil_semua_peminjaman()
        
        # Mapping nama laptop dan user ke list peminjaman
        from inventori.models import User
        users_dict = {u.id_user: u.nama for u in User.objects.all()}
        laptops_dict = {l.id_laptop_inventori: l.nama_laptop for l in LaptopInventori.objects.all()}
        
        riwayat_pinjam = []
        for p in peminjaman_list:
            # Ambil detail nama user & nama laptop
            nama_user = users_dict.get(p.id_user, f"User {p.id_user}")
            nama_laptop = laptops_dict.get(p.id_laptop_inventori, f"Laptop {p.id_laptop_inventori}")
            riwayat_pinjam.append({
                'nama_laptop': nama_laptop,
                'nama_user': nama_user,
                'tanggal_pinjam': p.tanggal_pinjam,
                'status': p.status or 'aktif'
            })
            
        # Urutkan berdasarkan tanggal pinjam terbaru, batasi 5 saja
        riwayat_pinjam.sort(key=lambda x: x['tanggal_pinjam'] if x['tanggal_pinjam'] else datetime.date.min, reverse=True)
        riwayat_pinjam = riwayat_pinjam[:5]
        
    except Exception as e:
        total_laptop = 0
        total_pengajuan = 0
        pengajuan_menunggu = 0
        riwayat_pinjam = []

    context = {
        'total_laptop': total_laptop,
        'total_pengajuan': total_pengajuan,
        'pengajuan_menunggu': pengajuan_menunggu,
        'riwayat_pinjam': riwayat_pinjam,
    }
    return render(request, 'hc/dashboard/dashboard_hc.html', context)
def manajemenlaptop_hc_view(request):
    return render(request, 'hc/inventori/manajemenlaptop_hc.html')

def manajementalent_hc_view(request):
    import random
    import string
    from inventori.models import User
    from django.db.models import Q
    
    generated_password = None
    created_username = None
    created_email = None

    if request.method == 'POST':
        nama = request.POST.get('username')
        email = request.POST.get('email')
        
        if nama and email:
            # Generate random password 8 chars
            chars = string.ascii_letters + string.digits
            generated_password = ''.join(random.choice(chars) for _ in range(8))
            
            # Generate unique ID USR-xxx
            random_id = f"USR-{random.randint(100, 999)}"
            while User.objects.filter(id_user=random_id).exists():
                random_id = f"USR-{random.randint(100, 999)}"
                
            try:
                # Simpan user baru (role Talent)
                User.objects.create(
                    id_user=random_id,
                    nama=nama,
                    email=email,
                    password=generated_password, # Disimpan plain text dulu sesuai spesifikasi user
                    role='Talent'
                )
                created_username = nama
                created_email = email
                messages.success(request, f'Akun Talent "{nama}" berhasil dibuat!')
            except Exception as e:
                messages.error(request, f'Gagal membuat akun: {str(e)}')
                generated_password = None

    # Get query params
    search_query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort', 'id_user') # Default sort by id_user

    # Base query for talent
    talents_qs = User.objects.filter(role__iexact='talent')
    total_talent = talents_qs.count()

    # Search filter
    if search_query:
        talents_qs = talents_qs.filter(
            Q(nama__icontains=search_query) | 
            Q(email__icontains=search_query) |
            Q(id_user__icontains=search_query)
        )

    # Sort logic
    if sort_by == 'nama':
        talents_qs = talents_qs.order_by('nama')
    elif sort_by == 'email':
        talents_qs = talents_qs.order_by('email')
    else:
        talents_qs = talents_qs.order_by('id_user')

    context = {
        'talents': talents_qs,
        'total_talent': total_talent,
        'search_query': search_query,
        'sort_by': sort_by,
        'generated_password': generated_password,
        'created_username': created_username,
        'created_email': created_email,
    }
    return render(request, 'hc/users/manajementalent_hc.html', context)

def pengajuanlaptop_it_view(request):
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
        import datetime
        users_dict = {u.id_user: u.nama for u in User.objects.all()}
        
        peminjamans = Peminjaman.objects.all()
        peminjaman_map = {}
        for p in peminjamans:
            pengajuan_id = p.id_pengajuan_id
            if pengajuan_id not in peminjaman_map:
                peminjaman_map[pengajuan_id] = []
            peminjaman_map[pengajuan_id].append(p)

        total_siap_proses = 0
        total_dikonfigurasi = 0
        total_selesai = 0
        total_mendesak = 0
        today = datetime.date.today()

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
            is_approved = p.status and p.status.lower() in ['disetujui', 'approved']
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

            # Calculate if urgent (due date <= 7 days)
            if p.status and p.status.lower() in ['menunggu', 'pending']:
                if p.bulan:
                    diff_days = (p.bulan - today).days
                    if diff_days <= 7:
                        total_mendesak += 1

            if not is_approved:
                belum_disetujui_list.append(p)
                p.status_display = 'menunggu'
                total_dikonfigurasi += 1
            else:
                has_ready = (not p_loans) or any(l.status.lower() == 'ready' for l in p_loans)
                if has_ready:
                    # Jika belum diambil oleh talent, hold dulu di belum_disetujui_list dengan status 'belum diambil'
                    belum_disetujui_list.append(p)
                    p.status_display = 'belum diambil'
                    total_siap_proses += 1
                else:
                    has_completed = any(l.status.lower() == 'selesai' for l in p_loans)
                    if has_completed:
                        riwayat_selesai_list.append(p)
                        p.status_display = 'selesai'
                        total_selesai += 1
                    else:
                        sedang_berlangsung_list.append(p)
                        has_returned = any(l.status.lower() == 'dikembalikan' for l in p_loans)
                        if has_returned:
                            p.status_display = 'dikembalikan'
                        else:
                            p.status_display = 'dipinjam'
        
        total_belum_disetujui = len(belum_disetujui_list)
        total_sedang_berlangsung = len(sedang_berlangsung_list)
        total_riwayat_selesai = len(riwayat_selesai_list)
        total_pengajuan = len(semua_pengajuan)

        # Select target list based on active tab
        if active_tab == 'sedang_berlangsung':
            filtered_pengajuan = sedang_berlangsung_list
        elif active_tab == 'riwayat_selesai':
            filtered_pengajuan = riwayat_selesai_list
        else:
            active_tab = 'belum_disetujui'
            filtered_pengajuan = belum_disetujui_list

        # Sort by date descending
        filtered_pengajuan.sort(key=lambda x: x.tanggal_pengajuan if x.tanggal_pengajuan else datetime.date.min, reverse=True)

        # Filter search
        if search_query:
            q_lower = search_query.lower()
            filtered_pengajuan = [
                p for p in filtered_pengajuan
                if q_lower in getattr(p, 'user_nama', '').lower() or
                   q_lower in str(getattr(p, 'id_pengajuan', '')).lower() or
                   q_lower in getattr(p, 'spesifikasi_tambahan', '').lower()
            ]

        # Filter status
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
            'total_pengajuan': total_pengajuan,
            'total_menunggu': total_menunggu,
            'total_disetujui': total_disetujui,
            'total_ditolak': total_ditolak,
            'total_belum_disetujui': total_belum_disetujui,
            'total_sedang_berlangsung': total_sedang_berlangsung,
            'total_riwayat_selesai': total_riwayat_selesai,
            'total_siap_proses': total_siap_proses,
            'total_dikonfigurasi': total_dikonfigurasi,
            'total_selesai': total_selesai,
            'total_mendesak': total_mendesak,
            'search_query': search_query,
            'status_filter': status_filter,
            'start_date_filter': start_date_filter,
            'end_date_filter': end_date_filter,
            'bulan_filter': bulan_filter,
            'per_page': per_page,
        }
    except Exception as e:
        context = {
            'error_message': f'Gagal memuat data pengajuan: {str(e)}',
            'list_pengajuan': [],
            'total_pengajuan': 0,
            'total_belum_disetujui': 0,
            'total_sedang_berlangsung': 0,
            'total_riwayat_selesai': 0,
            'total_siap_proses': 0,
            'total_dikonfigurasi': 0,
            'total_selesai': 0,
            'total_mendesak': 0,
            'search_query': search_query,
            'status_filter': status_filter,
            'active_tab': active_tab,
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

        from inventori.models import Proyek, Role
        proyek_obj = Proyek.objects.filter(id_proyek=pengajuan.id_proyek).first()
        pengajuan.proyek_nama = proyek_obj.nama_proyek if proyek_obj else "-"

        role_obj = Role.objects.filter(nama_role__iexact=pengajuan.kebutuhan_role).first()
        id_role = role_obj.id_role if role_obj else ""

        from inventori.models import Peminjaman
        pm_obj = Peminjaman.objects.filter(id_pengajuan=id_pengajuan).select_related('id_laptop_inventori').first()
        pengajuan.laptop_dipakai = pm_obj.id_laptop_inventori if pm_obj else None

        # IT does not have approve or reject actions.
        if request.method == 'POST':
            # Future actions that IT might need could be placed here.
            pass

        context = {
            'pengajuan': pengajuan,
            'id_role': id_role,
            'id_proyek': pengajuan.id_proyek or ""
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
                return render(request, 'it/inventori/tambahlaptop_it.html', {'processors': processors, 'rams': rams, 'storages': storages})

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
                    kondisi_clean = 'rusak' if 'rusak' in str(kondisi).lower() else 'baik'
                    update_service.update_kondisi(id_laptop, kondisi_clean)
                    if kondisi_clean == 'rusak':
                        update_service.update_status(id_laptop, 'rusak', lokasi)
                elif status:
                    update_service.update_status(id_laptop, status, lokasi)

                messages.success(request, 'Data laptop berhasil diperbarui.')
                return redirect('detaillaptop_it', id_laptop=id_laptop)
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
    return render(request, 'it/inventori/detaillaptop_it.html', context)

def riwayatpeminjamanlaptop_it_view(request, id_laptop=None):
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    laptop_id = id_laptop or request.GET.get('laptop_id', '').strip()

    try:
        service = PeminjamanService()
        riwayat_list = service.service_ambil_semua_peminjaamn()
        
        users_dict = {u.id_user: u.nama for u in User.objects.all()}
        users_role_dict = {u.id_user: u.role for u in User.objects.all()}
        laptops_dict = {l.id_laptop_inventori: l.nama_laptop for l in LaptopInventori.objects.all()}
        
        from inventori.models import Peminjaman as PeminjamanModel
        import datetime as _dt
        today_it = _dt.date.today()
        
        # Build DB lookup for jatuh_tempo
        db_peminjaman_map_it = {
            pm.id_peminjaman: pm for pm in PeminjamanModel.objects.all()
        }
        
        for p in riwayat_list:
            p.user_nama = users_dict.get(p.id_user, p.id_user)
            p.user_role = users_role_dict.get(p.id_user, "-")
            p.laptop_nama = laptops_dict.get(p.id_laptop_inventori, p.id_laptop_inventori)
            # Kalkulasi durasi peminjaman (TC-TRX-16)
            if p.tanggal_pinjam:
                if p.tanggal_kembali:
                    p.durasi_hari = (p.tanggal_kembali - p.tanggal_pinjam).days
                else:
                    p.durasi_hari = (today_it - p.tanggal_pinjam).days
            else:
                p.durasi_hari = 0
            # Sisa hari menuju jatuh tempo (TC-TRX-17) - ambil dari DB
            db_p = db_peminjaman_map_it.get(p.id_peminjaman)
            p.tanggal_jatuh_tempo = db_p.tanggal_jatuh_tempo if db_p else None
            if p.tanggal_jatuh_tempo:
                p.sisa_hari = (p.tanggal_jatuh_tempo - today_it).days
            else:
                p.sisa_hari = None
            
        total_peminjaman = len(riwayat_list)
        peminjam_terakhir = "-"
        
        sorted_p = sorted(riwayat_list, key=lambda x: str(x.tanggal_pinjam) if x.tanggal_pinjam else "", reverse=True)
        if sorted_p:
            peminjam_terakhir = sorted_p[0].user_nama

        # Filter by laptop_id if present
        filtered_p = sorted_p
        if laptop_id:
            target_lid = str(laptop_id).strip().lower()
            filtered_p = [p for p in filtered_p if str(getattr(p, 'id_laptop_inventori', '')).strip().lower() == target_lid]
            total_peminjaman = len(filtered_p)
            if filtered_p:
                peminjam_terakhir = filtered_p[0].user_nama
            else:
                peminjam_terakhir = "-"

        # Filter search
        if search_query:
            q_lower = search_query.lower()
            filtered_p = [
                p for p in filtered_p
                if q_lower in getattr(p, 'user_nama', '').lower() or
                   q_lower in getattr(p, 'laptop_nama', '').lower() or
                   q_lower in str(getattr(p, 'id_peminjaman', '')).lower()
            ]

        # Filter status
        if status_filter:
            status_lower = status_filter.lower()
            filtered_p = [
                p for p in filtered_p
                if getattr(p, 'status', '').lower() == status_lower
            ]

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
            'laptop_id': laptop_id,
            'per_page': per_page,
        }
    except Exception as e:
        messages.error(request, f'Gagal memuat riwayat: {str(e)}')
        context = {
            'list_peminjaman': [],
            'total_peminjaman': 0,
            'peminjam_terakhir': "-",
            'search_query': search_query,
            'status_filter': status_filter,
            'laptop_id': laptop_id,
        }
    return render(request, 'it/inventori/riwayatpeminjamanlaptop_it.html', context)

def editdatalaptop_hc_view(request):
    return render(request, 'hc/inventori/editdatalaptop_hc.html')

def inputkriteria_hc_view(request):
    conn = get_connection()
    selected_project = (request.GET.get("id_proyek")or request.POST.get("id_proyek"))
    selected_role  = (request.GET.get("id_role")or request.POST.get("id_role"))
    id_pengajuan = (request.GET.get("id_pengajuan") or request.POST.get("id_pengajuan") or request.session.get("id_pengajuan"))
    if id_pengajuan:
        request.session["id_pengajuan"] = id_pengajuan
    role_requirement = None
    bobot_role = None
    selected_role_teknologi = (
    request.GET.get("id_role_teknologi")
    or request.POST.get("id_role_teknologi"))
    processor_service = ReadProcessorService()
    processor_list = processor_service.ambil_processor()
    bobot_role = None
    # ==========================
    # LOAD ROLE REQUIREMENT
    # ==========================
    if selected_role:
        try:
            from inventori.models import Role
            role = Role.objects.get(id_role=selected_role)
            # print("=" * 50)
            # print("AMBIL ROLETEK")
            # print("=" * 50)
            role_teknologi_list = (RoleTeknologi.objects.select_related("teknologi").filter(role_id=selected_role))
            # print("JUMLAH ROLETEK =",role_teknologi_list.count())
            role_requirement = {
                "id_role": role.id_role,
                "nama_role": role.nama_role,
                "min_ram": role.min_ram,
                "min_storage": role.min_storage,
                "nama_processor": role.nama_processor,
                "min_processor_score": role.min_processor_score
            }
            repo_bobot = BobotKriteriaRepository(conn)
            aggregation_service = AggregationService(conn)
            hasil_teknologi = []
            for rt in role_teknologi_list:
                # print("=" * 40)
                # print("ROLETEK :",rt.id_role_teknologi)
                # print("TEKNOLOGI :",rt.teknologi.nama_teknologi)
                rows = (repo_bobot.ambil_bobot_role_teknologi(rt.id_role_teknologi))
                # print("JUMLAH BOBOT :",len(rows))
                hasil_teknologi.append(rows)
            if hasil_teknologi:
                bobot_role = (aggregation_service.aggregate_teknologi_role(hasil_teknologi))
            else:
                bobot_role = {}
            # print("BOBOT AGREGASI =",bobot_role)
        except Exception as e:
            print("ERROR ROLE REQUIREMENT:",str(e))
    # ==========================
    # PROSES DSS
    # ==========================
    if request.method == "POST":
        # print("=" * 50)
        # print("POST DSS")
        # print("POST =", request.POST)
        action = request.POST.get("action","load")
        jenis_rekomendasi = request.POST.get("jenis_rekomendasi","inventori")
        min_harga = request.POST.get("min_harga","")
        # print("JENIS =", jenis_rekomendasi)
        # print("MIN HARGA =", min_harga)
        # print("ACTION =", action)
        try:
            raw_weights = [
                {
                    "id_kriteria": "KRIT_0001",
                    "nama_kriteria": "processor",
                    "tipe_kriteria": request.POST.get(
                        "tipe_processor",
                        "benefit"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_processor",
                            0
                        )
                    )
                },
                {
                    "id_kriteria": "KRIT_0002",
                    "nama_kriteria": "ram",
                    "tipe_kriteria": request.POST.get(
                        "tipe_ram",
                        "benefit"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_ram",
                            0
                        )
                    )
                },
                {
                    "id_kriteria": "KRIT_0003",
                    "nama_kriteria": "storage",
                    "tipe_kriteria": request.POST.get(
                        "tipe_storage",
                        "benefit"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_storage",
                            0
                        )
                    )
                },
                {
                    "id_kriteria": "KRIT_0004",
                    "nama_kriteria": "berat",
                    "tipe_kriteria": request.POST.get(
                        "tipe_berat",
                        "cost"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_berat",
                            0
                        )
                    )
                },
                {
                    "id_kriteria": "KRIT_0005",
                    "nama_kriteria": "layar",
                    "tipe_kriteria": request.POST.get(
                        "tipe_layar",
                        "benefit"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_layar",
                            0
                        )
                    )
                },
                {
                    "id_kriteria": "KRIT_0006",
                    "nama_kriteria": "baterai",
                    "tipe_kriteria": request.POST.get(
                        "tipe_baterai",
                        "benefit"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_baterai",
                            0
                        )
                    )
                }
            ]
            request.session["selected_project"] = request.POST.get("id_proyek")
            request.session["selected_role"] = request.POST.get("id_role")
            request.session["dss_raw_weights"] = raw_weights
            request.session["minimum_requirement"] = {
                "processor_score":request.POST.get("min_processor_score"),
                "ram":request.POST.get("min_ram"),
                "storage":request.POST.get("min_storage"),
                "min_harga":min_harga
            }
            # ==========================
            # PROSES DSS SEKALI SAJA
            # ==========================
            selected_role  = request.session.get("selected_role")
            minimum_requirement = request.session.get("minimum_requirement",{})
            role_id = role.id_role
            if jenis_rekomendasi == "inventori":
                filter_data = FilterInventoriDTO(
                    min_ram_kapasitas=int(minimum_requirement.get("ram",0) or 0),
                    min_storage=int(minimum_requirement.get("storage",0) or 0),
                    processor_score=int(minimum_requirement.get("processor_score",0) or 0)
                )

            else:

                filter_data = FilterPengadaanDTO(
                    min_ram_kapasitas=int(minimum_requirement.get("ram",0) or 0),
                    min_storage=int(minimum_requirement.get("storage",0) or 0),
                    min_harga=int(minimum_requirement.get("min_harga",0) or 0),
                    processor_score=int(minimum_requirement.get("processor_score",0) or 0)
                )
            service = Servicesaw(conn)
            id_user = request.user.id_user if (hasattr(request.user, 'id_user') and request.user.id_user) else 'U001'
            hasil = service.proses_dss_saw(
                id_user=id_user,
                id_bobot=selected_role ,
                sumber_data=jenis_rekomendasi,
                filter_data=filter_data,
                role=[role_id],
                debug=True
            )
            # print("\n=== HASIL SERVICE ===")
            # print(hasil)
            if hasil.get("status") != "success":
                messages.error(request, hasil.get("message","Gagal menjalankan DSS"))
                return redirect("inputkriteria_hc")
            request.session["ranking_sesuai"] = (
                hasil["data"]
                ["rekomendasi_sesuai_role"]
                ["ranking"]
            )
            request.session["ranking_alternatif"] = (
                hasil["data"]
                ["alternatif_lain"]
                ["ranking"]
            )
            request.session["warning_dss"] = (hasil.get("warning"))
            request.session["jenis_rekomendasi"] = (
                request.POST.get(
                    "jenis_rekomendasi",
                    "inventori"
                )
            )
            request.session["selected_role_teknologi"] = selected_role
            request.session["minimum_requirement"] = minimum_requirement
            request.session.modified = True
            warning_dss = request.session.get("warning_dss")
            return redirect("hasilrekomendasi_hc")        
        except Exception as e:
            import traceback
            # print(traceback.format_exc())
            messages.error(request,f"Gagal memproses DSS: {str(e)}")
    projects = (Proyek.objects.all().order_by("nama_proyek"))
    role_teknologi = (
        RoleTeknologi.objects
        .select_related(
            "role",
            "teknologi"
        )
        .order_by(
            "role__nama_role",
            "teknologi__nama_teknologi"
        )
    )
    project_role_mapping = []
    for pr in ProjectRole.objects.select_related("proyek","role"):
        project_role_mapping.append({
            "id_proyek": pr.proyek.id_proyek,
            "id_role": pr.role.id_role,
            "nama": pr.role.nama_role
        })
    context = {
        "projects": projects,
        "role_teknologi": role_teknologi,
        "role_requirement": role_requirement,
        "processor_list": processor_list,
        "bobot_role": bobot_role,
        "selected_project": selected_project,
        "selected_role_teknologi": selected_role,
        "project_role_mapping":(project_role_mapping),
    }
    # print("="*50)
    # print("PROJECT ROLE MAPPING")
    # print(project_role_mapping)
    # print("="*50)
    repo_bobot = BobotKriteriaRepository(conn)
    role_teknologi_data = []
    for rt in role_teknologi:
        rows = repo_bobot.ambil_bobot_role_teknologi(rt.id_role_teknologi)
        bobot = {}
        for row in rows:
            bobot[row["nama_kriteria"].lower().strip()] = row["nilai_bobot"]
        role_teknologi_data.append({
            "id_role": rt.role.id_role,
            "id_role_teknologi": rt.id_role_teknologi,
            "teknologi": rt.teknologi.nama_teknologi,
            "bobot": bobot
        })
        context["role_teknologi_data"] = role_teknologi_data
    return render(request,"hc/dss/inputkriteria_hc.html",context)


def hasilrekomendasi_hc_view(request):
    conn = get_connection()

    try:
        conn = get_connection()
        repo_laptop = LaptopInventoriRepository(conn)
        repo_laptop_pengadaan = LaptopPengadaanRepository(conn)
        selected_role_teknologi = request.session.get(
            "selected_role_teknologi"
        )

        minimum_requirement = request.session.get(
            "minimum_requirement",
            {}
        )
        jenis_rekomendasi = request.session.get(
            "jenis_rekomendasi",
            "inventori"
        )


        if not selected_role_teknologi:

            messages.error(
                request,
                "Role teknologi belum dipilih"
            )

            return redirect(
                "inputkriteria_hc"
            )
            
        ranking_sesuai = request.session.get("ranking_sesuai",[])
        ranking_alternatif = request.session.get("ranking_alternatif",[])
        id_sesuai = {item["id"] for item in ranking_sesuai}
        ranking_alternatif = [item for item in ranking_alternatif if item["id"] not in id_sesuai]
        
        warning = request.session.get("warning_dss")
        # if not ranking_sesuai:
        #     messages.error(request,"Silakan hitung DSS terlebih dahulu")
        #     return redirect("inputkriteria_it")
        sort_by = request.GET.get("sort","skor_desc")
        # print("\n=== TEST DETAIL ===")
        # print(
        #     repo_laptop.ambil_spek_laptop(
        #         ranking_sesuai[9]["id"]
        #     )
        # )
        # print("\n=== RANKING PERTAMA ===")
        # print(ranking_sesuai[0])

        for ranking_list in [ranking_sesuai, ranking_alternatif]:
            if not ranking_list:
                continue

            for item in ranking_list:
                if jenis_rekomendasi == "inventori":
                    laptop = repo_laptop.ambil_spek_laptop(item["id"]) or {}
                    laptop_obj = LaptopInventori.objects.filter(id_laptop_inventori=item["id"]).first()
                    nama_laptop = (laptop_obj.nama_laptop if (laptop_obj and laptop_obj.nama_laptop) else None) or laptop.get("nama_laptop") or laptop.get("model") or item["id"]

                    try:
                        item["skor"] = float(item.get("skor", 0))
                    except (ValueError, TypeError):
                        pass

                    item["detail"] = {
                        "nama": nama_laptop,
                        "processor":
                            f"{laptop.get('manufacturer', '')} "
                            f"{laptop.get('processor_model', '')}".strip(),
                        "ram": laptop.get("ram_kapasitas", 0),
                        "storage": laptop.get("storage_kapasitas", 0),
                        "layar": "-",
                        "benchmark": laptop.get("processor_score", 0)
                    }
                elif jenis_rekomendasi == "pengadaan":
                    pengadaan = repo_laptop_pengadaan.ambil_laptop_pengadaan_by_id(
                        item["id"]
                    )
                    print("=" * 50)
                    print("ID =", item["id"])
                    print("PENGADAAN =", pengadaan)
                    print("=" * 50)
                    try:
                        item["skor"] = float(item.get("skor", 0))
                    except (ValueError, TypeError):
                        pass
                    item["detail"] = {
                        "nama": pengadaan.get("nama_laptop",item["id"]),
                        "processor":
                            f"{pengadaan.get('manufacturer', '')} "
                            f"{pengadaan.get('processor_model', '')}",
                        "ram":pengadaan.get("ram_kapasitas",0),
                        "storage":pengadaan.get("storage_kapasitas",0),
                        "layar":pengadaan.get("ukuran_layar",0),
                        "harga":pengadaan.get("harga",0),
                        "benchmark":pengadaan.get("processor_score",0),
                        "gpu":pengadaan.get("gpu","-"),
                        "baterai":pengadaan.get("baterai",0),
                        "berat":pengadaan.get("berat",0)
                    }    
        rata_rata_harga = 0
        if jenis_rekomendasi == "pengadaan":

            harga_list = []

            for item in ranking_sesuai:

                harga = (
                    item["detail"]
                    .get("harga", 0)
                )

                if harga:
                    harga_list.append(harga)

            if harga_list:
                rata_rata_harga = (
                    sum(harga_list)
                    / len(harga_list)
                )
        if sort_by == "skor_desc":
            ranking_sesuai.sort(key=lambda x: x["skor"],reverse=True)
        elif sort_by == "skor_asc":
            ranking_sesuai.sort(key=lambda x: x["skor"])
        elif sort_by == "harga_asc" and jenis_rekomendasi == "pengadaan":
            ranking_sesuai.sort(key=lambda x: x["detail"].get("harga", 0))
        
        paginator = Paginator(ranking_sesuai, 999999)  # Tampilkan 10 item per halaman
        page_number = request.GET.get('page')
        rangking_page = paginator.get_page(page_number)
        alternatif_paginator = Paginator(ranking_alternatif, 999999)
        alternatif_page_number = request.GET.get('alternatif_page')
        ranking_alternatif = alternatif_paginator.get_page(alternatif_page_number)

        from inventori.models import Pengajuan, User as InvUser
        selected_pengajuan_id = request.GET.get("id_pengajuan") or request.session.get("id_pengajuan")
        selected_pengajuan = None
        target_user_nama = None
        if selected_pengajuan_id:
            try:
                selected_pengajuan = Pengajuan.objects.filter(id_pengajuan=selected_pengajuan_id).first()
                if selected_pengajuan:
                    u_obj = InvUser.objects.filter(id_user=selected_pengajuan.id_user_id).first()
                    target_user_nama = u_obj.nama if u_obj else selected_pengajuan.id_user_id
            except Exception:
                pass

        pending_pengajuan_qs = Pengajuan.objects.filter(status__in=['pending', 'menunggu'])
        pending_pengajuan_list = []
        for p in pending_pengajuan_qs:
            u_obj = InvUser.objects.filter(id_user=p.id_user_id).first()
            u_nama = u_obj.nama if u_obj else p.id_user_id
            pending_pengajuan_list.append({
                'id_pengajuan': p.id_pengajuan,
                'user_nama': u_nama,
                'kebutuhan_role': p.kebutuhan_role
            })

        context = {
            "ranking_sesuai": rangking_page,
            "ranking_alternatif": ranking_alternatif,
            "jenis_rekomendasi":jenis_rekomendasi,
            "sort_by": sort_by,
            "top_3":ranking_sesuai[:3],
            "total_alternatif":len(ranking_sesuai),
            "rata_rata_harga":rata_rata_harga,
            "skor_tertinggi":
                ranking_sesuai[0]["skor"]
                if ranking_sesuai
                else 0,
            "warning": warning,
            "selected_pengajuan_id": selected_pengajuan_id,
            "selected_pengajuan": selected_pengajuan,
            "target_user_nama": target_user_nama,
            "pending_pengajuan_list": pending_pengajuan_list,
        }
        # print("=" * 50)
        # print("JENIS TEMPLATE =", jenis_rekomendasi)
        # print("RATA RATA =", rata_rata_harga)
        # print("=" * 50)
        
        # print("HARGA LIST =", harga_list)
        return render(
            request,
            "hc/dss/hasilrekomendasi_hc.html",
            context
        )

    except Exception as e:

        import traceback

        traceback.print_exc()

        messages.error(
            request,
            f"Error DSS: {str(e)}"
        )

        return redirect(
            "inputkriteria_hc"
        )               
def detailrekomendasi_hc_view(request):
    conn = get_connection()

    try:
        laptop_id = request.GET.get("id")
        jenis = request.GET.get("jenis", "inventori")

        if not laptop_id:
            messages.error(request, "ID laptop tidak ditemukan.")
            return redirect("hasilrekomendasi_hc")

        repo_laptop = LaptopInventoriRepository(conn)
        repo_pengadaan = LaptopPengadaanRepository(conn)

        if jenis == "inventori":
            laptop = repo_laptop.ambil_detail_laptop(laptop_id)
            if not laptop:
                messages.error(
                    request,
                    "Laptop tidak ditemukan"
                )
                return redirect(
                    "hasilrekomendasi_hc"
                )
            return render(
                request,
                "hc/dss/detailrekomendasi_hc.html",
                {
                    "detail": laptop
                }
            )

        pengadaan = repo_pengadaan.ambil_laptop_pengadaan_by_id(laptop_id)

        if not pengadaan:
            messages.error(request, "Data laptop pengadaan tidak ditemukan.")
            return redirect("hasilrekomendasi_hc")
        detail = {
            "id": pengadaan.get("id_laptop_pengadaan"),
            "nama_laptop": pengadaan.get("nama_laptop"),
            "harga": pengadaan.get("harga", 0),
            "harga_format": f"{pengadaan.get('harga', 0):,.0f}",
            "gpu": pengadaan.get("gpu", "-"),
            "layar": pengadaan.get("ukuran_layar", 0),
            "baterai": pengadaan.get("baterai", 0),
            "berat": pengadaan.get("berat", 0),
            "nama_processor": pengadaan.get("nama_processor", "-"),
            "manufacturer": pengadaan.get("manufacturer", "-"),
            "processor_model": pengadaan.get("processor_model", "-"),
            "cores": pengadaan.get("cores", 0),
            "threads": pengadaan.get("threads", 0),
            "processor_score": pengadaan.get("processor_score", 0),
            "ram": pengadaan.get("ram_kapasitas", 0),
            "ram_tipe": pengadaan.get("ram_tipe", "-"),
            "storage": pengadaan.get("storage_kapasitas", 0),
            "storage_tipe": pengadaan.get("storage_tipe", "-"),
        }

        return render(
            request,
            "hc/dss/detailrekomendasiscrapping_hc.html",
            {"detail": detail}
        )

    except Exception as e:
        print("ERROR DETAIL REKOMENDASI:", repr(e))
        messages.error(request, f"Terjadi kesalahan: {str(e)}")
        return redirect("hasilrekomendasi_hc")

    finally:
        if conn:
            conn.close()

def detailrekomendasiscrapping_hc_view(request):
    return render(request, 'hc/dss/detailrekomendasiscrapping_hc.html')

def notifikasi_hc_view(request):
    from inventori.models import Pengajuan, Peminjaman
    import datetime
    
    today = datetime.date.today()
    notifications = []
    
    # 1. Notifikasi pengajuan menunggu persetujuan
    try:
        menunggu_list = Pengajuan.objects.filter(status__in=['menunggu', 'pending']).select_related('id_user').order_by('-tanggal_pengajuan')
        for p in menunggu_list:
            tgl_target = p.bulan if p.bulan else today
            diff_days = (tgl_target - today).days
            
            if diff_days <= 3:
                urgency_class = 'urgent'
                urgency_tag = 'Sangat Mendesak'
            elif diff_days <= 7:
                urgency_class = 'warning'
                urgency_tag = 'Mendesak'
            else:
                urgency_class = 'info'
                urgency_tag = 'Pengajuan Masuk'
                
            if diff_days < 0:
                time_str = f"Lewat {abs(diff_days)} hari"
            elif diff_days == 0:
                time_str = "Hari ini"
            elif diff_days == 1:
                time_str = "Besok"
            else:
                time_str = f"{diff_days} hari lagi"
                
            u_nama = p.id_user.nama if hasattr(p.id_user, 'nama') else str(p.id_user or '-')
            tgl_pengajuan_str = p.tanggal_pengajuan.strftime('%d %B %Y') if hasattr(p, 'tanggal_pengajuan') and p.tanggal_pengajuan and hasattr(p.tanggal_pengajuan, 'strftime') else ''

            notifications.append({
                'tipe': 'pengajuan',
                'id_pengajuan': p.id_pengajuan,
                'user_nama': u_nama,
                'kebutuhan_role': p.kebutuhan_role,
                'perusahaan': p.perusahaan or '-',
                'bulan': p.bulan.strftime('%d %B %Y') if hasattr(p.bulan, 'strftime') else str(p.bulan or '-'),
                'tanggal_pengajuan': tgl_pengajuan_str,
                'urgency_class': urgency_class,
                'urgency_tag': urgency_tag,
                'time_str': time_str,
                'keterangan': p.keterangan
            })
    except Exception as e:
        pass
    
    # 2. Notifikasi pengembalian laptop menunggu konfirmasi HC (TC-TRX-18)
    try:
        pengembalian_list = Peminjaman.objects.filter(status='dikembalikan').select_related('id_user', 'id_laptop_inventori')
        for pem in pengembalian_list:
            u_nama = pem.id_user.nama if hasattr(pem.id_user, 'nama') else str(pem.id_user or '-')
            laptop_nama = pem.id_laptop_inventori.nama_laptop if hasattr(pem.id_laptop_inventori, 'nama_laptop') else '-'
            tgl_kembali = pem.tanggal_kembali
            if tgl_kembali:
                sisa = (today - tgl_kembali).days
                waktu_str = "Hari ini" if sisa <= 0 else f"{sisa} hari lalu"
            else:
                waktu_str = "-"

            notifications.append({
                'tipe': 'pengembalian',
                'id_peminjaman': pem.id_peminjaman,
                'user_nama': u_nama,
                'laptop_nama': laptop_nama,
                'tanggal_kembali': tgl_kembali.strftime('%d %B %Y') if tgl_kembali and hasattr(tgl_kembali, 'strftime') else str(tgl_kembali or '-'),
                'keterangan': pem.keterangan or '-',
                'urgency_class': 'warning',
                'urgency_tag': 'Menunggu Konfirmasi',
                'time_str': waktu_str,
            })
    except Exception as e:
        pass
    
    # 3. Notifikasi jatuh tempo hampir tiba (TC-TRX-17)
    try:
        aktif_list = Peminjaman.objects.filter(status__in=['dipinjam', 'aktif']).select_related('id_user', 'id_laptop_inventori')
        for pem in aktif_list:
            if hasattr(pem, 'tanggal_jatuh_tempo') and pem.tanggal_jatuh_tempo:
                sisa = (pem.tanggal_jatuh_tempo - today).days
                if sisa <= 3:
                    urgency_class = 'urgent'
                    urgency_tag = 'Jatuh Tempo Hampir Tiba'
                elif sisa <= 7:
                    urgency_class = 'warning'
                    urgency_tag = 'Jatuh Tempo Segera'
                else:
                    continue  # Skip if plenty of time

                u_nama = pem.id_user.nama if hasattr(pem.id_user, 'nama') else str(pem.id_user or '-')
                laptop_nama = pem.id_laptop_inventori.nama_laptop if hasattr(pem.id_laptop_inventori, 'nama_laptop') else '-'
                if sisa < 0:
                    time_str = f"Lewat {abs(sisa)} hari (Telat!)"
                elif sisa == 0:
                    time_str = "Hari ini (Jatuh Tempo)"
                else:
                    time_str = f"{sisa} hari lagi"

                notifications.append({
                    'tipe': 'jatuh_tempo',
                    'id_peminjaman': pem.id_peminjaman,
                    'user_nama': u_nama,
                    'laptop_nama': laptop_nama,
                    'tanggal_jatuh_tempo': pem.tanggal_jatuh_tempo.strftime('%d %B %Y') if hasattr(pem.tanggal_jatuh_tempo, 'strftime') else str(pem.tanggal_jatuh_tempo),
                    'urgency_class': urgency_class,
                    'urgency_tag': urgency_tag,
                    'time_str': time_str,
                })
    except Exception as e:
        pass
        
    return render(request, 'hc/inventori/notifikasi_hc.html', {
        'notifications': notifications,
        'total_pengembalian_menunggu': len([n for n in notifications if n.get('tipe') == 'pengembalian']),
        'total_pengajuan_menunggu': len([n for n in notifications if n.get('tipe') == 'pengajuan']),
    })


# ==========================================
# 2. INFORMATION TECHNOLOGY (IT) VIEWS (START FROM SCRATCH)
# ==========================================

def dashboard_it_view(request):
    try:
        total_laptop = LaptopInventori.objects.count()
        service = PengajuanService()
        semua_pengajuan = service.service_ambil_semua_pengajuan()
        total_pengajuan = len(semua_pengajuan)
        pengajuan_menunggu = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'menunggu')
    except Exception:
        total_laptop = 0
        total_pengajuan = 0
        pengajuan_menunggu = 0

    context = {
        'total_laptop': total_laptop,
        'total_pengajuan': total_pengajuan,
        'pengajuan_menunggu': pengajuan_menunggu,
    }
    return render(request, 'it/dashboard/dashboard_it.html', context)

def manajemenlaptop_it_view(request):
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

    from inventori.models import LaptopInventori
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
    return render(request, 'it/inventori/manajemenlaptop_it.html', context)

# def pengajuanlaptop_it_view(request):
#     from inventori.services.service_pengajuan import PengajuanService
#     from inventori.repositories.dto.dto_pengajuan import PengajuanDTO
    
#     context = {
#         'laptop': laptop,
#         'processors': processors,
#         'rams': rams,
#         'storages': storages,
#     }
#     return render(request, 'it/inventori/editdatalaptop_it.html', context)

def inputkriteria_it_view(request):
    conn = connection
    
    selected_project = (request.GET.get("id_proyek")or request.POST.get("id_proyek"))
    selected_role  = (request.GET.get("id_role")or request.POST.get("id_role"))
    role_requirement = None
    bobot_role = None
    selected_role_teknologi = (
    request.GET.get("id_role_teknologi")
    or request.POST.get("id_role_teknologi"))
    processor_service = ReadProcessorService()
    processor_list = processor_service.ambil_processor()
    bobot_role = None
    # ==========================
    # LOAD ROLE REQUIREMENT
    # ==========================
    if selected_role:
        try:
            from inventori.models import Role
            role = Role.objects.get(id_role=selected_role)
            print("=" * 50)
            print("AMBIL ROLETEK")
            print("=" * 50)
            role_teknologi_list = (RoleTeknologi.objects.select_related("teknologi").filter(role_id=selected_role))
            print("JUMLAH ROLETEK =",role_teknologi_list.count())
            role_requirement = {
                "id_role": role.id_role,
                "nama_role": role.nama_role,
                "min_ram": role.min_ram,
                "min_storage": role.min_storage,
                "nama_processor": role.nama_processor,
                "min_processor_score": role.min_processor_score
            }
            repo_bobot = BobotKriteriaRepository(conn)
            aggregation_service = AggregationService(conn)
            hasil_teknologi = []
            for rt in role_teknologi_list:
                print("=" * 40)
                print("ROLETEK :",rt.id_role_teknologi)
                print("TEKNOLOGI :",rt.teknologi.nama_teknologi)
                rows = (
                    repo_bobot
                    .ambil_bobot_role_teknologi(
                        rt.id_role_teknologi
                    )
                )
                print("JUMLAH BOBOT :",len(rows))
                hasil_teknologi.append(
                    rows
                )
            if hasil_teknologi:
                bobot_role = (
                    aggregation_service
                    .aggregate_teknologi_role(
                        hasil_teknologi
                    )
                )
            else:
                bobot_role = {}

            # print("BOBOT AGREGASI =",bobot_role)
        except Exception as e:
            print(
                "ERROR ROLE REQUIREMENT:",
                str(e)
            )
    # ==========================
    # PROSES DSS
    # ==========================
    if request.method == "POST":

        # print("=" * 50)
        # print("POST DSS")
        # print("POST =", request.POST)
        action = request.POST.get("action","load")
        jenis_rekomendasi = request.POST.get("jenis_rekomendasi","inventori")
        min_harga = request.POST.get("min_harga","")
        # print("JENIS =", jenis_rekomendasi)
        # print("MIN HARGA =", min_harga)
        # print("ACTION =", action)
        try:

            raw_weights = [
                {
                    "id_kriteria": "KRIT_0001",
                    "nama_kriteria": "processor",
                    "tipe_kriteria": request.POST.get(
                        "tipe_processor",
                        "benefit"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_processor",
                            0
                        )
                    )
                },
                {
                    "id_kriteria": "KRIT_0002",
                    "nama_kriteria": "ram",
                    "tipe_kriteria": request.POST.get(
                        "tipe_ram",
                        "benefit"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_ram",
                            0
                        )
                    )
                },
                {
                    "id_kriteria": "KRIT_0003",
                    "nama_kriteria": "storage",
                    "tipe_kriteria": request.POST.get(
                        "tipe_storage",
                        "benefit"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_storage",
                            0
                        )
                    )
                },
                {
                    "id_kriteria": "KRIT_0004",
                    "nama_kriteria": "berat",
                    "tipe_kriteria": request.POST.get(
                        "tipe_berat",
                        "cost"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_berat",
                            0
                        )
                    )
                },
                {
                    "id_kriteria": "KRIT_0005",
                    "nama_kriteria": "layar",
                    "tipe_kriteria": request.POST.get(
                        "tipe_layar",
                        "benefit"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_layar",
                            0
                        )
                    )
                },
                {
                    "id_kriteria": "KRIT_0006",
                    "nama_kriteria": "baterai",
                    "tipe_kriteria": request.POST.get(
                        "tipe_baterai",
                        "benefit"
                    ),
                    "nilai_bobot": float(
                        request.POST.get(
                            "bobot_baterai",
                            0
                        )
                    )
                }
            ]
            request.session["selected_project"] = request.POST.get("id_proyek")
            request.session["selected_role"] = request.POST.get("id_role")
            request.session["dss_raw_weights"] = raw_weights
            request.session["minimum_requirement"] = {
                "processor_score":request.POST.get("min_processor_score"),
                "ram":request.POST.get("min_ram"),
                "storage":request.POST.get("min_storage"),
                "min_harga":min_harga
            }
            # ==========================
            # PROSES DSS SEKALI SAJA
            # ==========================
            selected_role  = request.session.get("selected_role")
            minimum_requirement = request.session.get("minimum_requirement",{})
            role_id = role.id_role
            if jenis_rekomendasi == "inventori":
                filter_data = FilterInventoriDTO(
                    min_ram_kapasitas=int(minimum_requirement.get("ram",0) or 0),
                    min_storage=int(minimum_requirement.get("storage",0) or 0),
                    processor_score=int(minimum_requirement.get("processor_score",0) or 0)
                )

            else:

                filter_data = FilterPengadaanDTO(
                    min_ram_kapasitas=int(minimum_requirement.get("ram",0) or 0),
                    min_storage=int(minimum_requirement.get("storage",0) or 0),
                    min_harga=int(minimum_requirement.get("min_harga",0) or 0),
                    processor_score=int(minimum_requirement.get("processor_score",0) or 0)
                )

            service = Servicesaw(conn)
            id_user = request.user.id_user if (hasattr(request.user, 'id_user') and request.user.id_user) else 'U002'
            hasil = service.proses_dss_saw(
                id_user=id_user,
                id_bobot=selected_role ,
                sumber_data=jenis_rekomendasi,
                filter_data=filter_data,
                role=[role_id],
                debug=True
            )

            # print("\n=== HASIL SERVICE ===")
            # print(hasil)
            if hasil.get("status") != "success":
                messages.error(
                    request,
                    hasil.get(
                        "message",
                        "Gagal menjalankan DSS"
                    )
                )
                return redirect("inputkriteria_it")
            request.session["ranking_sesuai"] = (
                hasil["data"]
                ["rekomendasi_sesuai_role"]
                ["ranking"]
            )
            request.session["ranking_alternatif"] = (
                hasil["data"]
                ["alternatif_lain"]
                ["ranking"]
            )
            request.session["warning_dss"] = (hasil.get("warning"))
            request.session["jenis_rekomendasi"] = (
                request.POST.get(
                    "jenis_rekomendasi",
                    "inventori"
                )
            )
            warning_dss = request.session.get("warning_dss")
            return redirect("hasilrekomendasi_it")        
        except Exception as e:
            import traceback
            # print(traceback.format_exc())
            messages.error(request,f"Gagal memproses DSS: {str(e)}")
    projects = (Proyek.objects.all().order_by("nama_proyek"))

    role_teknologi = (
        RoleTeknologi.objects
        .select_related(
            "role",
            "teknologi"
        )
        .order_by(
            "role__nama_role",
            "teknologi__nama_teknologi"
        )
    )
    project_role_mapping = []

    for pr in ProjectRole.objects.select_related("proyek","role"):
        project_role_mapping.append({
            "id_proyek": pr.proyek.id_proyek,
            "id_role": pr.role.id_role,
            "nama": pr.role.nama_role
        })
    context = {
        "projects": projects,
        "role_teknologi": role_teknologi,
        "role_requirement": role_requirement,
        "processor_list": processor_list,
        "bobot_role": bobot_role,
        "selected_project": selected_project,
        "selected_role_teknologi": selected_role,
        "project_role_mapping":(project_role_mapping),
    }
    # print("="*50)
    # print("PROJECT ROLE MAPPING")
    # print(project_role_mapping)
    # print("="*50)
    repo_bobot = BobotKriteriaRepository(conn)
    role_teknologi_data = []
    for rt in role_teknologi:
        rows = repo_bobot.ambil_bobot_role_teknologi(rt.id_role_teknologi)
        bobot = {}
        for row in rows:
            bobot[row["nama_kriteria"].lower().strip()] = row["nilai_bobot"]
        role_teknologi_data.append({
            "id_role": rt.role.id_role,
            "id_role_teknologi": rt.id_role_teknologi,
            "teknologi": rt.teknologi.nama_teknologi,
            "bobot": bobot
        })
        context["role_teknologi_data"] = role_teknologi_data

    return render(
        request,
        "it/dss/inputkriteria_it.html",
        context
    )

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



def editdatalaptop_it_view(request, id_laptop):
    from inventori.models import LaptopInventori, Processor, RAM, Storage
    from inventori.services.laptop_inventori.update import UpdateLaptopInventoriService
    from inventori.dto.dto_laptop_inventori import LaptopInventoriDTO
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




def hasilrekomendasi_it_view(request):
    conn = get_connection()

    try:
        conn = get_connection()
        repo_laptop = LaptopInventoriRepository(conn)
        repo_laptop_pengadaan = LaptopPengadaanRepository(conn)
        selected_role_teknologi = request.session.get(
            "selected_role_teknologi"
        )

        minimum_requirement = request.session.get(
            "minimum_requirement",
            {}
        )
        jenis_rekomendasi = request.session.get(
            "jenis_rekomendasi",
            "inventori"
        )


        if not selected_role_teknologi:

            messages.error(
                request,
                "Role teknologi belum dipilih"
            )

            return redirect(
                "inputkriteria_it"
            )
            
        ranking_sesuai = request.session.get("ranking_sesuai",[])
        ranking_alternatif = request.session.get("ranking_alternatif",[])
        id_sesuai = {item["id"] for item in ranking_sesuai}
        ranking_alternatif = [item for item in ranking_alternatif if item["id"] not in id_sesuai]
        
        warning = request.session.get("warning_dss")
        # if not ranking_sesuai:
        #     messages.error(request,"Silakan hitung DSS terlebih dahulu")
        #     return redirect("inputkriteria_it")
        sort_by = request.GET.get("sort","skor_desc")
        # print("\n=== TEST DETAIL ===")
        # print(
        #     repo_laptop.ambil_spek_laptop(
        #         ranking_sesuai[9]["id"]
        #     )
        # )
        # print("\n=== RANKING PERTAMA ===")
        # print(ranking_sesuai[0])

        for ranking_list in [ranking_sesuai, ranking_alternatif]:
            if not ranking_list:
                continue

            for item in ranking_list:
                if jenis_rekomendasi == "inventori":

                    laptop = repo_laptop.ambil_spek_laptop(
                        item["id"]
                    )

                    item["detail"] = {

                        "nama": item["id"],

                        "processor":
                            f"{laptop.get('manufacturer', '')} "
                            f"{laptop.get('processor_model', '')}",

                        "ram":
                            laptop.get(
                                "ram_kapasitas",
                                0
                            ),

                        "storage":
                            laptop.get(
                                "storage_kapasitas",
                                0
                            ),

                        "layar":
                            "-",

                        "benchmark":
                            laptop.get(
                                "processor_score",
                                0
                            )
                    }
                elif jenis_rekomendasi == "pengadaan":
                    pengadaan = repo_laptop_pengadaan.ambil_laptop_pengadaan_by_id(
                        item["id"]
                    )
                    # print("=" * 50)
                    # print("ID =", item["id"])
                    # print("PENGADAAN =", pengadaan)
                    # print("=" * 50)
                    item["detail"] = {
                        "nama": pengadaan.get("nama_laptop",item["id"]),
                        "processor":
                            f"{pengadaan.get('manufacturer', '')} "
                            f"{pengadaan.get('processor_model', '')}",
                        "ram":pengadaan.get("ram_kapasitas",0),
                        "storage":pengadaan.get("storage_kapasitas",0),
                        "layar":pengadaan.get("ukuran_layar",0),
                        "harga":pengadaan.get("harga",0),
                        "benchmark":pengadaan.get("processor_score",0),
                        "gpu":pengadaan.get("gpu","-"),
                        "baterai":pengadaan.get("baterai",0),
                        "berat":pengadaan.get("berat",0)
                    }    
        rata_rata_harga = 0
        if jenis_rekomendasi == "pengadaan":

            harga_list = []

            for item in ranking_sesuai:

                harga = (
                    item["detail"]
                    .get("harga", 0)
                )

                if harga:
                    harga_list.append(harga)

            if harga_list:
                rata_rata_harga = (
                    sum(harga_list)
                    / len(harga_list)
                )
        if sort_by == "skor_desc":
            ranking_sesuai.sort(key=lambda x: x["skor"],reverse=True)
        elif sort_by == "skor_asc":
            ranking_sesuai.sort(key=lambda x: x["skor"])
        elif sort_by == "harga_asc" and jenis_rekomendasi == "pengadaan":
            ranking_sesuai.sort(key=lambda x: x["detail"].get("harga", 0))
        
        paginator = Paginator(ranking_sesuai, 999999)  # Tampilkan 10 item per halaman
        page_number = request.GET.get('page')
        rangking_page = paginator.get_page(page_number)
        alternatif_paginator = Paginator(ranking_alternatif, 999999)
        alternatif_page_number = request.GET.get('alternatif_page')
        ranking_alternatif = alternatif_paginator.get_page(alternatif_page_number)

        context = {
            "ranking_sesuai": rangking_page,
            "ranking_alternatif": ranking_alternatif,
            "jenis_rekomendasi":jenis_rekomendasi,
            "sort_by": sort_by,
            "top_3":ranking_sesuai[:3],
            "total_alternatif":len(ranking_sesuai),
            "rata_rata_harga":rata_rata_harga,
            "skor_tertinggi":
                ranking_sesuai[0]["skor"]
                if ranking_sesuai
                else 0,
            "warning": warning, 
        }
        # print("=" * 50)
        # print("JENIS TEMPLATE =", jenis_rekomendasi)
        # print("RATA RATA =", rata_rata_harga)
        # print("=" * 50)
        
        # print("HARGA LIST =", harga_list)
        return render(
            request,
            "it/dss/hasilrekomendasi_it.html",
            context
        )

    except Exception as e:

        import traceback

        traceback.print_exc()

        messages.error(
            request,
            f"Error DSS: {str(e)}"
        )

        return redirect(
            "inputkriteria_it"
        )

def detailrekomendasi_it_view(request):
    conn = get_connection()

    try:
        laptop_id = request.GET.get("id")
        jenis = request.GET.get("jenis", "inventori")

        if not laptop_id:
            messages.error(request, "ID laptop tidak ditemukan.")
            return redirect("hasilrekomendasi_it")

        repo_laptop = LaptopInventoriRepository(conn)
        repo_pengadaan = LaptopPengadaanRepository(conn)

        if jenis == "inventori":
            laptop = repo_laptop.ambil_detail_laptop(laptop_id)
            if not laptop:
                messages.error(
                    request,
                    "Laptop tidak ditemukan"
                )
                return redirect(
                    "hasilrekomendasi_hc"
                )
            return render(
                request,
                "it/dss/detailrekomendasi_it.html",
                {
                    "detail": laptop
                }
            )

        pengadaan = repo_pengadaan.ambil_laptop_pengadaan_by_id(laptop_id)

        if not pengadaan:
            messages.error(request, "Data laptop pengadaan tidak ditemukan.")
            return redirect("hasilrekomendasi_it")
        detail = {
            "id": pengadaan.get("id_laptop_pengadaan"),
            "nama_laptop": pengadaan.get("nama_laptop"),
            "harga": pengadaan.get("harga", 0),
            "harga_format": f"{pengadaan.get('harga', 0):,.0f}",
            "gpu": pengadaan.get("gpu", "-"),
            "layar": pengadaan.get("ukuran_layar", 0),
            "baterai": pengadaan.get("baterai", 0),
            "berat": pengadaan.get("berat", 0),
            "nama_processor": pengadaan.get("nama_processor", "-"),
            "manufacturer": pengadaan.get("manufacturer", "-"),
            "processor_model": pengadaan.get("processor_model", "-"),
            "cores": pengadaan.get("cores", 0),
            "threads": pengadaan.get("threads", 0),
            "processor_score": pengadaan.get("processor_score", 0),
            "ram": pengadaan.get("ram_kapasitas", 0),
            "ram_tipe": pengadaan.get("ram_tipe", "-"),
            "storage": pengadaan.get("storage_kapasitas", 0),
            "storage_tipe": pengadaan.get("storage_tipe", "-"),
        }

        return render(
            request,
            "it/dss/detailrekomendasiscrapping_it.html",
            {"detail": detail}
        )

    except Exception as e:
        print("ERROR DETAIL REKOMENDASI:", repr(e))
        messages.error(request, f"Terjadi kesalahan: {str(e)}")
        return redirect("hasilrekomendasi_it")

    finally:
        if conn:
            conn.close()
                        
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
    from inventori.models import Pengajuan, Peminjaman
    import datetime
    
    today = datetime.date.today()
    notifications = []
    total_pengembalian_menunggu = 0
    total_pengajuan_menunggu = 0
    
    try:
        menunggu_list = Pengajuan.objects.filter(status__in=['menunggu', 'pending']).select_related('id_user').order_by('-tanggal_pengajuan')
        total_pengajuan_menunggu = menunggu_list.count()
        for p in menunggu_list:
            tgl_target = p.bulan if p.bulan else today
            diff_days = (tgl_target - today).days
            
            if diff_days <= 3:
                urgency_class = 'urgent'
                urgency_tag = 'Sangat Mendesak'
            elif diff_days <= 7:
                urgency_class = 'warning'
                urgency_tag = 'Mendesak'
            else:
                urgency_class = 'info'
                urgency_tag = 'Pengajuan Masuk'
                
            if diff_days < 0:
                time_str = f"Lewat {abs(diff_days)} hari"
            elif diff_days == 0:
                time_str = "Hari ini"
            elif diff_days == 1:
                time_str = "Besok"
            else:
                time_str = f"{diff_days} hari lagi"
                
            u_nama = p.id_user.nama if hasattr(p.id_user, 'nama') else str(p.id_user or '-')
            tgl_pengajuan_str = p.tanggal_pengajuan.strftime('%d %B %Y') if hasattr(p, 'tanggal_pengajuan') and p.tanggal_pengajuan and hasattr(p.tanggal_pengajuan, 'strftime') else ''

            notifications.append({
                'tipe': 'pengajuan',
                'id_pengajuan': p.id_pengajuan,
                'user_nama': u_nama,
                'kebutuhan_role': p.kebutuhan_role,
                'perusahaan': p.perusahaan or '-',
                'bulan': p.bulan.strftime('%d %B %Y') if hasattr(p.bulan, 'strftime') else str(p.bulan or '-'),
                'tanggal_pengajuan': tgl_pengajuan_str,
                'urgency_class': urgency_class,
                'urgency_tag': urgency_tag,
                'time_str': time_str,
                'keterangan': p.keterangan
            })
    except Exception:
        pass

    # 2. Notifikasi pengembalian laptop menunggu konfirmasi IT
    try:
        pengembalian_list = Peminjaman.objects.filter(status='dikembalikan').select_related('id_user', 'id_laptop_inventori')
        total_pengembalian_menunggu = pengembalian_list.count()
        for pem in pengembalian_list:
            u_nama = pem.id_user.nama if hasattr(pem.id_user, 'nama') else str(pem.id_user or '-')
            laptop_nama = pem.id_laptop_inventori.nama_laptop if hasattr(pem.id_laptop_inventori, 'nama_laptop') else '-'
            tgl_kembali = pem.tanggal_kembali
            if tgl_kembali:
                sisa = (today - tgl_kembali).days
                waktu_str = "Hari ini" if sisa <= 0 else f"{sisa} hari lalu"
            else:
                waktu_str = "-"

            notifications.append({
                'tipe': 'pengembalian',
                'id_peminjaman': pem.id_peminjaman,
                'user_nama': u_nama,
                'laptop_nama': laptop_nama,
                'tanggal_kembali': tgl_kembali.strftime('%d %B %Y') if tgl_kembali and hasattr(tgl_kembali, 'strftime') else str(tgl_kembali or '-'),
                'keterangan': pem.keterangan or '-',
                'urgency_class': 'warning',
                'urgency_tag': 'Menunggu Konfirmasi',
                'time_str': waktu_str,
            })
    except Exception:
        pass
        
    return render(request, 'it/inventori/notifikasi_it.html', {
        'notifications': notifications,
        'total_pengajuan_menunggu': total_pengajuan_menunggu,
        'total_pengembalian_menunggu': total_pengembalian_menunggu,
    })

# Procurement management views for IT
def manajemenpengadaan_it_view(request):
    search_query = request.GET.get('q', '').strip()
    processor_filter = request.GET.get('processor', '').strip()
    ram_filter = request.GET.get('ram', '').strip()
    storage_filter = request.GET.get('storage', '').strip()
    min_layar = request.GET.get('min_layar', '').strip()
    max_layar = request.GET.get('max_layar', '').strip()
    min_baterai = request.GET.get('min_baterai', '').strip()
    max_baterai = request.GET.get('max_baterai', '').strip()
    min_harga = request.GET.get('min_harga', '').strip()
    max_harga = request.GET.get('max_harga', '').strip()
    
    conn = get_connection()
    try:
        repo = LaptopPengadaanRepository(conn)
        raw_list = repo.ambil_laptop_pengadaan()
        
        all_processors = sorted(list(set(item.get('nama_processor') for item in raw_list if item.get('nama_processor'))))
        all_ram = sorted(list(set(int(item.get('ram_kapasitas')) for item in raw_list if item.get('ram_kapasitas'))))
        all_storage = sorted(list(set(int(item.get('storage_kapasitas')) for item in raw_list if item.get('storage_kapasitas'))))

        if search_query:
            raw_list = [
                item for item in raw_list
                if (search_query.lower() in item.get("nama_laptop", "").lower() or 
                    search_query.lower() in item.get("manufacturer", "").lower() or
                    search_query.lower() in item.get("nama_processor", "").lower())
            ]

        if processor_filter:
            raw_list = [item for item in raw_list if item.get("nama_processor") == processor_filter]

        if ram_filter:
            try:
                rf_int = int(ram_filter)
                raw_list = [item for item in raw_list if int(item.get("ram_kapasitas", 0) or 0) == rf_int]
            except ValueError:
                pass

        if storage_filter:
            try:
                sf_int = int(storage_filter)
                raw_list = [item for item in raw_list if int(item.get("storage_kapasitas", 0) or 0) == sf_int]
            except ValueError:
                pass

        if min_layar:
            try:
                ml = float(min_layar)
                raw_list = [item for item in raw_list if float(item.get("ukuran_layar", 0) or 0) >= ml]
            except ValueError:
                pass

        if max_layar:
            try:
                xl = float(max_layar)
                raw_list = [item for item in raw_list if float(item.get("ukuran_layar", 0) or 0) <= xl]
            except ValueError:
                pass

        if min_baterai:
            try:
                mb = float(min_baterai)
                raw_list = [item for item in raw_list if float(item.get("baterai", 0) or 0) >= mb]
            except ValueError:
                pass

        if max_baterai:
            try:
                xb = float(max_baterai)
                raw_list = [item for item in raw_list if float(item.get("baterai", 0) or 0) <= xb]
            except ValueError:
                pass

        if min_harga:
            try:
                mh = float(min_harga)
                raw_list = [item for item in raw_list if float(item.get("harga", 0) or 0) >= mh]
            except ValueError:
                pass

        if max_harga:
            try:
                xh = float(max_harga)
                raw_list = [item for item in raw_list if float(item.get("harga", 0) or 0) <= xh]
            except ValueError:
                pass
        
        try:
            per_page = int(request.GET.get('per_page', 10))
            if per_page not in [10, 15, 25]:
                per_page = 10
        except ValueError:
            per_page = 10

        from django.core.paginator import Paginator
        paginator = Paginator(raw_list, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'pengadaan_list': page_obj,
            'search_query': search_query,
            'processor_filter': processor_filter,
            'ram_filter': ram_filter,
            'storage_filter': storage_filter,
            'min_layar': min_layar,
            'max_layar': max_layar,
            'min_baterai': min_baterai,
            'max_baterai': max_baterai,
            'min_harga': min_harga,
            'max_harga': max_harga,
            'all_processors': all_processors,
            'all_ram': all_ram,
            'all_storage': all_storage,
            'total': len(raw_list),
            'per_page': per_page,
        }
        return render(request, 'it/inventori/manajemenpengadaan_it.html', context)
    finally:
        conn.close()

def detailpengadaan_it_view(request):
    laptop_id = request.GET.get('id')
    if not laptop_id:
        messages.error(request, 'ID laptop tidak ditemukan.')
        return redirect('manajemen_pengadaan_it')
        
    conn = get_connection()
    try:
        repo = LaptopPengadaanRepository(conn)
        
        # Handle delete action
        if request.method == 'POST' and request.POST.get('action') == 'hapus':
            try:
                repo.hapus_laptop_pengadaan(laptop_id)
                messages.success(request, 'Data laptop pengadaan berhasil dihapus!')
                return redirect('manajemen_pengadaan_it')
            except Exception as e:
                messages.error(request, f'Gagal menghapus laptop pengadaan: {str(e)}')
                return redirect('manajemen_pengadaan_it')

        laptop = repo.ambil_laptop_pengadaan_by_id(laptop_id)
        if not laptop:
            messages.error(request, 'Laptop pengadaan tidak ditemukan.')
            return redirect('manajemen_pengadaan_it')
            
        laptop['harga_format'] = f"Rp. {laptop.get('harga', 0):,.0f}".replace(",", ".")
        
        context = {
            'laptop': laptop
        }
        return render(request, 'it/inventori/detailpengadaan_it.html', context)
    finally:
        conn.close()

def editpengadaan_it_view(request):
    laptop_id = request.GET.get('id')
    if not laptop_id:
        messages.error(request, 'ID laptop tidak ditemukan.')
        return redirect('manajemen_pengadaan_it')
        
    conn = get_connection()
    try:
        repo = LaptopPengadaanRepository(conn)
        laptop = repo.ambil_laptop_pengadaan_by_id(laptop_id)
        if not laptop:
            messages.error(request, 'Laptop pengadaan tidak ditemukan.')
            return redirect('manajemen_pengadaan_it')
            
        if request.method == 'POST':
            try:
                nama_laptop = request.POST.get('nama_laptop')
                harga = int(request.POST.get('harga', 0))
                gpu = request.POST.get('gpu')
                ukuran_layar = float(request.POST.get('ukuran_layar') or 0.0)
                baterai = float(request.POST.get('baterai') or 0.0)
                berat = float(request.POST.get('berat') or 0.0)
                
                id_processor = request.POST.get('id_processor') or None
                id_ram = request.POST.get('id_ram') or None
                id_storage = request.POST.get('id_storage') or None
                
                from dss.repositories.dto.dto_laptop_pengadaan import LaptopPengadaanDTO
                dto = LaptopPengadaanDTO(
                    id_laptop_pengadaan=laptop_id,
                    nama_laptop=nama_laptop,
                    harga=harga,
                    gpu=gpu,
                    ukuran_layar=ukuran_layar,
                    baterai=baterai,
                    berat=berat,
                    id_processor=id_processor,
                    id_ram=id_ram,
                    id_storage=id_storage
                )
                repo.update_laptop_pengadaan(dto)
                repo.update_spek_pengadaan(dto)
                
                messages.success(request, 'Data laptop pengadaan berhasil diperbarui!')
                return redirect(f"/it/detail-pengadaan/?id={laptop_id}")
            except Exception as e:
                messages.error(request, f'Gagal memperbarui data: {str(e)}')
                
        processors = Processor.objects.all()
        rams = RAM.objects.all()
        storages = Storage.objects.all()
        
        context = {
            'laptop': laptop,
            'processors': processors,
            'rams': rams,
            'storages': storages,
        }
        return render(request, 'it/inventori/editpengadaan_it.html', context)
    finally:
        conn.close()

def tambahpengadaan_it_view(request):
    if request.method == 'POST':
        conn = get_connection()
        try:
            nama_laptop = request.POST.get('nama_laptop')
            gpu = request.POST.get('gpu')
            id_processor = request.POST.get('id_processor')
            id_ram = request.POST.get('id_ram')
            id_storage = request.POST.get('id_storage')
            raw_layar = request.POST.get('ukuran_layar')
            raw_baterai = request.POST.get('baterai')
            raw_berat = request.POST.get('berat')
            raw_harga = request.POST.get('harga')

            if not all([nama_laptop, gpu, id_processor, id_ram, id_storage, raw_layar, raw_baterai, raw_berat, raw_harga]):
                messages.error(request, 'Gagal menambahkan laptop pengadaan: Semua kolom wajib diisi!')
                processors = Processor.objects.all()
                rams = RAM.objects.all()
                storages = Storage.objects.all()
                return render(request, 'it/inventori/tambahpengadaan_it.html', {'processors': processors, 'rams': rams, 'storages': storages})

            harga = int(raw_harga or 0)
            ukuran_layar = float(raw_layar or 0.0)
            baterai = float(raw_baterai or 0.0)
            berat = float(raw_berat or 0.0)
            
            from dss.repositories.dto.dto_laptop_pengadaan import LaptopPengadaanDTO
            dto = LaptopPengadaanDTO(
                nama_laptop=nama_laptop,
                harga=harga,
                gpu=gpu,
                ukuran_layar=ukuran_layar,
                baterai=baterai,
                berat=berat,
                id_processor=id_processor,
                id_ram=id_ram,
                id_storage=id_storage
            )
            repo.tambah_laptop_pengadaan(dto)
            messages.success(request, 'Laptop pengadaan berhasil ditambahkan!')
            return redirect('manajemen_pengadaan_it')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan laptop pengadaan: {str(e)}')
        finally:
            conn.close()
            
    processors = Processor.objects.all()
    rams = RAM.objects.all()
    storages = Storage.objects.all()
    
    context = {
        'processors': processors,
        'rams': rams,
        'storages': storages,
    }
    return render(request, 'it/inventori/tambahpengadaan_it.html', context)

# ==========================================
# 3. TALENT VIEWS
# ==========================================

def dashboard_talent_view(request):
    try:
        id_user = None
        if hasattr(request.user, 'id_user') and request.user.id_user:
            id_user = request.user.id_user
        elif hasattr(request.user, 'username') and request.user.username:
            id_user = request.user.username
        else:
            id_user = 'USR_0021'
        
        service_pengajuan = PengajuanService()
        semua_pengajuan = service_pengajuan.service_ambil_semua_pengajuan()
        if id_user:
            semua_pengajuan = [p for p in semua_pengajuan if str(getattr(p, 'id_user', '')).strip() == str(id_user).strip()]
            
        total_menunggu = sum(1 for p in semua_pengajuan if p.status and p.status.lower() in ['menunggu', 'pending'])
        total_ditolak = sum(1 for p in semua_pengajuan if p.status and p.status.lower() in ['ditolak', 'rejected'])
        total_disetujui = sum(1 for p in semua_pengajuan if p.status and p.status.lower() in ['disetujui', 'approved'])
        
        service_peminjaman = PeminjamanService()
        semua_peminjaman = service_peminjaman.service_ambil_semua_peminjaman()
        if id_user:
            semua_peminjaman = [p for p in semua_peminjaman if str(getattr(p, 'id_user', '')).strip() == str(id_user).strip()]
            
        total_selesai = sum(1 for p in semua_peminjaman if p.status and p.status.lower() in ['selesai', 'dikembalikan'])
        
        import datetime as _dt
        semua_pengajuan.sort(key=lambda x: x.tanggal_pengajuan if x.tanggal_pengajuan else _dt.date.min, reverse=True)
        recent_pengajuan = semua_pengajuan

        from inventori.models import Proyek, Peminjaman
        for p in recent_pengajuan:
            if getattr(p, 'id_proyek', None):
                pr_obj = Proyek.objects.filter(id_proyek=p.id_proyek).first()
                p.nama_proyek = pr_obj.nama_proyek if pr_obj else p.id_proyek
            else:
                p.nama_proyek = "-"

            pm_obj = Peminjaman.objects.filter(id_pengajuan=p.id_pengajuan).select_related('id_laptop_inventori').first()
            p.laptop_dipakai = pm_obj.id_laptop_inventori if pm_obj else None
        
        # Build comprehensive notifications for pengajuan & peminjaman
        notifikasi_talent = []
        
        for p in semua_pengajuan:
            st = (p.status or '').lower()
            tgl_str = p.tanggal_pengajuan.strftime("%d %b %Y, %H:%i") if hasattr(p, 'tanggal_pengajuan') and p.tanggal_pengajuan else "Baru saja"
            if hasattr(p.tanggal_pengajuan, 'strftime'):
                tgl_str = p.tanggal_pengajuan.strftime("%d %b %Y")
            
            if st in ['disetujui', 'approved']:
                notifikasi_talent.append({
                    'pesan': f"Pengajuan ({p.id_pengajuan}) untuk role {p.kebutuhan_role} telah DISETUJUI oleh HC.",
                    'waktu': tgl_str,
                    'status': 'disetujui',
                    'status_text': 'Disetujui'
                })
            elif st in ['ditolak', 'rejected']:
                ket = f" Alasan: {p.keterangan}" if p.keterangan else ""
                notifikasi_talent.append({
                    'pesan': f"Pengajuan ({p.id_pengajuan}) untuk role {p.kebutuhan_role} DITOLAK.{ket}",
                    'waktu': tgl_str,
                    'status': 'ditolak',
                    'status_text': 'Ditolak'
                })
            else:
                notifikasi_talent.append({
                    'pesan': f"Pengajuan ({p.id_pengajuan}) untuk role {p.kebutuhan_role} sedang MENUNGGU persetujuan HC.",
                    'waktu': tgl_str,
                    'status': 'menunggu',
                    'status_text': 'Menunggu'
                })

        for pm in semua_peminjaman:
            st_pm = (pm.status or '').lower()
            tgl_pm = pm.tanggal_pinjam.strftime("%d %b %Y") if hasattr(pm, 'tanggal_pinjam') and pm.tanggal_pinjam else "Baru saja"
            if st_pm in ['dipinjam', 'aktif']:
                notifikasi_talent.append({
                    'pesan': f"Laptop ({pm.id_laptop_inventori}) telah berhasil Anda PINJAM.",
                    'waktu': tgl_pm,
                    'status': 'disetujui',
                    'status_text': 'Dipinjam'
                })
            elif st_pm in ['selesai', 'dikembalikan']:
                notifikasi_talent.append({
                    'pesan': f"Peminjaman laptop ({pm.id_laptop_inventori}) telah SELESAI dikembalikan.",
                    'waktu': tgl_pm,
                    'status': 'disetujui',
                    'status_text': 'Selesai'
                })

        # Ambil maksimal 5 notifikasi terbaru
        notifikasi_talent = notifikasi_talent[:5]

        context = {
            'total_menunggu': total_menunggu,
            'total_ditolak': total_ditolak,
            'total_disetujui': total_disetujui,
            'total_selesai': total_selesai,
            'recent_pengajuan': recent_pengajuan,
            'notifikasi_talent': notifikasi_talent
        }
    except Exception as e:
        context = {
            'error_message': str(e),
            'total_menunggu': 0,
            'total_ditolak': 0,
            'total_disetujui': 0,
            'total_selesai': 0,
            'recent_pengajuan': []
        }
    return render(request, 'talent/dashboard/dashboard_talent.html', context)
def pengajuanlaptop_talent_view(request):
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    try:
        service = PengajuanService()

        # Ambil user id
        id_user = request.POST.get('id_user')

        if not id_user:
            if hasattr(request.user, 'id_user') and request.user.id_user:
                id_user = request.user.id_user
            elif hasattr(request.user, 'username') and request.user.username:
                id_user = request.user.username
            else:
                id_user = 'USR_0021'

        from inventori.models import User, Proyek, ProjectRole, Role, RoleTeknologi
        user_obj = None
        if id_user:
            user_obj = User.objects.filter(id_user=id_user).first()
        
        user_departemen = user_obj.departemen if user_obj else 'IT'

        if request.method == 'POST':
            from datetime import datetime

            departemen = user_departemen
            is_tech_role = user_departemen in ['IT', 'Outsourcing', 'Talent'] or (user_obj and str(user_obj.role).upper() in ['TALENT', 'IT'])
            if is_tech_role:
                role = request.POST.get('role') or 'Unknown'
                spesifikasi = request.POST.get('spesifikasi') or '-'
            else:
                role = 'Non-IT'
                spesifikasi = '-'
            alasan = request.POST.get('alasan') or '-'
            tanggal_dibutuhkan = request.POST.get('tanggal_dibutuhkan')
            
            keterangan_full = alasan
            if tanggal_dibutuhkan:
                keterangan_full = f"{alasan} (Target Dibutuhkan: {tanggal_dibutuhkan})"

            # Validate double booking (maksimal 1 laptop aktif dipinjam)
            from inventori.services.service_peminjaman import PeminjamanService
            p_service = PeminjamanService()
            all_peminjaman = p_service.service_ambil_semua_peminjaman()
            has_active_borrow = any(
                str(p.id_user) == str(id_user) and p.status and p.status.lower() in ['dipinjam', 'aktif']
                for p in all_peminjaman
            )
            if has_active_borrow:
                messages.error(request, 'Gagal mengajukan: Anda masih meminjam laptop aktif.')
                return redirect('pengajuanlaptop_talent')

            proyek_id = request.POST.get('proyek') or None
            
            # Parse tanggal_dibutuhkan ke bulan/date jika ada
            tgl_kebutuhan_obj = datetime.now().date()
            if tanggal_dibutuhkan:
                try:
                    tgl_kebutuhan_obj = datetime.strptime(tanggal_dibutuhkan, "%Y-%m-%d").date()
                except Exception:
                    pass

            dto = PengajuanDTO(
                id_user=id_user,
                kebutuhan_role=role,
                kebutuhan_requirement=spesifikasi,
                bulan=tgl_kebutuhan_obj,
                keterangan=keterangan_full,
                perusahaan=departemen,
                status='menunggu',
                id_proyek=proyek_id
            )

            service.service_tambah_pengajuan(dto)
            messages.success(request, 'Pengajuan laptop berhasil dikirim dan sedang menunggu persetujuan.')
            return redirect('pengajuanlaptop_talent')

        semua_pengajuan = service.service_ambil_semua_pengajuan()

        if id_user:
            semua_pengajuan = [
                p for p in semua_pengajuan
                if getattr(p, 'id_user', None) == id_user
            ]

        # Filter search
        if search_query:
            q_lower = search_query.lower()
            semua_pengajuan = [
                p for p in semua_pengajuan
                if q_lower in getattr(p, 'kebutuhan_role', '').lower() or
                   q_lower in getattr(p, 'kebutuhan_requirement', '').lower() or
                   q_lower in str(getattr(p, 'id_pengajuan', '')).lower()
            ]

        # Filter status
        if status_filter:
            status_lower = status_filter.lower()
            semua_pengajuan = [
                p for p in semua_pengajuan
                if getattr(p, 'status', '').lower() == status_lower
            ]

        try:
            per_page = int(request.GET.get('per_page', 10))
            if per_page not in [10, 15, 25]:
                per_page = 10
        except ValueError:
            per_page = 10

        import datetime as dt
        semua_pengajuan.sort(
            key=lambda x: x.tanggal_pengajuan if x.tanggal_pengajuan else dt.date.min,
            reverse=True
        )

        from django.core.paginator import Paginator
        paginator = Paginator(semua_pengajuan, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        projects = Proyek.objects.all()
        project_roles_map = {}
        for pr in ProjectRole.objects.select_related('proyek', 'role'):
            proj_id = pr.proyek.id_proyek
            if proj_id not in project_roles_map:
                project_roles_map[proj_id] = []
            project_roles_map[proj_id].append({
                'id_role': pr.role.id_role,
                'nama_role': pr.role.nama_role,
            })

        role_technologies_map = {}
        for rt in RoleTeknologi.objects.select_related('role', 'teknologi'):
            r_name = rt.role.nama_role
            if r_name not in role_technologies_map:
                role_technologies_map[r_name] = []
            role_technologies_map[r_name].append({
                'id_teknologi': rt.teknologi.id_teknologi,
                'nama_teknologi': rt.teknologi.nama_teknologi,
            })

        from datetime import datetime
        today_str = datetime.now().strftime('%Y-%m-%d')

        context = {
            'list_pengajuan': page_obj,
            'total_pengajuan': len(semua_pengajuan),
            'search_query': search_query,
            'status_filter': status_filter,
            'user_departemen': user_departemen,
            'projects': projects,
            'project_roles_map': project_roles_map,
            'role_technologies_map': role_technologies_map,
        }

        return render(
            request,
            'talent/inventori/pengajuanlaptop_talent.html',
            context
        )

    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
        context = {
            'list_pengajuan': [],
            'total_pengajuan': 0,
            'search_query': search_query,
            'status_filter': status_filter,
            'user_departemen': 'Non IT',
        }
        return render(
            request,
            'talent/inventori/pengajuanlaptop_talent.html',
            context
        )

def detaillaptop_talent_view(request):
    id_user = request.user.id_user if hasattr(request.user, 'id_user') else None
    service = PeminjamanService()
    active_laptop = None
    riwayat_peminjaman = []
    try:
        riwayat_list = service.service_ambil_semua_peminjaman()
        if id_user:
            riwayat_list = [p for p in riwayat_list if str(getattr(p, 'id_user', '')).strip() == str(id_user).strip()]
        
        active_peminjaman = next((r for r in riwayat_list if r.status and r.status.lower() in ['dipinjam', 'aktif', 'ready', 'dikembalikan']), None)
        if active_peminjaman:
            lap_id = getattr(active_peminjaman, 'id_laptop_inventori', None)
            if hasattr(lap_id, 'id_laptop_inventori'):
                lap_id = lap_id.id_laptop_inventori
            active_laptop = LaptopInventori.objects.select_related('id_processor', 'id_ram', 'id_storage').filter(id_laptop_inventori=str(lap_id)).first()
            if active_laptop:
                from inventori.models import Peminjaman
                riwayat_peminjaman = Peminjaman.objects.filter(
                    id_laptop_inventori_id=active_laptop.id_laptop_inventori
                ).select_related('id_user', 'id_pengajuan').order_by('-tanggal_pinjam')
                for p in riwayat_peminjaman:
                    p.user_nama = p.id_user.nama if p.id_user else '-'
                    p.user_role = p.id_user.role if p.id_user else '-'
    except Exception as e:
        messages.error(request, f'Gagal memuat detail laptop: {str(e)}')

    context = {
        'laptop': active_laptop,
        'riwayat_peminjaman': riwayat_peminjaman,
    }
    return render(request, 'talent/inventori/detaillaptop_talent.html', context)

def riwayatpeminjamanlaptop_talent_view(request):
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    try:
        per_page = int(request.GET.get('per_page', 10))
        if per_page not in [10, 15, 25]:
            per_page = 10
    except ValueError:
        per_page = 10

    try:
        id_user = None
        if hasattr(request.user, 'id_user') and request.user.id_user:
            id_user = request.user.id_user
        elif hasattr(request.user, 'username') and request.user.username:
            id_user = request.user.username
        else:
            id_user = 'USR_0021'
            
        service = PeminjamanService()
        riwayat_list = service.service_ambil_semua_peminjaman()
        
        if id_user:
            riwayat_list = [p for p in riwayat_list if str(getattr(p, 'id_user', '')).strip() == str(id_user).strip()]
            
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
                
            from datetime import date
            if p.tanggal_pinjam:
                if p.tanggal_kembali:
                    p.durasi_hari = (p.tanggal_kembali - p.tanggal_pinjam).days
                else:
                    p.durasi_hari = (date.today() - p.tanggal_pinjam).days
            else:
                p.durasi_hari = 0

        active_peminjaman = next((r for r in riwayat_list if r.status and r.status.lower() in ['dipinjam', 'aktif']), None)
        active_laptop = None
        active_jatuh_tempo = None
        active_sisa_hari = None
        if active_peminjaman:
            active_laptop = LaptopInventori.objects.filter(id_laptop_inventori=active_peminjaman.id_laptop_inventori).first()
            # Ambil jatuh_tempo dari DB (TC-TRX-17)
            from inventori.models import Peminjaman as PeminjamanModel
            import datetime as _dt
            try:
                db_pem = PeminjamanModel.objects.get(id_peminjaman=active_peminjaman.id_peminjaman)
                active_jatuh_tempo = db_pem.tanggal_jatuh_tempo
                if active_jatuh_tempo:
                    active_sisa_hari = (active_jatuh_tempo - _dt.date.today()).days
            except Exception:
                pass

        # Filter search
        if search_query:
            q_lower = search_query.lower()
            riwayat_list = [
                p for p in riwayat_list
                if q_lower in getattr(p, 'nama_laptop', '').lower() or
                   q_lower in str(getattr(p, 'id_peminjaman', '')).lower() or
                   q_lower in getattr(p, 'no_inventori', '').lower()
            ]

        # Filter status
        if status_filter:
            status_lower = status_filter.lower()
            riwayat_list = [
                p for p in riwayat_list
                if getattr(p, 'status', '').lower() == status_lower
            ]

        try:
            per_page = int(request.GET.get('per_page', 10))
            if per_page not in [10, 15, 25]:
                per_page = 10
        except ValueError:
            per_page = 10

        from django.core.paginator import Paginator
        paginator = Paginator(riwayat_list, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
            
        context = {
            'riwayat_list': page_obj,
            'total_peminjaman': total_peminjaman,
            'total_aktif': total_aktif,
            'total_selesai': total_selesai,
            'active_peminjaman': active_peminjaman,
            'active_laptop': active_laptop,
            'active_jatuh_tempo': active_jatuh_tempo,
            'active_sisa_hari': active_sisa_hari,
            'search_query': search_query,
            'status_filter': status_filter,
            'per_page': per_page,
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
            'search_query': search_query,
            'status_filter': status_filter,
        }
    return render(request, 'talent/inventori/riwayatpeminjamanlaptop_talent.html', context)

def pengembalianlaptop_talent_view(request):
    from inventori.models import Peminjaman, LaptopInventori
    id_user = request.user.id_user if hasattr(request.user, 'id_user') else None
    if not id_user:
        messages.error(request, 'Anda harus login terlebih dahulu.')
        return redirect('riwayatpeminjamanlaptop_talent')

    service = PeminjamanService()
    try:
        riwayat_list = service.service_ambil_semua_peminjaman()
        if id_user:
            riwayat_list = [p for p in riwayat_list if str(getattr(p, 'id_user', '')).strip() == str(id_user).strip()]
        
        # Check active or pending return loans
        active_peminjaman = next((r for r in riwayat_list if r.status and str(r.status).lower() in ['dipinjam', 'aktif', 'ready', 'dikembalikan']), None)
        
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
                db_kondisi = 'rusak ringan'
            else:
                db_kondisi = 'rusak berat'
                
            from datetime import datetime
            import datetime as dt
            
            # Update Peminjaman menjadi dikembalikan
            jadwal = request.POST.get('jadwal')
            if jadwal:
                parsed_jadwal = datetime.strptime(jadwal, '%Y-%m-%d').date()
                if parsed_jadwal < dt.date.today():
                    messages.error(request, 'Gagal memproses pengembalian: Tanggal jadwal penyerahan tidak boleh sebelum hari ini.')
                    return redirect('pengembalianlaptop_talent')
            
            peminjaman = Peminjaman.objects.filter(id_peminjaman=active_peminjaman.id_peminjaman).first()
            if peminjaman:
                peminjaman.status = 'dikembalikan'
                peminjaman.keterangan = f"{alasan} - {catatan}"
                if jadwal:
                    peminjaman.tanggal_kembali = datetime.strptime(jadwal, '%Y-%m-%d').date()
                else:
                    peminjaman.tanggal_kembali = datetime.now().date()
                peminjaman.save()
                
                # Update kondisi fisik laptop langsung
                lap_id_str = getattr(active_peminjaman, 'id_laptop_inventori', None)
                if hasattr(lap_id_str, 'id_laptop_inventori'):
                    lap_id_str = lap_id_str.id_laptop_inventori
                laptop = LaptopInventori.objects.filter(id_laptop_inventori=str(lap_id_str)).first()
                if laptop:
                    laptop.kondisi = db_kondisi
                    laptop.save()
            
            messages.success(request, 'Pengembalian laptop berhasil disubmit. Menunggu konfirmasi HC.')
            return redirect('riwayatpeminjamanlaptop_talent')
            
        if not active_peminjaman:
            messages.error(request, 'Anda tidak memiliki perangkat aktif yang perlu dikembalikan.')
            return redirect('riwayatpeminjamanlaptop_talent')
            
        lap_id_str = getattr(active_peminjaman, 'id_laptop_inventori', None)
        if hasattr(lap_id_str, 'id_laptop_inventori'):
            lap_id_str = lap_id_str.id_laptop_inventori
        active_laptop = LaptopInventori.objects.filter(id_laptop_inventori=str(lap_id_str)).first()
        
        # Ambil data dari DB untuk jatuh_tempo yang sudah tersimpan (TC-TRX-17)
        peminjaman_db = Peminjaman.objects.filter(id_peminjaman=active_peminjaman.id_peminjaman).first()
        
        import datetime as _dt
        today = _dt.date.today()
        durasi_aktif = None
        sisa_jatuh_tempo = None
        if active_peminjaman and active_peminjaman.tanggal_pinjam:
            durasi_aktif = (today - active_peminjaman.tanggal_pinjam).days
        if peminjaman_db and peminjaman_db.tanggal_jatuh_tempo:
            sisa_jatuh_tempo = (peminjaman_db.tanggal_jatuh_tempo - today).days
        
        context = {
            'active_peminjaman': active_peminjaman,
            'active_laptop': active_laptop,
            'peminjaman_db': peminjaman_db,
            'durasi_aktif': durasi_aktif,
            'sisa_jatuh_tempo': sisa_jatuh_tempo,
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
    role = str(getattr(request.user, 'role', '')).upper()
    if 'HC' in role:
        return redirect('dashboard_hc')
    elif 'IT' in role:
        return redirect('dashboard_it')
    else:
        return redirect('dashboard_talent')

def home_view(request):
    return login_redirect_view(request)

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')




def setujui_pengajuan_it_view(request):
    from inventori.models import LaptopInventori
    from inventori.services.service_pengajuan import PengajuanService
    from inventori.repositories.dto.dto_pengajuan import PengajuanDTO
    from inventori.repositories.dto.dto_peminjaman import PeminjamanDTO
    import datetime
    import time

    pengajuan_id = request.GET.get('id')
    if not pengajuan_id:
        messages.error(request, 'ID Pengajuan tidak diberikan.')
        return redirect('pengajuanlaptop_it')

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
                return redirect('pengajuanlaptop_it')

            # Buat DTO Pengajuan
            id_user = request.user.id_user if (hasattr(request.user, 'id_user') and request.user.id_user) else 'USR-002'
            dto_peng = PengajuanDTO(
                id_pengajuan=pengajuan_id,
                status='approved',
                approved_by=id_user
            )

            # Buat DTO Peminjaman
            id_peminjaman = f"PMJ-{int(time.time())}"
            dto_pem = PeminjamanDTO(
                id_peminjaman=id_peminjaman,
                id_pengajuan=pengajuan_id,
                id_user=pengajuan.id_user,
                id_laptop_inventori=laptop_id,
                tanggal_pinjam=datetime.date.today().strftime('%Y-%m-%d'),
                status='dipinjam',
                keterangan='Persetujuan pengajuan laptop oleh IT'
            )

            # Eksekusi
            service.service_approve_dan_pinjam(dto_peng, dto_pem)

            # Update Peminjaman status to 'ready'
            peminjaman = Peminjaman.objects.filter(id_pengajuan=pengajuan_id).first()
            if peminjaman:
                peminjaman.status = 'ready'
                peminjaman.save()

            messages.success(request, 'Pengajuan berhasil disetujui oleh IT dan laptop siap diambil oleh Talent.')
            return redirect('pengajuanlaptop_it')
        except Exception as e:
            messages.error(request, f'Gagal menyetujui pengajuan: {str(e)}')
            return redirect(f"{request.path}?id={pengajuan_id}")

    # GET Request: Fetch and Map Laptop Specifications
    from inventori.models import Peminjaman
    # Exclude laptops that have an active loan (assigned)
    active_laptop_ids = Peminjaman.objects.filter(status__in=['dipinjam', 'aktif', 'dikembalikan']).values_list('id_laptop_inventori', flat=True)
    laptops = LaptopInventori.objects.filter(status__in=['tersedia', 'Available', 'Tersedia']).exclude(id_laptop_inventori__in=active_laptop_ids).select_related('id_processor', 'id_ram', 'id_storage')
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

    return render(request, 'it/inventori/setujuipengajuan_it.html', {
        'pengajuan_id': pengajuan_id,
        'laptops': laptops
    })
def manajemenproyek_it_view(request):
    from inventori.models import Proyek
    from django.core.paginator import Paginator
    from django.db.models import Q


    search_query = request.GET.get('q', '')
    proyek_list = Proyek.objects.prefetch_related(
        'roles__role__teknologi_role__teknologi'
    )

    if search_query:
        proyek_list = proyek_list.filter(Q(nama_proyek__icontains=search_query))

    proyek_list = proyek_list.order_by('id_proyek')

    try:
        per_page = int(request.GET.get('per_page', 10))
        if per_page not in [10, 15, 25]:
            per_page = 10
    except ValueError:
        per_page = 10

    paginator = Paginator(proyek_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "proyek_list": page_obj,
        "search_query": search_query,
        "per_page": per_page,
    }
    return render(
        request,
        "it/inventori/manajemenproyek_it.html",
        context
    )
def tambahproyek_it_view(request):
    conn = get_connection()
    proyek_repo = ProyekRepository(conn)
    projectrole_repo = ProjectRoleRepository(conn)
    service_proyek = ProyekService(proyek_repo,conn)
    service_projectrole = ProjectRoleService(projectrole_repo,conn)
    if request.method == "POST":
        print(request.POST)
        try:
            proyek_data = ProyekDTO(
                nama_proyek=request.POST.get("nama_proyek"),
                user_perusahaan=request.POST.get("user_perusahaan"),
                mulai_proyek=request.POST.get("mulai_proyek"),
                akhir_proyek=request.POST.get("akhir_proyek")
            )
            role_ids = request.POST.getlist("role_ids[]")

            if len(role_ids) != len(set(role_ids)):
                raise Exception(
                    "Role yang sama tidak boleh dipilih lebih dari satu kali dalam satu proyek."
                )
            with transaction.atomic():
                result = (service_proyek.tambah_proyek(proyek_data))
                
                print("HASIL SERVICE:")
                print(result)
                print("TYPE RESULT:")
                print(type(result))
                print("ID PROYEK:")
                print(result["id_proyek"])
                print("TYPE ID:")
                print(type(result["id_proyek"]))
                
                id_proyek = (result["id_proyek"])
                for role_id in role_ids:

                    (
                        service_projectrole
                        .tambah_projectrole(
                            ProjectRoleDTO(
                                id_proyek=id_proyek,
                                id_role=role_id
                            )
                        )
                    )
                messages.success(request,"Proyek berhasil ditambahkan")
                return redirect("manajemen_proyek_it")

        except Exception as e:
            traceback.print_exc()
            print("ERROR:",str(e))
            messages.error(request,str(e))

    role_list = (Role.objects
        .all()
        .order_by("nama_role")
    )
    role_data = []
    for role in role_list:
        teknologi = []
        rels = (
            RoleTeknologi.objects
            .select_related("teknologi")
            .filter(role=role)
        )
        for rel in rels:
            teknologi.append({
                "id":rel.teknologi.id_teknologi,
                "nama":rel.teknologi.nama_teknologi
            })

        role_data.append({
            "id": role.id_role,
            "nama": role.nama_role,
            "teknologi": teknologi
        })
    context = {"role_list": role_list,"role_data_json": role_data}
    return render(request,"it/inventori/tambahproyek_it.html",context)
                
def editproyek_it_view(request,id_proyek):
    conn = get_connection()
    proyek_repo = ProyekRepository(conn)
    service_proyek = ProyekService(proyek_repo,conn)
    project_role_repo = (ProjectRoleRepository(conn))
    project_role_service = (ProjectRoleService(project_role_repo,conn))

    # try:
    #     proyek = (proyek_repo.ambil_by_id_full_proyek(id_proyek))
    #     if not proyek:
    #         messages.error(request,"Proyek tidak ditemukan.")
    #         return redirect("manajemen_proyek_it")

    # except Exception as e:
    #     messages.error(request,str(e))
    #     return redirect("manajemen_proyek_it")

    if request.method == "POST":
        try:
            proyek_data = ProyekDTO(
                id_proyek=id_proyek,
                nama_proyek=request.POST.get("nama_proyek"),
                user_perusahaan=request.POST.get("user_perusahaan"),
                mulai_proyek=request.POST.get("mulai_proyek"),
                akhir_proyek=request.POST.get("akhir_proyek")
            )
            role_ids = request.POST.getlist("role_ids[]")
            print("\n=== UPDATE PROYEK ===")
            print("PROJECT :", id_proyek)
            print("ROLE IDS :", role_ids)
            service_proyek.update_proyek(proyek_data)
            project_role_repo.hapus_by_project(id_proyek)
            
            for role_id in role_ids:
                print(f"Tambah role {role_id}")
                project_role_service.tambah_projectrole(ProjectRoleDTO(id_proyek=id_proyek,id_role=role_id))
            conn.commit()
            messages.success(
                request,
                f'Proyek "{proyek_data.nama_proyek}" berhasil diperbarui!'
            )
            return redirect("manajemen_proyek_it")

        except Exception as e:
            conn.rollback()
            traceback.print_exc()
            messages.error(
                request,
                str(e)
            )
            
    proyek = (proyek_repo.ambil_by_id_full_proyek(id_proyek))
    role_list = (proyek_repo.ambil_role_proyek(id_proyek))
    role_repo = RoleRepository(conn)
    all_roles = role_repo.get_all()
    print("\n=== ALL ROLES ===")
    for role in all_roles:
        print(role)
    context = {
        "proyek": proyek,
        "role_list": role_list,
        "all_roles": all_roles
    }
    return render(request,"it/inventori/editproyek_it.html",context)

def hapusproyek_it_view(
    request,
    id_proyek
):

    conn = get_connection()
    proyek_repo = (ProyekRepository(conn))
    service_proyek = (ProyekService(proyek_repo,conn))
    if request.method == "POST":
        try:
            proyek = (proyek_repo.ambil_by_id(id_proyek))
            if not proyek:
                messages.error(request,"Proyek tidak ditemukan.")
                return redirect("manajemen_proyek_it" )
            nama_proyek = (proyek["nama_proyek"])
            (
                service_proyek
                .hapus_proyek(
                    id_proyek
                )
            )
            messages.success(request,f'Proyek "{nama_proyek}" berhasil dihapus!')

        except Exception as e:
            traceback.print_exc()
            messages.error(request,str(e))
    return redirect("manajemen_proyek_it")

def tambah_komponen_it_view(request):
    from inventori.models import Processor, RAM, Storage
    
    if request.method == 'POST':
        comp_type = request.POST.get('component_type')
        try:
            if comp_type == 'processor':
                Processor.objects.create(
                    nama_processor=request.POST.get('nama_processor'),
                    manufacturer=request.POST.get('manufacturer'),
                    model=request.POST.get('model'),
                    cores=int(request.POST.get('cores') or 0),
                    threads=int(request.POST.get('threads') or 0),
                    base_clock=float(request.POST.get('base_clock') or 0.0),
                    max_clock=float(request.POST.get('max_clock') or 0.0),
                    arsitektur=request.POST.get('arsitektur', ''),
                    keterangan=request.POST.get('keterangan', '')
                )
                messages.success(request, 'Processor berhasil ditambahkan!')
            elif comp_type == 'ram':
                RAM.objects.create(
                    kapasitas_gb=int(request.POST.get('kapasitas_gb') or 0),
                    tipe=request.POST.get('tipe', ''),
                    keterangan=request.POST.get('keterangan', '')
                )
                messages.success(request, 'RAM berhasil ditambahkan!')
            elif comp_type == 'storage':
                Storage.objects.create(
                    kapasitas_gb=int(request.POST.get('kapasitas_gb') or 0),
                    tipe=request.POST.get('tipe', '')
                )
                messages.success(request, 'Storage berhasil ditambahkan!')
            return redirect('tambah_komponen_it')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan komponen: {str(e)}')
            return redirect('tambah_komponen_it')

    processors = Processor.objects.all().order_by('-id_processor')[:10]
    rams = RAM.objects.all().order_by('-id_ram')[:10]
    storages = Storage.objects.all().order_by('-id_storage')[:10]

    return render(request, 'it/inventori/tambah_komponen_it.html', {
        'processors': processors,
        'rams': rams,
        'storages': storages,
    })

def manajemen_role_teknologi_it_view(request):
    from django.core.paginator import Paginator
    from django.db.models import Q
    processor_service = ReadProcessorService()
    processor_list = (processor_service.ambil_processor_dropdown())
    search_role = request.GET.get('q_role', '')
    search_tech = request.GET.get('q_tech', '')
    role_list = (Role.objects.prefetch_related('teknologi_role__teknologi').order_by('nama_role'))
    teknologi_list = (Teknologi.objects.order_by('nama_teknologi'))
    if search_role:
        role_list = role_list.filter(Q(nama_role__icontains=search_role))
    if search_tech:
        teknologi_list = teknologi_list.filter(Q(nama_teknologi__icontains=search_tech) | Q(kategori__icontains=search_tech))
    try:
        per_page = int(request.GET.get('per_page', 10))
        if per_page not in [10, 15, 25]:
            per_page = 10
    except ValueError:
        per_page = 10

    paginator_role = Paginator(role_list, per_page)
    page_role = request.GET.get('page_role')
    role_obj = paginator_role.get_page(page_role)
    paginator_tech = Paginator(teknologi_list, per_page)
    page_tech = request.GET.get('page_tech')
    tech_obj = paginator_tech.get_page(page_tech)
    active_tab = request.GET.get('tab', 'role')
    context = {
        "role_list": role_obj,
        "tech_page": tech_obj,
        "teknologi_list": tech_obj,
        "processor_list": processor_list,
        "search_role": search_role,
        "search_tech": search_tech,
        "per_page": per_page,
        "active_tab": active_tab,
    }
    return render(request,"it/inventori/manajemenroleteknologi_it.html", context)
def tambah_teknologi_it_view(request):
    conn = get_connection()
    repo = TeknologiRepository(conn)
    service = TeknologiService(repo,conn)
    if request.method == "POST":
        try:
            data = TeknologiDTO(
                nama_teknologi=request.POST.get("nama_teknologi"),
                kategori=request.POST.get("kategori")
            )
            service.tambah(data)
            messages.success(request,"Teknologi berhasil ditambahkan.")
        except Exception as e:
            traceback.print_exc()
            messages.error(request,str(e))
    return redirect("manajemenroleteknologi_it")

def tambah_role_it_view(request):
    from django.shortcuts import redirect
    from django.contrib import messages
    import uuid
    import traceback
    from  inventori.repositories.repositori_role_teknologi import RoleTeknologiRepository
    conn = get_connection()
    role_repo = RoleRepository(conn)
    repo_bobot = BobotKriteriaRepository(conn)
    role_service = RoleService(role_repo,conn,repo_bobot)
    role_teknologi_repo = (RoleTeknologiRepository(conn))
    role_teknologi_service = (RoleTeknologiService(role_teknologi_repo,conn))

    if request.method == "POST":

        try:
            print("\n===================================")
            print("MULAI TAMBAH ROLE")
            print("===================================")
            print("\nPOST DATA:")
            print(dict(request.POST))
            nama_role = request.POST.get("nama_role", "").strip()
            if Role.objects.filter(nama_role__iexact=nama_role).exists():
                messages.error(request, f"Role dengan nama '{nama_role}' sudah ada.")
                return redirect("manajemenroleteknologi_it")

            # ==========================
            # CREATE ROLE
            # ==========================
            id_processor = request.POST.get("id_processor")
            processor_service = ReadProcessorService()
            processor = (processor_service.ambil_by_id(id_processor))
            print("PROCESSOR:")
            print(processor)
            print(type(processor))
            role_dto = RoleDTO(
                nama_role=request.POST.get("nama_role"),
                min_ram=int(request.POST.get("min_ram",0)),
                min_storage=int(request.POST.get("min_storage",0)),
                nama_processor=processor["nama_processor"],
                min_processor_score=int(request.POST.get("min_processor_score"))
            )
            id_role = (role_service.tambah_role(role_dto))
            teknologi_ids = (request.POST.getlist("teknologi"))
            service_bobot = (ServiceBobotKriteria(conn))
            KRITERIA_MAPPING = {
                "processor":"KRIT_0001",
                "ram":"KRIT_0002",
                "storage":"KRIT_0003",
                "berat":"KRIT_0004",
                "layar":"KRIT_0005",
                "baterai":"KRIT_0006"
            }
            list_role_teknologi = []
            for teknologi_id in teknologi_ids:
                dto_role_teknologi = (RoleTeknologiDTO(id_role= id_role,id_teknologi= teknologi_id))
                id_role_teknologi = (role_teknologi_service.tambah(dto_role_teknologi))
                list_role_teknologi.append(id_role_teknologi)
                
                processor = request.POST.get(f"processor_weight_{teknologi_id}")
                ram = request.POST.get(f"ram_weight_{teknologi_id}")
                storage = request.POST.get(f"storage_weight_{teknologi_id}")
                berat = request.POST.get(f"berat_weight_{teknologi_id}")
                layar = request.POST.get(f"layar_weight_{teknologi_id}")
                baterai = request.POST.get(f"baterai_weight_{teknologi_id}")
                # ----------------------
                # LIST BOBOT
                # ----------------------

                list_bobot = [
                    {
                        "id_kriteria":KRITERIA_MAPPING["processor"],
                        "nilai_bobot":float(processor or 0)
                    },
                    {
                        "id_kriteria":KRITERIA_MAPPING["ram"],
                        "nilai_bobot":float(ram or 0)
                    },
                    {
                        "id_kriteria":KRITERIA_MAPPING["storage"],
                        "nilai_bobot":float(storage or 0)
                    },
                    {
                        "id_kriteria":KRITERIA_MAPPING["berat"],
                        "nilai_bobot":float(berat or 0)
                    },
                    {
                        "id_kriteria":KRITERIA_MAPPING["layar"],
                        "nilai_bobot":float(layar or 0)
                    },
                    {
                        "id_kriteria":KRITERIA_MAPPING["baterai"],
                        "nilai_bobot":float(baterai or 0)
                    }
                ]
                # ----------------------
                # SAVE BOBOT
                # ----------------------
                print("ROLETEK CREATED:",id_role_teknologi)
                result = (service_bobot.input_bobot_role_teknologi(id_role_teknologi,list_bobot))
                print(result)

                if (result["status"]!="success"):
                    raise Exception(result["message"])
            # ==========================
            # PROSES SWARA
            # ==========================
            service_swara = (ServiceSwara(conn))

            for id_role_teknologi in list_role_teknologi:
                print("PROSES SWARA:",id_role_teknologi)
                hasil_swara = (service_swara.proses_swara_role_teknologi(id_role_teknologi))
                if (
                    hasil_swara["status"]
                    != "success"
                ):
                    raise Exception(
                        hasil_swara["message"]
                    )
            if (hasil_swara["status"]!="success"):
                raise Exception(hasil_swara["message"])
            messages.success(request,"Role berhasil ditambahkan.")
        except Exception as e:
            traceback.print_exc()
            print("\nERROR:",str(e))
            messages.error(request,str(e))

    return redirect(
        "manajemenroleteknologi_it"
    )

def hapus_role_it_view(request,id_role):
    conn = get_connection()
    role_repo = (RoleRepository(conn))
    repo_bobot = (BobotKriteriaRepository(conn))
    role_service = (RoleService(role_repo,conn,repo_bobot))
    try:

        role_service.hapus_role(
            id_role
        )

        messages.success(
            request,
            "Role berhasil dihapus."
        )

    except Exception as e:

        messages.error(
            request,
            str(e)
        )

    return redirect(
        "manajemenroleteknologi_it"
    )
    
def hapus_teknologi_it_view(request,id_teknologi):
    conn = get_connection()
    repo = TeknologiRepository(conn)
    service = TeknologiService(repo,conn)
    try:
        service.hapus_teknologi(id_teknologi)
        messages.success(request,"Teknologi berhasil dihapus.")
    except Exception as e:
        traceback.print_exc()
        messages.error(request,str(e))
    return redirect("manajemenroleteknologi_it")

def edit_role_it_view(request, id_role):
    conn = get_connection()
    role = get_object_or_404(Role,id_role=id_role)
    teknologi_repo = (TeknologiRepository(connection))
    teknologi_service = (TeknologiService(teknologi_repo,connection))
    repo_bobot = (BobotKriteriaRepository(conn))
    all_teknologi = (teknologi_service.ambil_semua())
    if request.method == "GET":
        print("ROLE =", role.id_role)
        role_teknologi_list = (
            RoleTeknologi.objects
            .filter(role=role)
            .select_related("teknologi")
        )
        data_teknologi = []
        repo_bobot = (BobotKriteriaRepository(connection))
        for rt in role_teknologi_list:
            bobot_list = (repo_bobot.ambil_bobot_role_teknologi(rt.id_role_teknologi))
            print("ROLE TEK:",rt.id_role_teknologi)
            print("BOBOT:",bobot_list)
            data_teknologi.append({
                "id_role_teknologi":rt.id_role_teknologi,
                "id_teknologi":rt.teknologi.id_teknologi,
                "nama_teknologi":rt.teknologi.nama_teknologi,
                "bobot":bobot_list
            })
            print(data_teknologi)
        # ==========================
        # UPDATE BOBOT KRITERIA
        # ==========================
        return JsonResponse({
            "id_role": role.id_role,
            "nama_role": role.nama_role,
            "min_ram": role.min_ram,
            "min_storage": role.min_storage,
            "min_processor_score": role.min_processor_score,
            "teknologi": data_teknologi,
            "all_teknologi":all_teknologi
        })
    if request.method == "POST":
        try:
            with transaction.atomic():
                # ==========================
                # UPDATE ROLE
                # ==========================
                role.nama_role = request.POST.get("nama_role")
                role.min_ram = int(request.POST.get("min_ram",0))
                role.min_storage = int(request.POST.get("min_storage",0))
                role.min_processor_score = int(request.POST.get("min_processor_score",0))
                role.save()
                role_teknologi_repo = (RoleTeknologiRepository(connection))
                role_teknologi_lama = role_teknologi_repo.get_by_role( role.id_role)
                teknologi_baru = {
                    x.strip()
                    for x in request.POST.getlist(
                        "teknologi_ids[]"
                    )
                    if x.strip()
                }

                if not teknologi_baru:
                    raise Exception(
                        "Role harus memiliki minimal 1 teknologi."
                    )
                teknologi_lama = {
                    x["id_teknologi"] 
                    for x in role_teknologi_lama
                }
                teknologi_dihapus = (teknologi_lama- teknologi_baru)
                teknologi_ditambah = (teknologi_baru- teknologi_lama)
                teknologi_ids = request.POST.getlist("teknologi_ids[]")
                print("TEKNOLOGI IDS")
                print(teknologi_ids)
                for id_teknologi in teknologi_dihapus:
                    relasi = (role_teknologi_repo.get_relasi(role.id_role,id_teknologi))
                    if relasi:
                        id_role_teknologi = relasi[0]
                        repo_bobot.hapus_by_role_teknologi(id_role_teknologi)
                        role_teknologi_repo.hapus(id_role_teknologi)
                for id_teknologi in teknologi_ditambah:
                    role_teknologi_repo.tambah(
                        RoleTeknologiDTO(
                            id_role=role.id_role,
                            id_teknologi=id_teknologi
                        ))
                # ==========================
                # UPDATE BOBOT
                # ==========================
                repo_bobot = (BobotKriteriaRepository(connection))
                KRITERIA_MAPPING = {
                    "processor":"KRIT_0001",
                    "ram":"KRIT_0002",
                    "storage":"KRIT_0003",
                    "berat":"KRIT_0004",
                    "layar":"KRIT_0005",
                    "baterai":"KRIT_0006"
                }
                role_teknologi_list = (RoleTeknologi.objects.filter(role=role))
                for role_teknologi in (role_teknologi_list):
                    for (nama_kriteria,id_kriteria) in (KRITERIA_MAPPING.items()):
                        field_name = (f"{nama_kriteria}_weight_" f"{role_teknologi.teknologi.id_teknologi}")
                        nilai_bobot = (request.POST.get(field_name))
                        print(field_name,"=",nilai_bobot)
                        if nilai_bobot:
                            dto = (BobotKriteriaDTO(
                                    id_role_teknologi=role_teknologi.id_role_teknologi,
                                    id_kriteria=id_kriteria,
                                    nilai_bobot=float(nilai_bobot)
                                )
                            )
                            repo_bobot.update_bobot_role_teknologi(dto)
            messages.success(request,"Role berhasil diperbarui.")
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse(
                {
                    "error": str(e)
                },
                status=500
            )
        return redirect("manajemenroleteknologi_it")
    
def edit_teknologi_it_view(
    request,
    id_teknologi
):

    teknologi = get_object_or_404(
        Teknologi,
        id_teknologi=id_teknologi
    )

    if request.method == "POST":

        try:

            teknologi.nama_teknologi = (
                request.POST.get(
                    "nama_teknologi"
                )
            )

            teknologi.kategori = (
                request.POST.get(
                    "kategori"
                )
            )

            teknologi.save()
            messages.success
            messages.success(
                request,
                "Teknologi berhasil diperbarui."
            )

        except Exception as e:

            messages.error(
                request,
                f"Gagal update teknologi: {str(e)}"
            )

    return redirect(
        "manajemenroleteknologi_it"
    )

# ==========================================
# HC USER MANAGEMENT VIEWS
# ==========================================

def _generate_id_user():
    """Generate ID pengguna otomatis dengan format USR_XXXX."""
    from inventori.models import User
    existing = (
        User.objects
        .filter(id_user__startswith='USR_')
        .values_list('id_user', flat=True)
    )
    max_num = 0
    for uid in existing:
        try:
            num = int(uid.split('_')[1])
            if num > max_num:
                max_num = num
        except (IndexError, ValueError):
            pass
    return f"USR_{max_num + 1:04d}"


def manajemenuser_hc_view(request):
    """Halaman list semua pengguna dengan fitur search & filter."""
    from inventori.models import User
    from django.db.models import Q
    from django.core.paginator import Paginator

    search_query = request.GET.get('q', '').strip()
    role_filter  = request.GET.get('role', '').strip()

    list_user = User.objects.all().order_by('id_user')
    total_user = list_user.count()
    total_hc = list_user.filter(role='HC').count()
    total_it = list_user.filter(role='IT').count()
    total_talent = list_user.filter(role='Talent').count()

    if search_query:
        list_user = list_user.filter(
            Q(nama__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(id_user__icontains=search_query)
        )
    if role_filter:
        list_user = list_user.filter(role__iexact=role_filter)

    try:
        per_page = int(request.GET.get('per_page', 10))
        if per_page not in [10, 15, 25]:
            per_page = 10
    except ValueError:
        per_page = 10

    paginator = Paginator(list_user, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'list_user': page_obj,
        'total_user': total_user,
        'total_hc': total_hc,
        'total_it': total_it,
        'total_talent': total_talent,
        'search_query': search_query,
        'role_filter': role_filter,
        'per_page': per_page,
    }
    return render(request, 'hc/user/manajemenuser_hc.html', context)


def tambahuser_hc_view(request):
    """Halaman form tambah pengguna baru. ID digenerate otomatis."""
    from inventori.models import User

    if request.method == 'POST':
        nama                = request.POST.get('nama', '').strip()
        email               = request.POST.get('email', '').strip() or None
        role                = request.POST.get('role', '').strip()
        departemen          = request.POST.get('departemen', 'Non IT').strip()
        password            = request.POST.get('password', '')
        konfirmasi_password = request.POST.get('konfirmasi_password', '')

        form_data = {'nama': nama, 'email': email, 'role': role, 'departemen': departemen}

        if not nama or not role or not password:
            messages.error(request, 'Nama, role, dan password wajib diisi.')
            return render(request, 'hc/user/tambahuser_hc.html', {'form_data': form_data})

        if password != konfirmasi_password:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')
            return render(request, 'hc/user/tambahuser_hc.html', {'form_data': form_data})

        if len(password) < 8:
            messages.error(request, 'Password minimal 8 karakter.')
            return render(request, 'hc/user/tambahuser_hc.html', {'form_data': form_data})

        if email and User.objects.filter(email=email).exists():
            messages.error(request, f'Email "{email}" sudah terdaftar.')
            return render(request, 'hc/user/tambahuser_hc.html', {'form_data': form_data})

        try:
            new_id = _generate_id_user()
            User.objects.create(
                id_user=new_id,
                nama=nama,
                email=email,
                role=role,
                departemen=departemen,
                password=password,
            )
            messages.success(request, f'Pengguna "{nama}" ({role}) berhasil ditambahkan dengan ID {new_id}.')
            return redirect('manajemenuser_hc')

        except Exception as e:
            messages.error(request, f'Gagal menambahkan pengguna: {str(e)}')

    return render(request, 'hc/user/tambahuser_hc.html', {'form_data': {}})


def edit_user_hc_view(request):
    """Edit data pengguna (nama, email, role, departemen, password)."""
    from inventori.models import User

    if request.method == 'POST':
        id_user    = request.POST.get('id_user', '').strip()
        nama       = request.POST.get('nama', '').strip()
        email      = request.POST.get('email', '').strip() or None
        role       = request.POST.get('role', '').strip()
        departemen = request.POST.get('departemen', 'Non IT').strip()
        password   = request.POST.get('password', '')

        if not id_user or not nama or not role:
            messages.error(request, 'Data tidak lengkap.')
            return redirect('manajemenuser_hc')

        try:
            user = User.objects.get(id_user=id_user)
            user.nama = nama
            user.email = email
            user.role = role
            user.departemen = departemen
            if password:
                if len(password) < 8:
                    messages.error(request, 'Password baru minimal 8 karakter.')
                    return redirect('manajemenuser_hc')
                user.password = password
            user.save()
            messages.success(request, f'Data pengguna "{nama}" berhasil diperbarui.')
        except User.DoesNotExist:
            messages.error(request, 'Pengguna tidak ditemukan.')
        except Exception as e:
            messages.error(request, f'Gagal mengubah data: {str(e)}')

    return redirect('manajemenuser_hc')


def hapus_user_hc_view(request):
    """Hapus pengguna dari sistem."""
    from inventori.models import User

    if request.method == 'POST':
        id_user = request.POST.get('id_user', '').strip()

        if not id_user:
            messages.error(request, 'ID Pengguna tidak diberikan.')
            return redirect('manajemenuser_hc')

        try:
            user = User.objects.get(id_user=id_user)
            nama = user.nama
            user.delete()
            messages.success(request, f'Pengguna "{nama}" berhasil dihapus dari sistem.')
        except User.DoesNotExist:
            messages.error(request, 'Pengguna tidak ditemukan.')
        except Exception as e:
            messages.error(request, f'Gagal menghapus pengguna: {str(e)}')

    return redirect('manajemenuser_hc')


def profile_view(request):
    """Menampilkan dan mengelola data profil pengguna serta perubahan password."""
    if not request.user.is_authenticated:
        return redirect('login')

    from inventori.models import User as CustomUser
    from django.contrib.auth import update_session_auth_hash
    from django.contrib.auth.models import User as DjangoUser
    from django.contrib import messages

    # Get custom user from database using username (which holds id_user)
    custom_user = CustomUser.objects.filter(id_user=request.user.username).first()
    if not custom_user:
        messages.error(request, 'Data pengguna kustom tidak ditemukan.')
        return redirect('login_redirect')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_info':
            nama = request.POST.get('nama', '').strip()
            email = request.POST.get('email', '').strip() or None

            if not nama:
                messages.error(request, 'Nama Lengkap wajib diisi.')
            else:
                try:
                    # Cek email duplikat di user lain
                    if email and CustomUser.objects.filter(email=email).exclude(id_user=custom_user.id_user).exists():
                        messages.error(request, f'Email "{email}" sudah terdaftar oleh pengguna lain.')
                    else:
                        custom_user.nama = nama
                        custom_user.email = email
                        custom_user.save()

                        # Sinkronisasi ke standard Django User
                        django_user = DjangoUser.objects.filter(username=custom_user.id_user).first()
                        if django_user:
                            django_user.first_name = nama
                            django_user.email = email or ""
                            django_user.save()

                        # Sinkronisasi data di session request
                        request.user.nama = nama
                        request.user.email = email or ""

                        messages.success(request, 'Informasi profil berhasil diperbarui.')
                except Exception as e:
                    messages.error(request, f'Gagal memperbarui profil: {str(e)}')

        elif action == 'update_password':
            password_lama = request.POST.get('password_lama', '')
            password_baru = request.POST.get('password_baru', '')
            konfirmasi_password = request.POST.get('konfirmasi_password', '')

            if not password_lama or not password_baru or not konfirmasi_password:
                messages.error(request, 'Semua kolom password wajib diisi.')
            elif custom_user.password != password_lama:
                messages.error(request, 'Password lama yang Anda masukkan salah.')
            elif password_baru != konfirmasi_password:
                messages.error(request, 'Password baru dan konfirmasi password tidak cocok.')
            elif len(password_baru) < 8:
                messages.error(request, 'Password baru minimal 8 karakter.')
            else:
                try:
                    # Simpan plaintext password untuk sistem kustom
                    custom_user.password = password_baru
                    custom_user.save()

                    # Simpan hashed password untuk Django Standard User agar session tetap valid
                    django_user = DjangoUser.objects.filter(username=custom_user.id_user).first()
                    if django_user:
                        django_user.set_password(password_baru)
                        django_user.save()
                        update_session_auth_hash(request, django_user)

                    messages.success(request, 'Password berhasil diperbarui.')
                except Exception as e:
                    messages.error(request, f'Gagal memperbarui password: {str(e)}')

        return redirect('profile')

    context = {
        'custom_user': custom_user,
        'active_page': 'profile',
    }
    return render(request, 'users/profile.html', context)


def konfirmasi_pengembalian_hc_view(request):
    if request.method == 'POST':
        from inventori.models import Peminjaman, LaptopInventori, Pengajuan
        import datetime as _dt
        id_peminjaman = request.POST.get('id_peminjaman')
        
        try:
            peminjaman = Peminjaman.objects.filter(id_peminjaman=id_peminjaman).first()
            if peminjaman:
                peminjaman.status = 'selesai'
                if not peminjaman.tanggal_kembali:
                    peminjaman.tanggal_kembali = _dt.date.today()
                peminjaman.save()

                # Sync status pengajuan jika ada
                if peminjaman.id_pengajuan:
                    try:
                        pg = peminjaman.id_pengajuan
                        pg.status = 'selesai'
                        pg.save()
                    except Exception:
                        pass
                
                # Ubah status laptop berdasarkan kondisi fisik (jika rusak ringan/berat -> status rusak)
                laptop = LaptopInventori.objects.filter(id_laptop_inventori=peminjaman.id_laptop_inventori_id).first()
                if laptop:
                    st_kondisi = str(laptop.kondisi or '').lower()
                    if st_kondisi in ['baik', 'good', 'bagus', 'normal', '']:
                        laptop.status = 'tersedia'
                    else:
                        laptop.status = 'rusak'
                    laptop.save()
                
                messages.success(request, f'Pengembalian dengan ID {id_peminjaman} berhasil dikonfirmasi.')
            else:
                messages.error(request, 'Data peminjaman tidak ditemukan.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat konfirmasi: {e}')
            
    return redirect('notifikasi_hc')


def konfirmasi_pengembalian_it_view(request):
    if request.method == 'POST':
        from inventori.models import Peminjaman, LaptopInventori, Pengajuan
        import datetime as _dt
        id_peminjaman = request.POST.get('id_peminjaman')
        
        try:
            peminjaman = Peminjaman.objects.filter(id_peminjaman=id_peminjaman).first()
            if peminjaman:
                peminjaman.status = 'selesai'
                if not peminjaman.tanggal_kembali:
                    peminjaman.tanggal_kembali = _dt.date.today()
                peminjaman.save()

                if peminjaman.id_pengajuan:
                    try:
                        pg = peminjaman.id_pengajuan
                        pg.status = 'selesai'
                        pg.save()
                    except Exception:
                        pass
                
                laptop = LaptopInventori.objects.filter(id_laptop_inventori=peminjaman.id_laptop_inventori_id).first()
                if laptop:
                    st_kondisi = str(laptop.kondisi or '').lower()
                    if st_kondisi in ['baik', 'good', 'bagus', 'normal', '']:
                        laptop.status = 'tersedia'
                    else:
                        laptop.status = 'rusak'
                    laptop.save()
                
                messages.success(request, f'Pengembalian dengan ID {id_peminjaman} berhasil dikonfirmasi.')
            else:
                messages.error(request, 'Data peminjaman tidak ditemukan.')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan saat konfirmasi: {e}')
            
    return redirect('notifikasi_it')


def konfirmasi_penerimaan_talent_view(request):
    if request.method == 'POST':
        from inventori.models import Peminjaman
        id_peminjaman = request.POST.get('id_peminjaman')
        try:
            peminjaman = Peminjaman.objects.get(id_peminjaman=id_peminjaman)
            peminjaman.status = 'dipinjam'
            peminjaman.save()
            messages.success(request, 'Berhasil mengonfirmasi penerimaan laptop. Status sekarang aktif dipinjam.')
        except Exception as e:
            messages.error(request, f'Gagal melakukan konfirmasi: {str(e)}')
    return redirect('riwayatpeminjamanlaptop_talent')
