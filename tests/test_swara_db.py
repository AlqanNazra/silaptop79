import pytest
from db import get_connection
from dss.services.service_swara import ServiceSwara


@pytest.fixture(scope="module")
def service_db():
    conn = get_connection()
    service = ServiceSwara(conn)
    return service


def test_proses_swara_db(service_db):
    result = service_db.proses_swara(
        ["Backend Developer", "Frontend Developer"]
    )

    print("\nHASIL DB:", result)
    assert False

    assert result["status"] == "success"

    data = result["data"]

    # total bobot harus = 1
    total = sum([x["bobot_akhir"] for x in data["bobot_akhir"]])
    assert total == pytest.approx(1.0, rel=1e-3)

    # minimal ada kriteria
    assert len(data["bobot_akhir"]) > 0