import pytest
import json
from tabulate import tabulate
from db import get_connection
from dss.services.service_swara import ServiceSwara


@pytest.fixture(scope="module")
def service_db():
    conn = get_connection()
    return ServiceSwara(conn)


def test_proses_swara_db(service_db):
    result = service_db.proses_swara(
        ["Backend Developer", "Frontend Developer"]
    )

    print("\n=== HASIL SWARA (JSON) ===")
    print(json.dumps(result, indent=4))

    assert result["status"] == "success"

    data = result["data"]

    # 🔥 tampilkan tabel (buat laporan TA)
    print("\n Note: untuk input masih berbentuk desimal belum berbentuk numerik")
    print("\n=== BOBOT AKHIR (TABLE) ===")
    print(tabulate(
        data["bobot_akhir"],
        headers="keys",
        tablefmt="grid"
    ))

    # validasi total = 1
    total = sum([x["bobot_akhir"] for x in data["bobot_akhir"]])
    assert total == pytest.approx(1.0, rel=1e-3)

    # minimal ada kriteria
    assert len(data["bobot_akhir"]) > 0