from urllib import request

from django.shortcuts import render, redirect
from django.http import HttpResponse

from dss.models import BobotKriteria
from dss.repositories.repositori_bobot_kriteria import BobotKriteriaRepository
from dss.repositories.repositori_bobot_kriteria import BobotKriteriaRepository
from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository
from .db import get_connection

# ==========================================
# 1. HUMAN CAPITAL (HC) VIEWS
# ==========================================

from inventori.models import LaptopInventori, Processor, RAM, Storage, User
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
    RoleTeknologi
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
        semua_pengajuan.sort(key=lambda x: x.tanggal_pengajuan, reverse=True)
        
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
            'total_siap_proses': total_siap_proses,
            'total_dikonfigurasi': total_dikonfigurasi,
            'total_selesai': total_selesai,
            'total_mendesak': total_mendesak,
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

        print("ACTION =", action)

        if action == "load":
            return redirect(
                "inputkriteria_hc"
            )

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
                    )
            }

            print(
                "REDIRECT KE HASIL DSS"
            )

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

    context = {
        "projects": projects,
        "role_teknologi": role_teknologi,
        "role_requirement": role_requirement,
        "bobot_role": bobot_role,
        "selected_project": selected_project,
        "selected_role_teknologi": selected_role_teknologi
    }
    return render(
        request,
        "hc/dss/inputkriteria_hc.html",
        context
    )

def hasilrekomendasi_hc_view(request):

    try:
        conn = get_connection()
        repo_laptop = LaptopInventoriRepository(conn)
        selected_role_teknologi = request.session.get(
            "selected_role_teknologi"
        )

        minimum_requirement = request.session.get(
            "minimum_requirement",
            {}
        )

        if not selected_role_teknologi:

            messages.error(
                request,
                "Role teknologi belum dipilih"
            )

            return redirect(
                "inputkriteria_hc"
            )

        roletek = (
            RoleTeknologi.objects
            .select_related("role")
            .get(
                id_role_teknologi=
                selected_role_teknologi
            )
        )

        repo_bobot = BobotKriteriaRepository(conn)

        hasil = repo_bobot.cari_bobot_kriteria_by_roles(
            [roletek.role.nama_role]
        )

        print("=" * 50)
        print("HASIL BOBOT")
        print(hasil)
        print("=" * 50)

        role_id = roletek.role.id_role

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

        service = Servicesaw(conn)

        hasil = service.proses_dss_saw(
            id_user="USR_0001",
            id_bobot=selected_role_teknologi,
            sumber_data="inventori",
            filter_data=filter_data,
            role=[role_id],
            debug=True
        )
        print("\n=== HASIL SERVICE ===")
        print(hasil)
        print(type(hasil))

        if hasil.get("status") != "success":

            print("\n=== ERROR DSS ===")
            print(hasil)

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

        ranking_sesuai = (
            hasil["data"]
            ["rekomendasi_sesuai_role"]
            ["ranking"]
        )

        ranking_alternatif = (
            hasil["data"]
            ["alternatif_lain"]
            ["ranking"]
        )    
        # print("\n=== TEST DETAIL ===")
        # print(
        #     repo_laptop.ambil_spek_laptop(
        #         ranking_sesuai[9]["id"]
        #     )
        # )
        # print("\n=== RANKING PERTAMA ===")
        # print(ranking_sesuai[0])

        for ranking_list in [ranking_sesuai, ranking_alternatif]:

            for item in ranking_list:

                laptop = repo_laptop.ambil_spek_laptop(
                    item["id"]
                )

                item["detail"] = {
                    "nama": item["id"],

                    "processor":
                        f"{laptop[0]} {laptop[2]}"
                        if laptop else "-",

                    "ram":
                        laptop[6]
                        if laptop else 0,

                    "storage":
                        laptop[8]
                        if laptop else 0,

                    "layar":
                        laptop[9]
                        if laptop else 0
                }

        context = {
            "ranking_sesuai": ranking_sesuai,
            "ranking_alternatif": ranking_alternatif,

            "top_3": ranking_sesuai[:3],

            "total_alternatif":
                len(ranking_sesuai),

            "rata_rata_harga": 0,

            "skor_tertinggi":
                ranking_sesuai[0]["skor"]
                if ranking_sesuai
                else 0,

            "warning":
                hasil.get("warning")
        }

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
    return render(request, 'hc/dss/detailrekomendasi_hc.html')

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
    conn = get_connection()

    try:
        from dss.services.service_saw import Servicesaw
        from inventori.models import RoleTeknologi
        from inventori.dto.dto_laptop_inventori import (
            FilterInventoriDTO
        )

        selected_role_teknologi = request.session.get(
            "selected_role_teknologi"
        )

        minimum_requirement = request.session.get(
            "minimum_requirement",
            {}
        )

        if not selected_role_teknologi:
            messages.error(
                request,
                "Role teknologi belum dipilih"
            )
            return redirect(
                "inputkriteria_it"
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

        service = Servicesaw(conn)

        hasil = service.proses_dss_saw(
            id_user="USR_0001",
            id_bobot=selected_role_teknologi,
            sumber_data="inventori",
            filter_data=filter_data,
            role=[role_id],
            debug=True
        )

        if hasil["status"] != "success":

            messages.error(
                request,
                hasil.get(
                    "message",
                    "Gagal proses DSS"
                )
            )

            return redirect(
                "inputkriteria_it"
            )

        ranking = (
            hasil["data"]
            ["rekomendasi_sesuai_role"]
            ["ranking"]
        )

        context = {
            "ranking": ranking,
            "top_3": ranking[:3],
            "total_alternatif":
                len(ranking),
            "skor_tertinggi":
                ranking[0]["skor"]
                if ranking else 0,
            "rata_rata_harga": 0,
            "warning":
                hasil.get("warning")
        }

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

            context = {
                'show_success_popup': True,
                'success_message': 'Pengajuan laptop berhasil dikirim dan sedang menunggu persetujuan.',
                'list_pengajuan': [],
                'total_pengajuan': 0,
            }

            return render(
                request,
                'talent/inventori/pengajuanlaptop_talent.html',
                context
            )
        semua_pengajuan = service.service_ambil_semua_pengajuan()

        if user_id:
            semua_pengajuan = [
                p for p in semua_pengajuan
                if getattr(p, 'id_user', None) == user_id
            ]

        semua_pengajuan.sort(
            key=lambda x: x.tanggal_pengajuan,
            reverse=True
        )

        context = {
            'list_pengajuan': semua_pengajuan,
            'total_pengajuan': len(semua_pengajuan),
            'show_success_popup': False,
            'show_error_popup': False,
        }

        return render(
            request,
            'talent/inventori/pengajuanlaptop_talent.html',
            context
        )

    except Exception as e:

        context = {
            'show_error_popup': True,
            'error_message': str(e),
            'list_pengajuan': [],
            'total_pengajuan': 0,
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

            # Update status laptop ke dipinjam
            laptop = LaptopInventori.objects.get(id_laptop_inventori=laptop_id)
            laptop.status = 'dipinjam'
            laptop.save()

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


