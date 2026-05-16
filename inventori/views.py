import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render

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
# HELPER: Response standar
# =============================================
def success_response(data=None, message="Berhasil", status=200):
    return JsonResponse({"status": "success", "message": message, "data": data}, status=status, safe=False)

def error_response(message="Terjadi kesalahan", status=400):
    return JsonResponse({"status": "error", "message": message}, status=status)

def _parse_body(request):
    """Parse JSON body dari request"""
    return json.loads(request.body)


# =============================================================================
#   1. PROCESSOR CRUD (Memakai DTO -> Service -> Repository)
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
            res = service.tambah_processor(dto)
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
#   2. LAPTOP INVENTORI CRUD (Memakai DTO -> Service -> Repository)
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
            # Jika PUT, anggap update kondisi dan status sebagai contoh
            # Jika mau update spek, sebaiknya endpoint berbeda
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

# Catatan: Fungsi CRUD lain untuk RAM, Storage, Peminjaman, Riwayat dapat 
# diimplementasikan menggunakan pola yang persis sama.

@csrf_exempt
def tambah_pengajuan_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            dto = PengajuanDTO(
                id_user=request.user.id_user,
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

@csrf_exempt
def tambah_pengajuan_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            dto = PengajuanDTO(
                id_user=request.user.id_user,
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

            return JsonResponse({
                "data": [d.__dict__ for d in data]
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def approve_pengajuan_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            dto = PengajuanDTO(
                id_pengajuan=body.get("id_pengajuan"),
                status=body.get("status"),  
                approved_by=request.user.id_user  
            )

            service = PengajuanService()
            result = service.approve_pengajuan(dto)

            return JsonResponse({"message": result})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def approve_dan_pinjam_view(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            # DTO Pengajuan
            dto_pengajuan = PengajuanDTO(
                id_pengajuan=body.get("id_pengajuan"),
                status="approved",
                approved_by=request.user.id_user
            )

            # DTO Peminjaman
            dto_peminjaman = PeminjamanDTO(
                id_user=body.get("id_user"),
                id_laptop_inventori=body.get("id_laptop_inventori"),
                id_pengajuan=body.get("id_pengajuan"),
                tanggal_pinjam=body.get("tanggal_pinjam"),
                tanggal_kembali=body.get("tanggal_kembali"),
                keterangan=body.get("keterangan")
            )

            service = PengajuanService()
            result = service.approve_dan_pinjam(dto_pengajuan, dto_peminjaman)

            return JsonResponse({"message": result})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)

# =============================================================================
#   4. VIews Peminjaman 
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

            return JsonResponse({
                "data": [d.__dict__ for d in data]
            })

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