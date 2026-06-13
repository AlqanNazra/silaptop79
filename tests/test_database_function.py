import pytest
from tabulate import tabulate

from core.db import get_connection

from dss.services.service_saw import Servicesaw

from inventori.repositories.dto.dto_laptop_inventori import (
    FilterInventoriDTO
)

from dss.repositories.dto.dto_laptop_pengadaan import (
    FilterPengadaanDTO
)


@pytest.fixture(scope="module")
def service():
    conn = get_connection()
    return Servicesaw(conn)


def test_get_inventori(service):

    data = service.repoInventori.ambil_laptop()

    print(
        tabulate(
            data[:5],
            headers="keys",
            tablefmt="grid"
        )
    )

    assert len(data) > 0

    row = data[0]

    assert "processor_score" in row
    assert "ram_kapasitas" in row
    assert "storage_kapasitas" in row


def test_get_pengadaan(service):

    data = service.repoPengadaan.ambil_laptop_pengadaan()

    print(
        tabulate(
            data[:5],
            headers="keys",
            tablefmt="grid"
        )
    )

    assert len(data) > 0

    row = data[0]

    assert "processor_score" in row
    assert "ram_kapasitas" in row
    assert "storage_kapasitas" in row


def test_filter_inventori_processor(service):

    dto = FilterInventoriDTO(
        min_processor_score=80
    )

    result = service.repoInventori.filter_inventori(dto)

    print(
        tabulate(
            result,
            headers="keys",
            tablefmt="grid"
        )
    )

    assert len(result) > 0

    for row in result:
        assert row["processor_score"] >= 80


def test_filter_pengadaan_processor(service):

    dto = FilterPengadaanDTO(
        min_processor_score=80
    )

    result = service.repoPengadaan.filter_pengadaan(dto)

    print(
        tabulate(
            result,
            headers="keys",
            tablefmt="grid"
        )
    )

    assert len(result) > 0

    for row in result:
        assert row["processor_score"] >= 80