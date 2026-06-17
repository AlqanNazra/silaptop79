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
from dss.services.service_bobotkriteria import ServiceBobotKriteria
from dss.services.service_swara import ServiceSwara
from inventori.dto.dto_projectrole import ProjectRoleDTO
from inventori.dto.dto_proyek import ProyekDTO
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
        pengajuan_pending = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'pending')

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
        pengajuan_pending = 0
        riwayat_pinjam = []

    context = {
        'total_laptop': total_laptop,
        'total_pengajuan': total_pengajuan,
        'pengajuan_pending': pengajuan_pending,
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
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    try:
        per_page = int(request.GET.get('per_page', 5))
        if per_page not in [5, 15, 25, 50]:
            per_page = 5
    except ValueError:
        per_page = 5

    try:
        service = PengajuanService()
        semua_pengajuan = service.service_ambil_semua_pengajuan()

        from inventori.models import User
        import datetime
        users_dict = {u.id_user: u.nama for u in User.objects.all()}
        
        total_siap_proses = 0
        total_dikonfigurasi = 0
        total_selesai = 0
        total_mendesak = 0
        today = datetime.date.today()

        for p in semua_pengajuan:
            p.user_nama = users_dict.get(p.id_user, f"User {p.id_user}")
            
            # Map status_it for frontend representation
            if p.status and p.status.lower() == 'pending':
                p.status_it = 'configuring' # Configuring / Menunggu Antrean
                total_siap_proses += 1
                total_dikonfigurasi += 1
                # Calculate if urgent (due date <= 7 days)
                if p.bulan:
                    diff_days = (p.bulan - today).days
                    if diff_days <= 7:
                        total_mendesak += 1
            elif p.status and p.status.lower() == 'approved':
                p.status_it = 'ready' # Siap Diambil
                total_selesai += 1
            else:
                p.status_it = 'rejected'
        
        # Sort by date descending
        semua_pengajuan.sort(key=lambda x: x.tanggal_pengajuan if x.tanggal_pengajuan else datetime.date.min, reverse=True)
        
        total_pengajuan = len(semua_pengajuan)
        total_pending = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'pending')
        total_disetujui = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'approved')
        total_ditolak = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'rejected')

        # Filter search
        if search_query:
            q_lower = search_query.lower()
            semua_pengajuan = [
                p for p in semua_pengajuan
                if q_lower in getattr(p, 'user_nama', '').lower() or
                   q_lower in str(getattr(p, 'id_pengajuan', '')).lower() or
                   q_lower in getattr(p, 'spesifikasi_tambahan', '').lower()
            ]

        # Filter status
        if status_filter:
            status_lower = status_filter.lower()
            semua_pengajuan = [
                p for p in semua_pengajuan
                if getattr(p, 'status', '').lower() == status_lower
            ]

        from django.core.paginator import Paginator
        paginator = Paginator(semua_pengajuan, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'list_pengajuan': page_obj,
            'total_pengajuan': total_pengajuan,
            'total_pending': total_pending,
            'total_disetujui': total_disetujui,
            'total_ditolak': total_ditolak,
            'total_siap_proses': total_siap_proses,
            'total_dikonfigurasi': total_dikonfigurasi,
            'total_selesai': total_selesai,
            'total_mendesak': total_mendesak,
            'search_query': search_query,
            'status_filter': status_filter,
            'per_page': per_page,
        }
    except Exception as e:
        context = {
            'error_message': f'Gagal memuat data pengajuan: {str(e)}',
            'list_pengajuan': [],
            'total_pengajuan': 0,
            'total_pending': 0,
            'total_disetujui': 0,
            'total_ditolak': 0,
            'total_siap_proses': 0,
            'total_dikonfigurasi': 0,
            'total_selesai': 0,
            'total_mendesak': 0,
            'search_query': search_query,
            'status_filter': status_filter,
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
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

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

        # Filter search
        if search_query:
            q_lower = search_query.lower()
            riwayat_list = [
                p for p in riwayat_list
                if q_lower in getattr(p, 'user_nama', '').lower() or
                   q_lower in getattr(p, 'laptop_nama', '').lower() or
                   q_lower in str(getattr(p, 'id_peminjaman', '')).lower()
            ]

        # Filter status
        if status_filter:
            status_lower = status_filter.lower()
            riwayat_list = [
                p for p in riwayat_list
                if getattr(p, 'status', '').lower() == status_lower
            ]

        from django.core.paginator import Paginator
        paginator = Paginator(riwayat_list, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
            
        context = {
            'list_peminjaman': page_obj,
            'total_peminjaman': total_peminjaman,
            'peminjam_terakhir': peminjam_terakhir,
            'search_query': search_query,
            'status_filter': status_filter,
        }
    except Exception as e:
        messages.error(request, f'Gagal memuat riwayat: {str(e)}')
        context = {
            'list_peminjaman': [],
            'total_peminjaman': 0,
            'peminjam_terakhir': "-",
            'search_query': search_query,
            'status_filter': status_filter,
        }
    return render(request, 'it/inventori/riwayatpeminjamanlaptop_it.html', context)

def editdatalaptop_hc_view(request):
    return render(request, 'hc/inventori/editdatalaptop_hc.html')

def inputkriteria_hc_view(request):
    conn = get_connection()

    selected_project = (
        request.GET.get("id_proyek")
        or request.POST.get("id_proyek")
    )

    selected_role_teknologi = (
        request.GET.get("id_role_teknologi")
        or request.POST.get("id_role_teknologi")
    )

    role_requirement = None
    bobot_role = None
    # ==========================
    # LOAD ROLE REQUIREMENT
    # ==========================
    if selected_role_teknologi:
        try:
            roletek = (
                RoleTeknologi.objects
                .select_related("role")
                .get(
                    id_role_teknologi=
                    selected_role_teknologi
                )
            )
            print("ROLE =", roletek.role)
            print("RAM =", roletek.role.min_ram)
            print("STORAGE =", roletek.role.min_storage)
            print("PROC =", roletek.role.min_processor_score)


            role_requirement = {
                "id_role":
                    roletek.role.id_role,
                "nama_role":
                    roletek.role.nama_role,
                "min_ram":
                    roletek.role.min_ram,
                "min_storage":
                    roletek.role.min_storage,
                "min_processor_score":
                    roletek.role.min_processor_score
            }
            repo_bobot = BobotKriteriaRepository(conn)
            rows = (
                repo_bobot
                .ambil_bobot_role_teknologi(
                    selected_role_teknologi
                )
            )
            bobot_role = {}
            for row in rows:
                nama = (
                    row["nama_kriteria"]
                    .lower()
                    .strip()
                )
                bobot_role[nama] = (
                    row["nilai_bobot"]
                )
            print("BOBOT =", bobot_role)
        except Exception as e:
            print(
                "ERROR ROLE REQUIREMENT:",
                str(e)
            )

    # ==========================
    # PROSES DSS
    # ==========================
    if request.method == "POST":

        print("=" * 50)
        print("POST DSS")
        print("POST =", request.POST)

        action = request.POST.get(
            "action",
            "load"
        )

        jenis_rekomendasi = request.POST.get(
            "jenis_rekomendasi",
            "inventori"
        )

        min_harga = request.POST.get(
            "min_harga",
            ""
        )

        print("JENIS =", jenis_rekomendasi)
        print("MIN HARGA =", min_harga)

        print("ACTION =", action)
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

            request.session[
                "selected_project"
            ] = request.POST.get(
                "id_proyek"
            )

            request.session[
                "selected_role_teknologi"
            ] = request.POST.get(
                "id_role_teknologi"
            )

            request.session[
                "dss_raw_weights"
            ] = raw_weights

            request.session[
                "minimum_requirement"
            ] = {
                "processor_score":
                    request.POST.get(
                        "min_processor_score"
                    ),
                "ram":
                    request.POST.get(
                        "min_ram"
                    ),
                "storage":
                    request.POST.get(
                        "min_storage"
                    ),
                "min_harga":
                    min_harga
            }
            # ==========================
            # PROSES DSS SEKALI SAJA
            # ==========================

            selected_role_teknologi = request.session.get(
                "selected_role_teknologi"
            )

            minimum_requirement = request.session.get(
                "minimum_requirement",
                {}
            )

            roletek = (
                RoleTeknologi.objects
                .select_related("role")
                .get(
                    id_role_teknologi=
                    selected_role_teknologi
                )
            )

            role_id = roletek.role.id_role

            if jenis_rekomendasi == "inventori":

                filter_data = FilterInventoriDTO(
                    min_ram_kapasitas=int(
                        minimum_requirement.get(
                            "ram",
                            0
                        ) or 0
                    ),
                    min_storage=int(
                        minimum_requirement.get(
                            "storage",
                            0
                        ) or 0
                    )
                )

            else:

                filter_data = FilterPengadaanDTO(
                    min_ram_kapasitas=int(
                        minimum_requirement.get(
                            "ram",
                            0
                        ) or 0
                    ),
                    min_storage=int(
                        minimum_requirement.get(
                            "storage",
                            0
                        ) or 0
                    ),
                    min_harga=int(
                        minimum_requirement.get(
                            "min_harga",
                            0
                        ) or 0
                    )
                )

            service = Servicesaw(conn)

            hasil = service.proses_dss_saw(
                id_user="USR_0001",
                id_bobot=selected_role_teknologi,
                sumber_data=jenis_rekomendasi,
                filter_data=filter_data,
                role=[role_id],
                debug=True
            )

            print("\n=== HASIL SERVICE ===")
            print(hasil)

            if hasil.get("status") != "success":

                messages.error(
                    request,
                    hasil.get(
                        "message",
                        "Gagal menjalankan DSS"
                    )
                )

                return redirect(
                    "inputkriteria_hc"
                )

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

            request.session["warning_dss"] = (
                hasil.get("warning")
            )
            request.session["jenis_rekomendasi"] = (
                request.POST.get(
                    "jenis_rekomendasi",
                    "inventori"
                )
            )
            warning_dss = request.session.get("warning_dss")
            return redirect(
                "hasilrekomendasi_hc"
)        
        except Exception as e:
            import traceback

            print(
                traceback.format_exc()
            )

            messages.error(
                request,
                f"Gagal memproses DSS: {str(e)}"
            )

    projects = (
        Proyek.objects
        .all()
        .order_by(
            "nama_proyek"
        )
    )

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

    for pr in (
        ProjectRole.objects
        .select_related("proyek", "role")
    ):
        roleteks = (
            RoleTeknologi.objects
            .select_related("role", "teknologi")
            .filter(role=pr.role)
        )

        for rt in roleteks:

            project_role_mapping.append({
                "id_proyek":
                    pr.proyek.id_proyek,

                "id_role_teknologi":
                    rt.id_role_teknologi,

                "nama":
                    (
                        f"{rt.role.nama_role}"
                        f" - "
                        f"{rt.teknologi.nama_teknologi}"
                    )
            })
    context = {
        "projects": projects,
        "role_teknologi": role_teknologi,
        "role_requirement": role_requirement,
        "bobot_role": bobot_role,
        "selected_project": selected_project,
        "selected_role_teknologi": selected_role_teknologi,

        "project_role_mapping":(project_role_mapping)
    }
    return render(
        request,
        "hc/dss/inputkriteria_hc.html",
        context
    )


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
                                "benchmark_score",
                                0
                            )
                    }
                elif jenis_rekomendasi == "pengadaan":
                    pengadaan = repo_laptop_pengadaan.ambil_laptop_pengadaan_by_id(
                        item["id"]
                    )
                    print("=" * 50)
                    print("ID =", item["id"])
                    print("PENGADAAN =", pengadaan)
                    print("=" * 50)
                    item["detail"] = {
                        "nama": pengadaan.get("nama_laptop",item["id"]),
                        "processor":
                            f"{pengadaan.get('manufacturer', '')} "
                            f"{pengadaan.get('processor_model', '')}",
                        "ram":pengadaan.get("ram_kapasitas",0),
                        "storage":pengadaan.get("storage_kapasitas",0),
                        "layar":pengadaan.get("ukuran_layar",0),
                        "harga":pengadaan.get("harga",0),
                        "benchmark":pengadaan.get("benchmark_score",0),
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
        
        paginator = Paginator(ranking_sesuai, 10)  # Tampilkan 10 item per halaman
        page_number = request.GET.get('page')
        rangking_page = paginator.get_page(page_number)
        alternatif_paginator = Paginator(ranking_alternatif, 10)
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
            "inputkriteria_it"
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
                    "hasilrekomendasi_it"
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
            "benchmark_score": pengadaan.get("benchmark_score", 0),
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
    from inventori.models import Pengajuan
    import datetime
    
    # Get all pending pengajuan
    pending_list = Pengajuan.objects.filter(status='pending').select_related('id_user').order_by('bulan')
    
    today = datetime.date.today()
    notifications = []
    
    for p in pending_list:
        diff_days = (p.bulan - today).days
        
        # Determine urgency class & tag
        if diff_days <= 3:
            urgency_class = 'urgent'
            urgency_tag = 'Sangat Mendesak'
        elif diff_days <= 7:
            urgency_class = 'warning'
            urgency_tag = 'Mendesak'
        else:
            urgency_class = 'info'
            urgency_tag = 'Segera Disiapkan'
            
        # Time string
        if diff_days < 0:
            time_str = f"Lewat {abs(diff_days)} hari"
        elif diff_days == 0:
            time_str = "Hari ini"
        elif diff_days == 1:
            time_str = "Besok"
        else:
            time_str = f"{diff_days} hari lagi"
            
        notifications.append({
            'id_pengajuan': p.id_pengajuan,
            'user_nama': p.id_user.nama if p.id_user else '',
            'kebutuhan_role': p.kebutuhan_role,
            'perusahaan': p.perusahaan,
            'bulan': p.bulan.strftime('%d %B %Y') if hasattr(p.bulan, 'strftime') else p.bulan,
            'tanggal_pengajuan': p.tanggal_pengajuan.strftime('%d %B %Y') if hasattr(p.tanggal_pengajuan, 'strftime') else '',
            'urgency_class': urgency_class,
            'urgency_tag': urgency_tag,
            'time_str': time_str,
            'keterangan': p.keterangan
        })
        
    return render(request, 'hc/inventori/notifikasi_hc.html', {
        'notifications': notifications
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

    try:
        per_page = int(request.GET.get('per_page', 5))
        if per_page not in [5, 15, 25, 50]:
            per_page = 5
    except ValueError:
        per_page = 5

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
    conn = get_connection()

    selected_project = (
        request.GET.get("id_proyek")
        or request.POST.get("id_proyek")
    )

    selected_role_teknologi = (
        request.GET.get("id_role_teknologi")
        or request.POST.get("id_role_teknologi")
    )

    role_requirement = None
    bobot_role = None
    # ==========================
    # LOAD ROLE REQUIREMENT
    # ==========================
    if selected_role_teknologi:
        try:
            roletek = (
                RoleTeknologi.objects
                .select_related("role")
                .get(
                    id_role_teknologi=
                    selected_role_teknologi
                )
            )
            print("ROLE =", roletek.role)
            print("RAM =", roletek.role.min_ram)
            print("STORAGE =", roletek.role.min_storage)
            print("PROC =", roletek.role.min_processor_score)


            role_requirement = {
                "id_role":
                    roletek.role.id_role,
                "nama_role":
                    roletek.role.nama_role,
                "min_ram":
                    roletek.role.min_ram,
                "min_storage":
                    roletek.role.min_storage,
                "min_processor_score":
                    roletek.role.min_processor_score
            }
            repo_bobot = BobotKriteriaRepository(conn)
            rows = (
                repo_bobot
                .ambil_bobot_role_teknologi(
                    selected_role_teknologi
                )
            )
            bobot_role = {}
            for row in rows:
                nama = (
                    row["nama_kriteria"]
                    .lower()
                    .strip()
                )
                bobot_role[nama] = (
                    row["nilai_bobot"]
                )
            print("BOBOT =", bobot_role)
        except Exception as e:
            print(
                "ERROR ROLE REQUIREMENT:",
                str(e)
            )

    # ==========================
    # PROSES DSS
    # ==========================
    if request.method == "POST":

        print("=" * 50)
        print("POST DSS")
        print("POST =", request.POST)

        action = request.POST.get(
            "action",
            "load"
        )

        jenis_rekomendasi = request.POST.get(
            "jenis_rekomendasi",
            "inventori"
        )

        min_harga = request.POST.get(
            "min_harga",
            ""
        )

        print("JENIS =", jenis_rekomendasi)
        print("MIN HARGA =", min_harga)

        print("ACTION =", action)
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

            request.session[
                "selected_project"
            ] = request.POST.get(
                "id_proyek"
            )

            request.session[
                "selected_role_teknologi"
            ] = request.POST.get(
                "id_role_teknologi"
            )

            request.session[
                "dss_raw_weights"
            ] = raw_weights

            request.session[
                "minimum_requirement"
            ] = {
                "processor_score":
                    request.POST.get(
                        "min_processor_score"
                    ),
                "ram":
                    request.POST.get(
                        "min_ram"
                    ),
                "storage":
                    request.POST.get(
                        "min_storage"
                    ),
                "min_harga":
                    min_harga
            }
            # ==========================
            # PROSES DSS SEKALI SAJA
            # ==========================

            selected_role_teknologi = request.session.get(
                "selected_role_teknologi"
            )

            minimum_requirement = request.session.get(
                "minimum_requirement",
                {}
            )

            roletek = (
                RoleTeknologi.objects
                .select_related("role")
                .get(
                    id_role_teknologi=
                    selected_role_teknologi
                )
            )

            role_id = roletek.role.id_role

            if jenis_rekomendasi == "inventori":

                filter_data = FilterInventoriDTO(
                    min_ram_kapasitas=int(
                        minimum_requirement.get(
                            "ram",
                            0
                        ) or 0
                    ),
                    min_storage=int(
                        minimum_requirement.get(
                            "storage",
                            0
                        ) or 0
                    )
                )

            else:

                filter_data = FilterPengadaanDTO(
                    min_ram_kapasitas=int(
                        minimum_requirement.get(
                            "ram",
                            0
                        ) or 0
                    ),
                    min_storage=int(
                        minimum_requirement.get(
                            "storage",
                            0
                        ) or 0
                    ),
                    min_harga=int(
                        minimum_requirement.get(
                            "min_harga",
                            0
                        ) or 0
                    )
                )

            service = Servicesaw(conn)

            hasil = service.proses_dss_saw(
                id_user="USR_0001",
                id_bobot=selected_role_teknologi,
                sumber_data=jenis_rekomendasi,
                filter_data=filter_data,
                role=[role_id],
                debug=True
            )

            print("\n=== HASIL SERVICE ===")
            print(hasil)

            if hasil.get("status") != "success":

                messages.error(
                    request,
                    hasil.get(
                        "message",
                        "Gagal menjalankan DSS"
                    )
                )

                return redirect(
                    "inputkriteria_it"
                )

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

            request.session["warning_dss"] = (
                hasil.get("warning")
            )
            request.session["jenis_rekomendasi"] = (
                request.POST.get(
                    "jenis_rekomendasi",
                    "inventori"
                )
            )
            warning_dss = request.session.get("warning_dss")
            return redirect(
                "hasilrekomendasi_it"
)        
        except Exception as e:
            import traceback

            print(
                traceback.format_exc()
            )

            messages.error(
                request,
                f"Gagal memproses DSS: {str(e)}"
            )

    projects = (
        Proyek.objects
        .all()
        .order_by(
            "nama_proyek"
        )
    )

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

    for pr in (
        ProjectRole.objects
        .select_related("proyek", "role")
    ):
        roleteks = (
            RoleTeknologi.objects
            .select_related("role", "teknologi")
            .filter(role=pr.role)
        )

        for rt in roleteks:

            project_role_mapping.append({
                "id_proyek":
                    pr.proyek.id_proyek,

                "id_role_teknologi":
                    rt.id_role_teknologi,

                "nama":
                    (
                        f"{rt.role.nama_role}"
                        f" - "
                        f"{rt.teknologi.nama_teknologi}"
                    )
            })
    context = {
        "projects": projects,
        "role_teknologi": role_teknologi,
        "role_requirement": role_requirement,
        "bobot_role": bobot_role,
        "selected_project": selected_project,
        "selected_role_teknologi": selected_role_teknologi,

        "project_role_mapping":(project_role_mapping)
    }
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
    from django.contrib import messages

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
                                "benchmark_score",
                                0
                            )
                    }
                elif jenis_rekomendasi == "pengadaan":
                    pengadaan = repo_laptop_pengadaan.ambil_laptop_pengadaan_by_id(
                        item["id"]
                    )
                    print("=" * 50)
                    print("ID =", item["id"])
                    print("PENGADAAN =", pengadaan)
                    print("=" * 50)
                    item["detail"] = {
                        "nama": pengadaan.get("nama_laptop",item["id"]),
                        "processor":
                            f"{pengadaan.get('manufacturer', '')} "
                            f"{pengadaan.get('processor_model', '')}",
                        "ram":pengadaan.get("ram_kapasitas",0),
                        "storage":pengadaan.get("storage_kapasitas",0),
                        "layar":pengadaan.get("ukuran_layar",0),
                        "harga":pengadaan.get("harga",0),
                        "benchmark":pengadaan.get("benchmark_score",0),
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
        
        paginator = Paginator(ranking_sesuai, 10)  # Tampilkan 10 item per halaman
        page_number = request.GET.get('page')
        rangking_page = paginator.get_page(page_number)
        alternatif_paginator = Paginator(ranking_alternatif, 10)
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
            "benchmark_score": pengadaan.get("benchmark_score", 0),
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
    from inventori.models import Pengajuan
    import datetime
    
    # Get all pending pengajuan
    pending_list = Pengajuan.objects.filter(status='pending').select_related('id_user').order_by('bulan')
    
    today = datetime.date.today()
    notifications = []
    
    for p in pending_list:
        diff_days = (p.bulan - today).days
        
        # Determine urgency class & tag
        if diff_days <= 3:
            urgency_class = 'urgent'
            urgency_tag = 'Sangat Mendesak'
        elif diff_days <= 7:
            urgency_class = 'warning'
            urgency_tag = 'Mendesak'
        else:
            urgency_class = 'info'
            urgency_tag = 'Segera Disiapkan'
            
        # Time string
        if diff_days < 0:
            time_str = f"Lewat {abs(diff_days)} hari"
        elif diff_days == 0:
            time_str = "Hari ini"
        elif diff_days == 1:
            time_str = "Besok"
        else:
            time_str = f"{diff_days} hari lagi"
            
        notifications.append({
            'id_pengajuan': p.id_pengajuan,
            'user_nama': p.id_user.nama if p.id_user else '',
            'kebutuhan_role': p.kebutuhan_role,
            'perusahaan': p.perusahaan,
            'bulan': p.bulan.strftime('%d %B %Y') if hasattr(p.bulan, 'strftime') else p.bulan,
            'tanggal_pengajuan': p.tanggal_pengajuan.strftime('%d %B %Y') if hasattr(p.tanggal_pengajuan, 'strftime') else '',
            'urgency_class': urgency_class,
            'urgency_tag': urgency_tag,
            'time_str': time_str,
            'keterangan': p.keterangan
        })
        
    return render(request, 'it/inventori/notifikasi_it.html', {
        'notifications': notifications
    })
    return render(request, 'it/inventori/notifikasi_it.html')

# Procurement management views for IT
def manajemenpengadaan_it_view(request):
    search_query = request.GET.get('q', '')
    
    mock_pengadaan = [
        {"id": 1, "name": "MacBook Pro M3 Max 14-inch", "brand": "Apple Inc."},
        {"id": 2, "name": "ThinkPad X1 Carbon Gen 10", "brand": "Lenovo"},
        {"id": 3, "name": "ASUS ROG Zephyrus G14", "brand": "ASUS"},
    ]
    
    if search_query:
        mock_pengadaan = [
            item for item in mock_pengadaan
            if search_query.lower() in item["name"].lower() or search_query.lower() in item["brand"].lower()
        ]
        
    from django.core.paginator import Paginator
    paginator = Paginator(mock_pengadaan, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'pengadaan_list': page_obj,
        'search_query': search_query,
        'total': len(mock_pengadaan),
    }
    return render(request, 'it/inventori/manajemenpengadaan_it.html', context)

def detailpengadaan_it_view(request):
    return render(request, 'it/inventori/detailpengadaan_it.html')

def editpengadaan_it_view(request):
    return render(request, 'it/inventori/editpengadaan_it.html')

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
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    try:
        service = PengajuanService()

        # Ambil user id
        user_id = request.POST.get('id_user')

        if not user_id:
            user_id = (
                request.user.id_user
                if hasattr(request.user, 'id_user')
                else None
            )
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

            service.service_tambah_pengajuan(dto)
            messages.success(request, 'Pengajuan laptop berhasil dikirim dan sedang menunggu persetujuan.')
            return redirect('pengajuanlaptop_talent')

        semua_pengajuan = service.service_ambil_semua_pengajuan()

        if user_id:
            semua_pengajuan = [
                p for p in semua_pengajuan
                if getattr(p, 'id_user', None) == user_id
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
            per_page = int(request.GET.get('per_page', 5))
            if per_page not in [5, 15, 25, 50]:
                per_page = 5
        except ValueError:
            per_page = 5

        import datetime as dt
        semua_pengajuan.sort(
            key=lambda x: x.tanggal_pengajuan if x.tanggal_pengajuan else dt.date.min,
            reverse=True
        )

        from django.core.paginator import Paginator
        paginator = Paginator(semua_pengajuan, per_page)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'list_pengajuan': page_obj,
            'total_pengajuan': len(semua_pengajuan),
            'search_query': search_query,
            'status_filter': status_filter,
            'per_page': per_page,
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
        }
        return render(
            request,
            'talent/inventori/pengajuanlaptop_talent.html',
            context
        )

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
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')

    try:
        per_page = int(request.GET.get('per_page', 5))
        if per_page not in [5, 15, 25, 50]:
            per_page = 5
    except ValueError:
        per_page = 5

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
    search_query = request.GET.get('q', '')
    
    mock_pengadaan = [
        {"id": 1, "name": "MacBook Pro M3 Max 14-inch", "brand": "Apple Inc."},
        {"id": 2, "name": "ThinkPad X1 Carbon Gen 10", "brand": "Lenovo"},
        {"id": 3, "name": "ASUS ROG Zephyrus G14", "brand": "ASUS"},
    ]
    
    if search_query:
        mock_pengadaan = [
            item for item in mock_pengadaan
            if search_query.lower() in item["name"].lower() or search_query.lower() in item["brand"].lower()
        ]
        
    from django.core.paginator import Paginator
    paginator = Paginator(mock_pengadaan, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'pengadaan_list': page_obj,
        'search_query': search_query,
        'total': len(mock_pengadaan),
    }
    return render(request, 'it/inventori/manajemenpengadaan_it.html', context)

def detailpengadaan_it_view(request):
    return render(request, 'it/inventori/detailpengadaan_it.html')

def editpengadaan_it_view(request):
    return render(request, 'it/inventori/editpengadaan_it.html')

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
            user_id = request.user.id_user if (hasattr(request.user, 'id_user') and request.user.id_user) else 'USR-002'
            dto_peng = PengajuanDTO(
                id_pengajuan=pengajuan_id,
                status='approved',
                approved_by=user_id
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

            messages.success(request, 'Pengajuan berhasil disetujui oleh IT dan laptop telah dipinjamkan.')
            return redirect('pengajuanlaptop_it')
        except Exception as e:
            messages.error(request, f'Gagal menyetujui pengajuan: {str(e)}')
            return redirect(f"{request.path}?id={pengajuan_id}")

    # GET Request: Fetch and Map Laptop Specifications
    laptops = LaptopInventori.objects.filter(status__in=['tersedia', 'Available', 'Tersedia']).select_related('id_processor', 'id_ram', 'id_storage')
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

    paginator = Paginator(proyek_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "proyek_list": page_obj,
        "search_query": search_query,
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
            proyek_data = ProyekDTO(id_proyek=id_proyek,
                nama_proyek=request.POST.get("nama_proyek"),
                user_perusahaan=request.POST.get("user_perusahaan"),
                mulai_proyek=request.POST.get("mulai_proyek"),
                akhir_proyek=request.POST.get("akhir_proyek")
            )
            (
                service_proyek.update_proyek(proyek_data)
            )
            messages.success(request,f'Proyek "{proyek_data.nama_proyek}" berhasil diperbarui!')
            return redirect("manajemen_proyek_it")
        except Exception as e:
            traceback.print_exc()
            messages.error(request,str(e))
            
    proyek = (proyek_repo.ambil_by_id_full_proyek(id_proyek))
    role_list = (proyek_repo.ambil_role_proyek(id_proyek))
    context = {
        "proyek": proyek,"role_list": role_list
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

    search_role = request.GET.get('q_role', '')
    search_tech = request.GET.get('q_tech', '')

    role_list = (Role.objects.prefetch_related('teknologi_role__teknologi').order_by('nama_role'))
    teknologi_list = (Teknologi.objects.order_by('nama_teknologi'))
    if search_role:
        role_list = role_list.filter(Q(nama_role__icontains=search_role))

    if search_tech:
        teknologi_list = teknologi_list.filter(Q(nama_teknologi__icontains=search_tech) | Q(kategori__icontains=search_tech))
    paginator_role = Paginator(role_list, 5)
    page_role = request.GET.get('page_role')
    role_obj = paginator_role.get_page(page_role)
    paginator_tech = Paginator(teknologi_list, 5)
    page_tech = request.GET.get('page_tech')
    tech_obj = paginator_tech.get_page(page_tech)
    active_tab = request.GET.get('tab', 'role')
    context = {
        "role_list": role_obj,
        "tech_page": tech_obj,
        "teknologi_list": teknologi_list,
        "search_role": search_role,
        "search_tech": search_tech,
        "active_tab": active_tab,
    }
    return render(request,"it/inventori/manajemenroleteknologi_it.html",context)
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
    role_teknologi_repo = RoleTeknologiRepository(conn)

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

            role = Role.objects.create(

                id_role=
                    str(uuid.uuid4())[:8],

                nama_role=
                    request.POST.get(
                        "nama_role"
                    ),

                min_ram=
                    request.POST.get(
                        "min_ram"
                    ),

                min_storage=
                    request.POST.get(
                        "min_storage"
                    ),

                min_processor_score=
                    request.POST.get(
                        "min_processor_score"
                    )
            )

            print("\n====================")
            print("ROLE CREATED")
            print("====================")

            print(
                "ID ROLE :",
                role.id_role
            )

            print(
                "NAMA    :",
                role.nama_role
            )

            print(
                "RAM     :",
                role.min_ram
            )

            print(
                "STORAGE :",
                role.min_storage
            )

            print(
                "CPU     :",
                role.min_processor_score
            )

            # ==========================
            # AMBIL TEKNOLOGI
            # ==========================

            teknologi_ids = (
                request.POST.getlist(
                    "teknologi"
                )
            )

            print("\nTEKNOLOGI TERPILIH")
            print(teknologi_ids)

            # ==========================
            # SERVICE BOBOT
            # ==========================

            service_bobot = (
                ServiceBobotKriteria(
                    conn
                )
            )

            KRITERIA_MAPPING = {

                "processor":
                    "KRIT_0001",

                "ram":
                    "KRIT_0002",

                "storage":
                    "KRIT_0003",

                "berat":
                    "KRIT_0004",

                "layar":
                    "KRIT_0005",

                "baterai":
                    "KRIT_0006"
            }

            # ==========================
            # LOOP TEKNOLOGI
            # ==========================

            for teknologi_id in teknologi_ids:

                print("\n===================================")
                print(
                    "PROSES TEKNOLOGI:",
                    teknologi_id
                )
                print("===================================")

                # ----------------------
                # CREATE ROLE TEKNOLOGI
                # ----------------------
                dto_role_teknologi = (
                    RoleTeknologiDTO(
                        id_role=
                            role.id_role,

                        id_teknologi=
                            teknologi_id
                    )
                )

                id_role_teknologi = (
                    role_teknologi_repo
                    .tambah(
                        dto_role_teknologi
                    )
                )

                print(
                    "\nDEBUG ROLE TEKNOLOGI"
                )

                print(
                    "ID:",
                    id_role_teknologi
                )

                print(
                    "TYPE:",
                    type(
                        id_role_teknologi
                    )
                )

                # ----------------------
                # AMBIL BOBOT FORM
                # ----------------------

                processor = request.POST.get(
                    f"processor_weight_{teknologi_id}"
                )

                ram = request.POST.get(
                    f"ram_weight_{teknologi_id}"
                )

                storage = request.POST.get(
                    f"storage_weight_{teknologi_id}"
                )

                berat = request.POST.get(
                    f"berat_weight_{teknologi_id}"
                )

                layar = request.POST.get(
                    f"layar_weight_{teknologi_id}"
                )

                baterai = request.POST.get(
                    f"baterai_weight_{teknologi_id}"
                )

                print("\nDEBUG BOBOT")

                print(
                    "processor =",
                    processor
                )

                print(
                    "ram       =",
                    ram
                )

                print(
                    "storage   =",
                    storage
                )

                print(
                    "berat     =",
                    berat
                )

                print(
                    "layar     =",
                    layar
                )

                print(
                    "baterai   =",
                    baterai
                )

                # ----------------------
                # LIST BOBOT
                # ----------------------

                list_bobot = [

                    {
                        "id_kriteria":
                            KRITERIA_MAPPING[
                                "processor"
                            ],

                        "nilai_bobot":
                            float(processor or 0)
                    },

                    {
                        "id_kriteria":
                            KRITERIA_MAPPING[
                                "ram"
                            ],

                        "nilai_bobot":
                            float(ram or 0)
                    },

                    {
                        "id_kriteria":
                            KRITERIA_MAPPING[
                                "storage"
                            ],

                        "nilai_bobot":
                            float(storage or 0)
                    },

                    {
                        "id_kriteria":
                            KRITERIA_MAPPING[
                                "berat"
                            ],

                        "nilai_bobot":
                            float(berat or 0)
                    },

                    {
                        "id_kriteria":
                            KRITERIA_MAPPING[
                                "layar"
                            ],

                        "nilai_bobot":
                            float(layar or 0)
                    },

                    {
                        "id_kriteria":
                            KRITERIA_MAPPING[
                                "baterai"
                            ],

                        "nilai_bobot":
                            float(baterai or 0)
                    }
                ]

                print("\nLIST BOBOT")

                for item in list_bobot:

                    print(
                        item["id_kriteria"],
                        item["nilai_bobot"]
                    )

                # ----------------------
                # SAVE BOBOT
                # ----------------------

                result = (
                    service_bobot
                    .input_bobot_role_teknologi(
                        id_role_teknologi,
                        list_bobot
                    )
                )

                print(
                    "\nHASIL SERVICE:"
                )

                print(result)

                if (
                    result["status"]
                    !=
                    "success"
                ):

                    raise Exception(
                        result["message"]
                    )
            # ==========================
            # PROSES SWARA
            # ==========================
            print("\n===================================")
            print("PROSES SWARA")
            print("===================================")

            service_swara = (
                ServiceSwara(conn)
            )

            hasil_swara = (
                service_swara
                .proses_swara_role_teknologi(
                    id_role_teknologi
                )
            )

            print(
                "\nHASIL SWARA"
            )

            print(
                hasil_swara
            )

            if (
                hasil_swara["status"]
                !=
                "success"
            ):
                raise Exception(
                    hasil_swara["message"]
                )

            print("\n===================================")
            print("SELESAI TAMBAH ROLE")
            print("===================================")

            messages.success(
                request,
                "Role berhasil ditambahkan."
            )

        except Exception as e:

            traceback.print_exc()

            print(
                "\nERROR:",
                str(e)
            )

            messages.error(
                request,
                str(e)
            )

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

    role = get_object_or_404(
        Role,
        id_role=id_role
    )

    # ====================================
    # GET DATA UNTUK MODAL EDIT
    # ====================================

    if request.method == "GET":

        role_teknologi_list = (
            RoleTeknologi.objects
            .filter(role=role)
            .select_related("teknologi")
        )

        data_teknologi = []

        repo_bobot = (
            BobotKriteriaRepository(
                connection
            )
        )

        for rt in role_teknologi_list:

            bobot_list = (
                repo_bobot
                .ambil_bobot_role_teknologi(
                    rt.id_role_teknologi
                )
            )
            print("ROLE TEK:",rt.id_role_teknologi)
            print("BOBOT:",bobot_list)
            data_teknologi.append({
                "id_role_teknologi":
                    rt.id_role_teknologi,
                "id_teknologi":
                    rt.teknologi.id_teknologi,
                "nama_teknologi":
                    rt.teknologi.nama_teknologi,
                "bobot":
                    bobot_list
            })
            print(data_teknologi)
        # ==========================
        # UPDATE BOBOT KRITERIA
        # ==========================

        repo_bobot = BobotKriteriaRepository(
            connection
        )

        KRITERIA_MAPPING = {

            "processor": "KRIT_0001",
            "ram": "KRIT_0002",
            "storage": "KRIT_0003",
            "berat": "KRIT_0004",
            "layar": "KRIT_0005",
            "baterai": "KRIT_0006"

        }

        role_teknologi_list = (

            RoleTeknologi.objects

            .filter(
                role=role
            )

        )

        for role_teknologi in role_teknologi_list:

            for nama_kriteria, id_kriteria in (

                KRITERIA_MAPPING.items()

            ):

                field_name = (

                    f"{nama_kriteria}_weight_"
                    f"{role_teknologi.teknologi.id_teknologi}"

                )

                nilai_bobot = request.POST.get(
                    field_name
                )

                print(
                    field_name,
                    "=",
                    nilai_bobot
                )

                if nilai_bobot:

                    dto = BobotKriteriaDTO(

                        id_role_teknologi=
                            role_teknologi
                            .id_role_teknologi,

                        id_kriteria=
                            id_kriteria,

                        nilai_bobot=
                            float(nilai_bobot)

                    )

                    repo_bobot.update_bobot_role_teknologi(
                        dto
                    )

                return JsonResponse({

                    "id_role":
                        role.id_role,

                    "nama_role":
                        role.nama_role,

                    "min_ram":
                        role.min_ram,

                    "min_storage":
                        role.min_storage,

                    "min_processor_score":
                        role.min_processor_score,
                    "teknologi":
                        data_teknologi
                })
    if request.method == "POST":

        try:

            with transaction.atomic():

                # ==========================
                # UPDATE ROLE
                # ==========================

                nama_role = request.POST.get("nama_role", "").strip()
                if Role.objects.filter(nama_role__iexact=nama_role).exclude(id_role=role.id_role).exists():
                    raise Exception(f"Role dengan nama '{nama_role}' sudah ada.")

                role.nama_role = nama_role

                role.min_ram = int(
                    request.POST.get(
                        "min_ram",
                        0
                    )
                )

                role.min_storage = int(
                    request.POST.get(
                        "min_storage",
                        0
                    )
                )

                role.min_processor_score = int(
                    request.POST.get(
                        "min_processor_score",
                        0
                    )
                )

                role.save()

                # ==========================
                # UPDATE BOBOT
                # ==========================

                repo_bobot = (
                    BobotKriteriaRepository(
                        connection
                    )
                )

                KRITERIA_MAPPING = {

                    "processor":
                        "KRIT_0001",

                    "ram":
                        "KRIT_0002",

                    "storage":
                        "KRIT_0003",

                    "berat":
                        "KRIT_0004",

                    "layar":
                        "KRIT_0005",

                    "baterai":
                        "KRIT_0006"

                }

                role_teknologi_list = (

                    RoleTeknologi.objects

                    .filter(
                        role=role
                    )

                )

                for role_teknologi in (

                    role_teknologi_list

                ):

                    for (
                        nama_kriteria,
                        id_kriteria
                    ) in (
                        KRITERIA_MAPPING.items()
                    ):

                        field_name = (

                            f"{nama_kriteria}_weight_"
                            f"{role_teknologi.teknologi.id_teknologi}"

                        )

                        nilai_bobot = (
                            request.POST.get(
                                field_name
                            )
                        )

                        print(
                            field_name,
                            "=",
                            nilai_bobot
                        )

                        if nilai_bobot:

                            dto = (
                                BobotKriteriaDTO(

                                    id_role_teknologi=

                                    role_teknologi
                                    .id_role_teknologi,

                                    id_kriteria=
                                    id_kriteria,

                                    nilai_bobot=
                                    float(
                                        nilai_bobot
                                    )

                                )
                            )

                            repo_bobot.update_bobot_role_teknologi(
                                dto
                            )

            messages.success(
                request,
                "Role berhasil diperbarui."
            )

        except Exception as e:

            messages.error(
                request,
                f"Gagal update role: {str(e)}"
            )

        return redirect(
            "manajemenroleteknologi_it"
        )
    
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

def _generate_user_id():
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

    list_user = User.objects.all().order_by('id_user')
    total_user = list_user.count()
    total_hc = list_user.filter(role='HC').count()
    total_it = list_user.filter(role='IT').count()
    total_talent = list_user.filter(role='Talent').count()

    context = {
        'list_user': list_user,
        'total_user': total_user,
        'total_hc': total_hc,
        'total_it': total_it,
        'total_talent': total_talent,
    }
    return render(request, 'hc/user/manajemenuser_hc.html', context)


def tambahuser_hc_view(request):
    """Halaman form tambah pengguna baru. ID digenerate otomatis."""
    from inventori.models import User

    if request.method == 'POST':
        nama                = request.POST.get('nama', '').strip()
        email               = request.POST.get('email', '').strip() or None
        role                = request.POST.get('role', '').strip()
        password            = request.POST.get('password', '')
        konfirmasi_password = request.POST.get('konfirmasi_password', '')

        form_data = {'nama': nama, 'email': email, 'role': role}

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
            new_id = _generate_user_id()
            User.objects.create(
                id_user=new_id,
                nama=nama,
                email=email,
                role=role,
                password=password,
            )
            messages.success(request, f'Pengguna "{nama}" ({role}) berhasil ditambahkan dengan ID {new_id}.')
            return redirect('manajemenuser_hc')

        except Exception as e:
            messages.error(request, f'Gagal menambahkan pengguna: {str(e)}')

    return render(request, 'hc/user/tambahuser_hc.html', {'form_data': {}})


def edit_user_hc_view(request):
    """Edit data pengguna (nama, email, role, password)."""
    from inventori.models import User

    if request.method == 'POST':
        id_user  = request.POST.get('id_user', '').strip()
        nama     = request.POST.get('nama', '').strip()
        email    = request.POST.get('email', '').strip() or None
        role     = request.POST.get('role', '').strip()
        password = request.POST.get('password', '')

        if not id_user or not nama or not role:
            messages.error(request, 'Data tidak lengkap.')
            return redirect('manajemenuser_hc')

        try:
            user = User.objects.get(id_user=id_user)
            user.nama = nama
            user.email = email
            user.role = role
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

