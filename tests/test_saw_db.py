import pytest
import json
from tabulate import tabulate

from core.db import get_connection
from dss.services.service_saw import Servicesaw
from dss.repositories.dto.dto_laptop_pengadaan import FilterPengadaanDTO
from inventori.repositories.dto.dto_laptop_inventori import FilterInventoriDTO


@pytest.fixture(scope="module")
def service():
    conn = get_connection()
    return Servicesaw(conn)


# =========================
# HELPER: FORMAT DATA
# =========================
def format_data_saw(rows, source="inventori"):
    hasil = []

    for r in rows:
        try:
            hasil.append({
                "id": r["id"],
                "processor": float(r["processor"]),
                "ram": float(r["ram"]),
                "storage": float(r["storage"]),
                "berat": float(r["berat"]),
                "layar": float(r["layar"]),
                "baterai": float(r["baterai"])
            })
        except Exception as e:
            print("SKIP DATA:", r, e)

    return hasil


# =========================
# TEST AMBIL DATA INVENTORI
# =========================
def test_ambil_data_inventori(service):
    data = service.repoInventori.ambil_laptop()

    print("\n=== DATA INVENTORI ===")
    print(data[:3])

    assert data is not None
    assert len(data) > 0


# =========================
# TEST AMBIL DATA PENGADAAN
# =========================
def test_ambil_data_pengadaan(service):
    data = service.repoPengadaan.ambil_laptop_pengadaan()

    print("\n=== DATA PENGADAAN ===")
    print(data[:3])

    assert data is not None
    assert len(data) > 0


# =========================
# TEST FULL DSS (INVENTORI)
# =========================

def test_dss_saw_inventori(service):
    filter_dto = FilterInventoriDTO()  
    result = service.proses_dss_saw(
        sumber_data="inventori",   
        filter_data=filter_dto,
        role=["Backend Developer", "Frontend Developer"],
        debug=False
    )

    print("\n=== DSS INVENTORI ===")
    print(json.dumps(result, indent=4, default=str))
    assert result["status"] == "success"

    ranking = result["data"]["ranking"]
    print("\n=== RANKING INVENTORI ===")
    print(tabulate(ranking, headers="keys", tablefmt="grid"))

    assert len(ranking) > 0

# =========================
# TEST FULL DSS (PENGADAAN)
# =========================
def test_dss_saw_pengadaan(service):
    filter_dto = FilterPengadaanDTO()  
    result = service.proses_dss_saw(
        sumber_data="pengadaan",   
        filter_data=filter_dto,
        role=["Backend Developer", "Frontend Developer"],
        debug=False
    )
    print("\n=== HASIL DSS PENGADAAN ===")
    print(json.dumps(result, indent=4, default=str))
    assert result["status"] == "success"

    ranking = result["data"]["ranking"]
    print("\n=== RANKING PENGADAAN ===")
    print(tabulate(ranking, headers="keys", tablefmt="grid"))

    assert len(ranking) > 0


# =========================
# TEST GABUNGAN (INVENTORI + PENGADAAN)
# =========================
# def test_dss_saw_combined(service):
#     inv = service.repoInventori.ambil_laptop()
#     peng = service.repoPengadaan.ambil_laptop_pengadaan()

#     data_inv = format_data_saw(inv)
#     data_peng = format_data_saw(peng)

#     combined = data_inv + data_peng

#     result = service.proses_dss_saw(
#         sumber_data=combined,
#         filter_data={},
#         role=["Backend Developer", "Frontend Developer"],
#         debug=False
#     )

#     print("\n=== HASIL DSS GABUNGAN ===")
#     print(json.dumps(result, indent=4))

#     ranking = result["data"]["ranking"]

#     print("\n=== RANKING FINAL (COMBINED) ===")
#     print(tabulate(ranking[:10], headers="keys", tablefmt="grid"))

#     assert result["status"] == "success"
#     assert len(ranking) > 0