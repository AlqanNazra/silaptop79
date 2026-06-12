import pytest
from unittest.mock import MagicMock


@pytest.fixture
def service(monkeypatch):
    # 🔥 PATCH class yang error
    monkeypatch.setattr(
        "dss.services.service_preposesdata.ILaptopInventoriRepository",
        lambda conn: MagicMock()
    )

    monkeypatch.setattr(
        "dss.services.service_preposesdata.ILaptopPengadaanRepositoryImpl",
        lambda conn: MagicMock()
    )

    from dss.services.service_preposesdata import Servicepreposesdata

    service = Servicepreposesdata(conn=MagicMock())

    return service


# =========================
# TEST EKSTRAK PROCESSOR
# =========================
def test_ekstrak_processor_intel(service):
    text = "Intel Core i7-1165G7"

    series, model, gen = service.ekstrak_processor(text)

    assert series == 7
    assert model == 1165
    assert gen == 11


def test_ekstrak_processor_amd(service):
    text = "AMD Ryzen 5 5600H"

    series, model, gen = service.ekstrak_processor(text)

    assert series == 5
    assert model == 5600
    assert gen == 5


def test_ekstrak_processor_apple(service):
    text = "Apple M2"

    series, model, gen = service.ekstrak_processor(text)

    assert series == "M2"
    assert gen == 2


# =========================
# TEST MAPPING PROCESSOR
# =========================
def test_mapping_processor_intel(service):
    score = service.mapping_processor(series=7, gen=11)

    assert score > 0


def test_mapping_processor_apple(service):
    score = service.mapping_processor(series="M2", gen=2)

    # sesuai logic: 8 + gen
    assert score == 10


def test_mapping_processor_none(service):
    score = service.mapping_processor(series=None, gen=None)

    assert score == 3  # default


# =========================
# TEST PREPROCESSING PROCESSOR
# =========================
def test_preprocessing_processor(service):
    data = [
        {"id": "LP1", "processor": "Intel Core i7-1165G7"},
        {"id": "LP2", "processor": "AMD Ryzen 5 5600H"},
    ]

    result = service.preprocessing_processor(data)

    assert len(result) == 2
    assert "processor" in result[0]

    # nilai harus numerik
    assert isinstance(result[0]["processor"], (int, float))


# =========================
# TEST PREPROCESSING FULL
# =========================
def test_preprocessing_full(service):
    data = [
        {
            "id": "LP1",
            "processor": "Intel Core i7-1165G7",
            "ram": 16,
            "storage": 512,
            "berat": 1.5,
            "ukuran_layar": 14,
            "baterai": 5000
        },
        {
            "id": "LP2",
            "processor": "AMD Ryzen 5 5600H",
            "ram": 32,
            "storage": 1024,
            "berat": 2.0,
            "ukuran_layar": 15.6,
            "baterai": 6000
        }
    ]

    result = service.preprocessing(data)

    assert len(result) == 2

    for item in result:
        assert "processor" in item
        assert "ram" in item
        assert "storage" in item
        assert "berat" in item
        assert "layar" in item
        assert "baterai" in item

        # processor harus sudah jadi skor
        assert isinstance(item["processor"], (int, float))


# =========================
# TEST EDGE CASE
# =========================
def test_preprocessing_empty(service):
    result = service.preprocessing([])

    assert result == []