import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages

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

@login_required
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
    return render(request, 'inventori/manajemenlaptop_hc.html', context)


@login_required
def pengajuan_page_view(request):
    """
    Halaman daftar pengajuan laptop.
    Mengambil data dari PengajuanService lalu render ke template.
    """
    try:
        service = PengajuanService()
        semua_pengajuan = service.ambil_semua_pengajuan()
        
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

    return render(request, 'inventori/pengajuanlaptop_hc.html', context)


@login_required
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
                ukuran_layar=request.POST.get('ukuran_layar') or None,
            )
            service = CreateLaptopInventoriService()
            service.execute(dto)
            messages.success(request, 'Laptop berhasil ditambahkan ke inventori!')
            return redirect('manajemenlaptop_hc')
        except Exception as e:
            messages.error(request, f'Gagal menambahkan laptop: {str(e)}')

    context = {
        'processors': processors,
        'rams': rams,
        'storages': storages,
    }
    return render(request, 'inventori/tambahlaptop_hc.html', context)


@login_required
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
        return redirect('manajemenlaptop_hc')

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
                return redirect('manajemenlaptop_hc')
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
                return redirect('detail_laptop', id_laptop=id_laptop)
            except Exception as e:
                messages.error(request, f'Gagal update: {str(e)}')

    context = {
        'laptop': laptop,
        'processors': processors,
        'rams': rams,
        'storages': storages,
    }
    return render(request, 'inventori/detail.html', context)

@login_required
def detailpengajuan_hc_view(request):
    return render(request, 'inventori/detailpengajuan_hc.html')

@login_required
def riwayatpeminjamanlaptop_hc_view(request):
    return render(request, 'inventori/riwayatpeminjamanlaptop_hc.html')

@login_required
def editdatalaptop_hc_view(request, id_laptop):
    return render(request, 'inventori/editdatalaptop_hc.html')


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