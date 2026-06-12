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
    return render(request, 'hc/inventori/manajemenlaptop_hc.html', context)


# @login_required
def pengajuan_page_view(request):
    """
    Halaman daftar pengajuan laptop.
    Mengambil data dari PengajuanService lalu render ke template.
    """
    try:
        service = PengajuanService()
        semua_pengajuan = service.service_ambil_semua_pengajuan()
        
        # Calculate stats
        total = len(semua_pengajuan)
        pending = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'pending')
        disetujui = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'approved')
        ditolak = sum(1 for p in semua_pengajuan if p.status and p.status.lower() == 'rejected')
        
        context = {
            'list_pengajuan': semua_pengajuan,
            'total_pengajuan': total,
            'total_pending': pending,
            'total_disetujui': disetujui,
            'total_ditolak': ditolak,
        }
    except Exception as e:
        messages.error(request, f'Gagal memuat data pengajuan: {str(e)}')
        context = {
            'list_pengajuan': [],
            'total_pengajuan': 0,
            'total_pending': 0,
            'total_disetujui': 0,
            'total_ditolak': 0,
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
            return redirect('inventori:manajemen_laptop')
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
                service = DeleteLaptopInventoriService()
                service.execute(id_laptop)
                messages.success(request, f'Laptop {laptop.nama_laptop} berhasil dihapus.')
                return redirect('inventori:manajemen_laptop')
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
                return redirect('inventori:detaillaptop_hc', id_laptop=id_laptop)
            except Exception as e:
                messages.error(request, f'Gagal update: {str(e)}')

    context = {
        'laptop': laptop,
        'processors': processors,
        'rams': rams,
        'storages': storages,
    }
    return render(request, 'hc/inventori/detaillaptop_hc.html', context)

# @login_required
def detailpengajuan_hc_view(request):
    id_pengajuan = request.GET.get('id')
    if not id_pengajuan:
        messages.error(request, 'ID Pengajuan tidak diberikan.')
        return redirect('inventori:pengajuanlaptop_hc')

    try:
        service = PengajuanService()
        pengajuan = service.service_cari_pengajuan_by_id(id_pengajuan)
        
        if not pengajuan:
            messages.error(request, 'Data pengajuan tidak ditemukan.')
            return redirect('inventori:pengajuanlaptop_hc')

        from inventori.models import User
        user_obj = User.objects.filter(id_user=pengajuan.id_user).first()
        pengajuan.user_nama = user_obj.nama if user_obj else pengajuan.id_user

        if request.method == 'POST':
            action = request.POST.get('action')
            if action in ['approved', 'rejected']:
                from inventori.dto.dto_pengajuan import PengajuanDTO
                # Get user ID safely
                user_id = request.user.id_user if hasattr(request.user, 'id_user') else None
                
                dto = PengajuanDTO(
                    id_pengajuan=id_pengajuan,
                    status=action,
                    approved_by=user_id
                )
                service.service_approve_pengajuan(dto)
                messages.success(request, f'Pengajuan berhasil di-{action}.')
                return redirect('inventori:pengajuanlaptop_hc')

        context = {
            'pengajuan': pengajuan
        }
        return render(request, 'hc/inventori/detailpengajuan_hc.html', context)
        
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
        return redirect('inventori:pengajuanlaptop_hc')

# @login_required
def riwayatpeminjamanlaptop_hc_view(request):
    from inventori.services.service_peminjaman import PeminjamanService
    from inventori.models import User, LaptopInventori
    
    try:
        service = PeminjamanService()
        list_peminjaman = service.service_ambil_semua_peminjaman()
        
        users_dict = {u.id_user: u.nama for u in User.objects.all()}
        users_role_dict = {u.id_user: u.role for u in User.objects.all()}
        laptops_dict = {l.id_laptop_inventori: l.nama_laptop for l in LaptopInventori.objects.all()}
        
        for p in list_peminjaman:
            p.user_nama = users_dict.get(p.id_user, p.id_user)
            p.user_role = users_role_dict.get(p.id_user, "-")
            p.laptop_nama = laptops_dict.get(p.id_laptop_inventori, p.id_laptop_inventori)
            
        total_peminjaman = len(list_peminjaman)
        peminjam_terakhir = "-"
        
        # Sort by tanggal_pinjam desc
        sorted_p = sorted(list_peminjaman, key=lambda x: str(x.tanggal_pinjam) if x.tanggal_pinjam else "", reverse=True)
        if sorted_p:
            peminjam_terakhir = sorted_p[0].user_nama
            
        context = {
            'list_peminjaman': list_peminjaman,
            'total_peminjaman': total_peminjaman,
            'peminjam_terakhir': peminjam_terakhir,
        }
        return render(request, 'hc/inventori/riwayatpeminjamanlaptop_hc.html', context)
    except Exception as e:
        import traceback; traceback.print_exc()
        messages.error(request, f'Gagal memuat riwayat: {str(e)}')
        return redirect('inventori:manajemen_laptop')

# @login_required
def editdatalaptop_hc_view(request, id_laptop):
    try:
        laptop = LaptopInventori.objects.get(id_laptop_inventori=id_laptop)
    except LaptopInventori.DoesNotExist:
        messages.error(request, 'Laptop tidak ditemukan.')
        return redirect('inventori:manajemen_laptop')

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
            return redirect('inventori:detaillaptop_hc', id_laptop=id_laptop)
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
                perusahaan=body.get("perusahaan")
            )
            service = PengajuanService()
            result = service.tambah_pengajuan(dto)
            return JsonResponse({"message": result})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)


def list_pengajuan_view(request):
    if request.method == "GET":
        try:
            service = PengajuanService()
            data = service.ambil_semua()
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

    return render(request, "dashboard/laptop_dashboard.html", {
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
