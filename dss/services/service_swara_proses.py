from django.db import transaction

from dss.services.service_swara import ServiceSwara
from dss.services.service_agregiasi import AggregationService
from dss.services.service_normalisasi import NormalizationService
from dss.services.service_preposesdata import PreprocessingService
from dss.services.service_saw import Servicesaw


class DSSPipelineService:

    def __init__(
        self,
        conn,
        swara_service: ServiceSwara,
        aggregation_service: AggregationService,
        normalization_service: NormalizationService,
        preprocessing_service: PreprocessingService,
        saw_service: Servicesaw
    ):
        self.conn = conn
        self.swara_service = swara_service
        self.aggregation_service = aggregation_service
        self.normalization_service = normalization_service
        self.preprocessing_service = preprocessing_service
        self.saw_service = saw_service

    @transaction.atomic
    def proses_rekomendasi(
        self,
        project_roles: list,
        alternatif_laptop: list
    ):

        # ==========================================
        # 1. VALIDASI ROLE
        # ==========================================

        if not project_roles:
            raise ValueError("Project roles tidak boleh kosong")

        total_percentage = sum(
            r["persentase_role"]
            for r in project_roles
        )

        if abs(total_percentage - 1.0) > 0.0001:
            raise ValueError(
                "Total persentase role harus = 1"
            )

        # ==========================================
        # 2. SWARA PER ROLE
        # ==========================================

        swara_per_role = {}

        for role in project_roles:

            role_id = role["id_role"]

            hasil_swara = self.swara_service.proses_swara(
                [role_id]
            )

            if hasil_swara["status"] != "success":
                raise Exception(
                    f"Gagal proses SWARA role {role_id}"
                )

            swara_per_role[role_id] = [
                {
                    "nama_kriteria": item["nama_kriteria"],
                    "nilai_swara": item["bobot_akhir"]
                }
                for item in hasil_swara["data"]["bobot_akhir"]
            ]

        # ==========================================
        # 3. AGGREGATION
        # ==========================================

        aggregated_weights = (
            self.aggregation_service.aggregate_role_weight(
                project_roles,
                swara_per_role
            )
        )

        # ==========================================
        # 4. NORMALIZATION
        # ==========================================

        normalized_weights = (
            self.normalization_service.normalize_weight(
                aggregated_weights
            )
        )

        valid = (
            self.normalization_service.validate_normalization(
                normalized_weights
            )
        )

        if not valid:
            raise Exception(
                "Normalisasi bobot tidak valid"
            )

        # ==========================================
        # 5. PREPROCESSING ALTERNATIF
        # ==========================================

        processed_alternatives = (
            self.preprocessing_service.preprocessing(
                alternatif_laptop
            )
        )

        # ==========================================
        # 6. SAW RANKING
        # ==========================================

        ranking_result = self.saw_service.calculate_saw(
            processed_alternatives,
            normalized_weights
        )

        # ==========================================
        # 7. FINAL RESULT
        # ==========================================

        return {
            "status": "success",
            "weights": {
                "swara_per_role": swara_per_role,
                "aggregated": aggregated_weights,
                "normalized": normalized_weights
            },
            "ranking": ranking_result
        }