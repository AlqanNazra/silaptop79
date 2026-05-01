import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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
            # Ambil detail spek laptop
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
