import pytest

from tabulate import tabulate

from core.db import get_connection

from dss.services.service_saw import Servicesaw


@pytest.fixture(scope="module")
def service():
    conn = get_connection()
    return Servicesaw(conn)


def test_preprocessing_inventori(service):

    raw = service.repoInventori.ambil_laptop()

    result = service.servisPD.preprocessing(raw)

    print(
        tabulate(
            result[:10],
            headers="keys",
            tablefmt="grid"
        )
    )

    assert len(result) > 0

    row = result[0]

    assert "processor" in row
    assert "ram" in row
    assert "storage" in row
    assert "layar" in row


def test_preprocessing_pengadaan(service):

    raw = service.repoPengadaan.ambil_laptop_pengadaan()

    result = service.servisPD.preprocessing(raw)

    print(
        tabulate(
            result[:10],
            headers="keys",
            tablefmt="grid"
        )
    )

    assert len(result) > 0

    row = result[0]

    assert "processor" in row
    assert "ram" in row
    assert "storage" in row