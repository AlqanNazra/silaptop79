import pytest
from unittest.mock import MagicMock

from dss.services.service_swara import ServiceSwara


# =========================
# FIXTURE SERVICE
# =========================
@pytest.fixture
def service():
    service = ServiceSwara(conn=MagicMock())  
    service.repoBK = MagicMock()
    return service


# =========================
# MOCK DATA REAL (SESUAI DB KAMU)
# =========================
def get_mock_bobot_roles():
    return [
        # Backend Developer
        {"id_kriteria": "KRIT_0001", "nama_kriteria": "processor", "nilai_bobot": 0.35},
        {"id_kriteria": "KRIT_0002", "nama_kriteria": "ram", "nilai_bobot": 0.25},
        {"id_kriteria": "KRIT_0003", "nama_kriteria": "storage", "nilai_bobot": 0.15},
        {"id_kriteria": "KRIT_0004", "nama_kriteria": "berat", "nilai_bobot": 0.05, "tipe_kriteria": "cost"},
        {"id_kriteria": "KRIT_0005", "nama_kriteria": "layar", "nilai_bobot": 0.1},
        {"id_kriteria": "KRIT_0006", "nama_kriteria": "baterai", "nilai_bobot": 0.1},

        # Frontend Developer
        {"id_kriteria": "KRIT_0001", "nama_kriteria": "processor", "nilai_bobot": 0.2},
        {"id_kriteria": "KRIT_0002", "nama_kriteria": "ram", "nilai_bobot": 0.2},
        {"id_kriteria": "KRIT_0003", "nama_kriteria": "storage", "nilai_bobot": 0.1},
        {"id_kriteria": "KRIT_0004", "nama_kriteria": "berat", "nilai_bobot": 0.1, "tipe_kriteria": "cost"},
        {"id_kriteria": "KRIT_0005", "nama_kriteria": "layar", "nilai_bobot": 0.3},
        {"id_kriteria": "KRIT_0006", "nama_kriteria": "baterai", "nilai_bobot": 0.1},
    ]


# =========================
# TEST GABUNG + AVERAGE
# =========================
def test_ambil_dan_gabung_bobot_multi_role(service):
    service.repoBK.cari_bobot_kriteria_by_roles.return_value = get_mock_bobot_roles()

    result = service.ambil_dan_gabung_bobot(["Backend Developer", "Frontend Developer"])

    assert len(result) == 6

    # cek rata-rata processor (0.35 + 0.2)/2
    processor = next(r for r in result if r["nama_kriteria"] == "processor")
    assert processor["nilai_bobot"] == pytest.approx(0.275)
    print("\nDATA MOCK:")
    print(get_mock_bobot_roles())

    print("\nRESULT:")
    print(result)


# =========================
# TEST SORTING
# =========================
def test_pengurutan_kriteria_real(service):
    service.repoBK.cari_bobot_kriteria_by_roles.return_value = get_mock_bobot_roles()

    sorted_kriteria, meta = service.pengurutan_kriteria(
        ["Backend Developer", "Frontend Developer"]
    )

    # harus descending
    assert sorted_kriteria[0][1] >= sorted_kriteria[1][1]

    # pastikan semua kriteria masuk
    assert len(sorted_kriteria) == 6
    assert "processor" in meta


# =========================
# TEST FULL SWARA
# =========================
def test_proses_swara_realcase(service):
    service.repoBK.cari_bobot_kriteria_by_roles.return_value = get_mock_bobot_roles()
    service.repoBK.update_nilai_swara = MagicMock(return_value=True)

    result = service.proses_swara(
        ["Backend Developer", "Frontend Developer"]
    )

    assert result["status"] == "success"

    data = result["data"]

    # 🔥 VALIDASI INTI SWARA
    total = sum([x["bobot_akhir"] for x in data["bobot_akhir"]])
    assert total == pytest.approx(1.0, rel=1e-3)

    # jumlah kriteria harus 6
    assert len(data["bobot_akhir"]) == 6


# =========================
# TEST EDGE CASE (BOBOT KOSONG)
# =========================
def test_proses_swara_empty(service):
    service.repoBK.cari_bobot_kriteria_by_roles.return_value = []

    result = service.proses_swara(["Backend Developer"])

    assert result["status"] == "error"

# =========================
# TEST MULTI ROLE LEBIH BANYAK
# =========================
def test_multi_role_complex(service):
    # tambahkan Data Scientist
    data = get_mock_bobot_roles() + [
        {"id_kriteria": "KRIT_0001", "nama_kriteria": "processor", "nilai_bobot": 0.4},
        {"id_kriteria": "KRIT_0002", "nama_kriteria": "ram", "nilai_bobot": 0.3},
        {"id_kriteria": "KRIT_0003", "nama_kriteria": "storage", "nilai_bobot": 0.15},
        {"id_kriteria": "KRIT_0004", "nama_kriteria": "berat", "nilai_bobot": 0.05, "tipe_kriteria": "cost"},
        {"id_kriteria": "KRIT_0005", "nama_kriteria": "layar", "nilai_bobot": 0.05},
        {"id_kriteria": "KRIT_0006", "nama_kriteria": "baterai", "nilai_bobot": 0.05},
    ]

    service.repoBK.cari_bobot_kriteria_by_roles.return_value = data
    service.repoBK.update_nilai_swara = MagicMock()

    result = service.proses_swara(
        ["Backend Developer", "Frontend Developer", "Data Scientist"]
    )

    assert result["status"] == "success"
    # print("\n=== HASIL SWARA ===")
    # print(result)

    total = sum([x["bobot_akhir"] for x in result["data"]["bobot_akhir"]])
    assert total == pytest.approx(1.0, rel=1e-3)
    
# =========================
# TEST SWARA + Database
# =========================

# def test_swara_with_db():
#     from db import get_connection
#     from dss.services.service_swara import ServiceSwara

#     conn = get_connection()
#     service = ServiceSwara(conn)

#     result = service.proses_swara(["Backend Developer", "Frontend Developer"])
#     print(result)
#     assert result["status"] == "success"


    