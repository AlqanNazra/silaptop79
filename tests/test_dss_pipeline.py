import pytest
import json

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


def test_dss_backend_inventori(service):

    result = service.proses_dss_saw(
        id_user="USR_0001",
        id_bobot="BOBOT_0001",
        sumber_data="inventori",
        filter_data=FilterInventoriDTO(),
        role=["Backend Developer"],
        debug=True
    )

    print(
        json.dumps(
            result,
            indent=4,
            default=str
        )
    )

    assert result["status"] == "success"

    ranking = result["data"]["ranking"]

    print(
        tabulate(
            ranking[:10],
            headers="keys",
            tablefmt="grid"
        )
    )

    assert len(ranking) > 0


def test_dss_ai_pengadaan(service):

    result = service.proses_dss_saw(
        id_user="USR_0001",
        id_bobot="BOBOT_0001",
        sumber_data="pengadaan",
        filter_data=FilterPengadaanDTO(),
        role=["AI Engineer"],
        debug=True
    )

    assert result["status"] == "success"

    ranking = result["data"]["ranking"]

    print(
        tabulate(
            ranking[:10],
            headers="keys",
            tablefmt="grid"
        )
    )

    assert len(ranking) > 0


def test_dss_multi_role(service):

    result = service.proses_dss_saw(
        id_user="USR_0001",
        id_bobot="BOBOT_0001",
        sumber_data="inventori",
        filter_data=FilterInventoriDTO(),
        role=[
            "Backend Developer",
            "Frontend Developer"
        ],
        debug=True
    )

    assert result["status"] == "success"

    ranking = result["data"]["ranking"]

    print(
        tabulate(
            ranking[:10],
            headers="keys",
            tablefmt="grid"
        )
    )

    assert len(ranking) > 0