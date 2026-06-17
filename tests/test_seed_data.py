import pytest

from core.db import get_connection

from dss.services.service_saw import Servicesaw


@pytest.fixture(scope="module")
def service():
    conn = get_connection()
    return Servicesaw(conn)


def test_kriteria_exists(service):

    data = service.repoK.ambil_kriteria()

    print("\n=== KRITERIA ===")
    print(data)

    assert data is not None
    assert len(data) == 6


def test_bobot_exists(service):

    data = service.repoBK.ambil_semua()

    print("\n=== BOBOT ===")
    print(data)

    assert data is not None
    assert len(data) > 0


def test_role_exists(service):

    data = service.servisBK.repoRole.ambil_semua()

    print("\n=== ROLE ===")
    print(data)

    assert data is not None
    assert len(data) >= 5


def test_inventori_exists(service):

    data = service.repoInventori.ambil_laptop()

    print("\n=== INVENTORI ===")
    print(f"Total : {len(data)}")

    assert len(data) > 0


def test_pengadaan_exists(service):

    data = service.repoPengadaan.ambil_laptop_pengadaan()

    print("\n=== PENGADAAN ===")
    print(f"Total : {len(data)}")

    assert len(data) > 0