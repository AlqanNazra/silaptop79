import pytest
from unittest.mock import MagicMock

@pytest.fixture
def service(monkeypatch):

    # 🔥 PATCH Servicepreposesdata sebelum dipakai
    monkeypatch.setattr(
        "dss.services.service_saw.Servicepreposesdata",
        lambda conn: MagicMock()
    )

    from dss.services.service_saw import Servicesaw

    service = Servicesaw(conn=MagicMock())

    # override dependency
    service.repoK = MagicMock()
    service.repoBK = MagicMock()
    service.servisBK = MagicMock()
    service.servisPD = MagicMock()

    return service


# =========================
# MOCK DATA KRITERIA
# =========================
def get_mock_kriteria():
    return [
        {"nama_kriteria": "harga", "tipe_kriteria": "cost"},
        {"nama_kriteria": "ram", "tipe_kriteria": "benefit"},
        {"nama_kriteria": "storage", "tipe_kriteria": "benefit"},
        {"nama_kriteria": "berat", "tipe_kriteria": "cost"},
    ]


# =========================
# MOCK DATA PREPROCESS (HASIL PD)
# =========================
def get_mock_preprocessing():
    return [
        {"id": "LP_0001", "harga": 12500000, "ram": 16, "storage": 512, "berat": 1.4},
        {"id": "LP_0002", "harga": 15000000, "ram": 32, "storage": 1024, "berat": 1.5},
        {"id": "LP_0003", "harga": 10500000, "ram": 16, "storage": 512, "berat": 2.6},
    ]


# =========================
# MOCK BOBOT (HASIL SWARA)
# =========================
def get_mock_bobot():
    return {
        "harga": 0.3,
        "ram": 0.3,
        "storage": 0.2,
        "berat": 0.2,
    }


# =========================
# TEST NORMALISASI
# =========================
def test_normalisasi_saw(service):
    service.repoK.ambil_kriteria.return_value = get_mock_kriteria()

    data = get_mock_preprocessing()

    result = service.normalisasi_saw(data)

    assert len(result) == 3

    # cek range normalisasi
    for item in result:
        for k, v in item.items():
            if k != "id":
                assert 0 <= v <= 1

    print("\nNORMALISASI:")
    print(result)


# =========================
# TEST HITUNG SAW
# =========================
def test_hitung_saw(service):
    service.repoK.ambil_kriteria.return_value = get_mock_kriteria()
    service.get_bobot_saw = MagicMock(return_value=get_mock_bobot())

    data = service.normalisasi_saw(get_mock_preprocessing())
    result = service.hitung_saw_data(data, ["Backend"], "B1")

    assert len(result) == 3

    # skor harus ada
    for r in result:
        assert "skor" in r

    print("\nHASIL SAW:")
    print(result)


# =========================
# TEST RANKING
# =========================
def test_ranking(service):
    data = [
        {"id": "A", "skor": 0.5},
        {"id": "B", "skor": 0.8},
        {"id": "C", "skor": 0.3},
    ]

    result = service.ranking_saw(data)

    assert result[0]["skor"] >= result[1]["skor"]
    assert result[1]["skor"] >= result[2]["skor"]


# =========================
# TEST FULL DSS SAW
# =========================
def test_full_proses_dss_saw(service):
    # mock filtering
    service.servisPD.filtering_data.return_value = {
        "status": "success",
        "data_raw": get_mock_preprocessing()
    }

    # mock preprocessing
    service.servisPD.preprocessing.return_value = get_mock_preprocessing()

    service.repoK.ambil_kriteria.return_value = get_mock_kriteria()
    service.get_bobot_saw = MagicMock(return_value=get_mock_bobot())

    result = service.proses_dss_saw(
        sumber_data=[],
        filter_data={},
        role=["Backend"],
        id_bobot="B1"
    )

    assert result["status"] == "success"

    data = result["data"]

    assert "ranking" in data
    assert len(data["ranking"]) == 3

    print("\nFULL DSS RESULT:")
    print(data)


# =========================
# TEST EDGE CASE (DATA KOSONG)
# =========================
def test_empty_data(service):
    result = service.normalisasi_saw([])
    assert result == []


# =========================
# TEST AVERAGE GOLONGAN
# =========================
def test_average_golongan(service):
    service.repoBK.cari_bobot_kriteria_by_roles.side_effect = [
        {"golongan": "A", "harga": 0.3, "ram": 0.3},
        {"golongan": "A", "harga": 0.5, "ram": 0.5},
    ]

    result = service.hitung_average_golongan(["Backend", "Frontend"])

    assert "harga" in result
    assert result["harga"] == pytest.approx(0.4)


# =========================
# TEST WEIGHTED GOLONGAN
# =========================
def test_weighted_golongan(service):
    service.repoBK.cari_bobot_kriteria_by_roles.side_effect = [
        {"golongan": "A", "harga": 0.3, "ram": 0.3},
        {"golongan": "B", "harga": 0.5, "ram": 0.5},
    ]

    roles = [
        {"role": "Backend", "weight": 0.7},
        {"role": "Frontend", "weight": 0.3},
    ]

    result = service.hitung_weighted_golongan(roles)

    assert "harga" in result
    assert result["harga"] > 0