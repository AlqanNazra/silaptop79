from collections import defaultdict
from datetime import datetime

from dss.repositories.repositori_kriteria import KriteriaRepository
from dss.repositories.repositori_bobot_kriteria import BobotKriteriaRepository

from decimal import Decimal

# dss/services/service_agregiasi.py

class AggregationService:

    def __init__(self, conn):
        self.conn = conn
    def aggregate_role_weight(
        self,
        roles: list,
        swara_weights_per_role: dict
    ):
        if not roles:
            raise ValueError(
                "Roles tidak boleh kosong"
            )

        if not swara_weights_per_role:
            raise ValueError(
                "Data SWARA kosong"
            )
        total_weight = sum(
            role.get("weight", 0)
            for role in roles
        )

        if total_weight <= 0:
            raise ValueError(
                "Total weight harus > 0"
            )

        normalized_roles = []

        for role in roles:

            normalized_roles.append({
                "role": role["role"],
                "weight": (
                    role["weight"]
                    / total_weight
                )
            })
        hasil_agregasi = {}

        for role in normalized_roles:

            role_name = role["role"]
            role_weight = role["weight"]
            if role_name not in swara_weights_per_role:

                raise ValueError(
                    f"Hasil SWARA role "
                    f"'{role_name}' "
                    f"tidak ditemukan"
                )

            swara_data = (
                swara_weights_per_role[
                    role_name
                ]
            )
            for (
                nama_kriteria,
                bobot
            ) in swara_data.items():

                if nama_kriteria not in hasil_agregasi:

                    hasil_agregasi[
                        nama_kriteria
                    ] = 0

                hasil_agregasi[
                    nama_kriteria
                ] += (
                    bobot * role_weight
                )
        for k in hasil_agregasi:

            hasil_agregasi[k] = round(
                hasil_agregasi[k],
                6
            )

        return hasil_agregasi
    @staticmethod
    def validate_aggregation(
        aggregate_result: dict
    ):

        if not aggregate_result:
            return False

        total = sum(
            aggregate_result.values()
        )

        return total > 0

    @staticmethod
    def print_aggregate_result(
        aggregate_result: dict
    ):

        print(
            "\n=== HASIL AGGREGASI ==="
        )

        total = 0

        for (
            kriteria,
            nilai
        ) in aggregate_result.items():

            print(
                f"{kriteria} = {nilai}"
            )

            total += nilai

        print("\nTOTAL =", total)
    def aggregate_teknologi_role(
        self,
        list_hasil_teknologi
    ):

        if not list_hasil_teknologi:

            raise ValueError(
                "Data teknologi kosong"
            )

        hasil = {}

        counter = {}

        for teknologi in list_hasil_teknologi:

            for item in teknologi:

                nama = item[
                    "nama_kriteria"
                ]

                nilai = item[
                    "nilai_swara"
                ]

                if nama not in hasil:

                    hasil[nama] = 0
                    counter[nama] = 0

                hasil[nama] += nilai
                counter[nama] += 1

        for nama in hasil:

            hasil[nama] = round(
                hasil[nama]
                / counter[nama],
                6
            )

        return hasil