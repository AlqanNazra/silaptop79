import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "silaptop79.settings"
)

django.setup()

import pytest

from core.db import get_connection

from dss.services.service_saw import Servicesaw

from inventori.repositories.dto.dto_laptop_inventori import (
    FilterInventoriDTO
)


@pytest.fixture(scope="module")
def service():
    conn = get_connection()
    return Servicesaw(conn)


def test_dss_save_result(service):

    result = service.proses_dss_saw(
        id_user="USR_0001",
        id_bobot="BOBOT_0001",
        sumber_data="inventori",
        filter_data=FilterInventoriDTO(),
        role=["ROLE_0002"],
        debug=False
    )

    print(result)

    assert result["status"] == "success"

    meta = result["meta"]

    assert meta["id_dss"] is not None

    assert (
        meta["id_hasil_role"] is not None
        or meta["id_hasil_fallback"] is not None
    )