from ..repositories.dto.dto_dss_proses import DssProsesDTO
from ..repositories.dto.dto_alternatif_dss import AlternatifDssDTO
from ..repositories.interface.interface_dss_proses import IDssProssesRepositoryImpl
from ..repositories.interface.interface_alternatif_dss import IAlternatifDssImpl

from datetime import datetime
from decimal import Decimal
from collections import defaultdict

from django.db import transaction

from dss.services.service_swara import ServiceSwara
from dss.services.service_preposesdata import PreprocessingService
from dss.services.service_agregiasi import AggregationService
from dss.services.service_normalisasi import NormalizationService
from dss.services.service_saw import Servicesaw

from dss.repositories.repositori_kriteria import KriteriaRepository
from dss.repositories.repositori_bobot_kriteria import BobotKriteriaRepository

from dss.repositories.repositori_dss_proses import DssprossesRepository
from dss.repositories.dto.dto_dss_proses import DssProsesDTO

from dss.repositories.repositori_alternatif_dss import AlternatifDssRepository
from dss.repositories.dto.dto_alternatif_dss import AlternatifDssDTO

from dss.repositories.repositori_laptop_altenatif import LaptopAlternatifRepository
from dss.repositories.dto.dto_laptop_alternatif import LaptopAlternatifDTO

from dss.repositories.repositori_hasil_saw import HasilSawRepository
from dss.repositories.dto.dto_hasil_saw import HasilSAWDTO

from dss.repositories.repositori_detail_hasil_saw import DetailHasilSawRepository
from dss.repositories.dto.dto_detail_hasil_saw import DetailHasilSawDTO

from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository
from dss.repositories.repositori_laptop_pengadaan import LaptopPengadaanRepository

class DssProsesService:
    def __init__(
        self,
        dss_repo: IDssProssesRepositoryImpl,
        alternatif_repo: IAlternatifDssImpl,
        swara_service: ServiceSwara,
        preprocessing_service: PreprocessingService,
        aggregation_service: AggregationService,
        normalization_service: NormalizationService,
        repo_dss_process: DssprossesRepository,
        repo_alternatif_dss: AlternatifDssRepository,
        repo_laptop_alternatif: LaptopAlternatifRepository,
        repo_hasil_saw: HasilSawRepository,
        repo_detail_hasil_saw: DetailHasilSawRepository,
        repo_kriteria: KriteriaRepository,
        repo_bobot_kriteria: BobotKriteriaRepository,
        repo_inventori: LaptopInventoriRepository,
        repo_pengadaan: LaptopPengadaanRepository,
        saw_calculation_service: Servicesaw
    ):
        # SERVICES
        self.dss_repo = dss_repo
        self.alternatif_repo = alternatif_repo
        self.swaraService = swara_service
        self.preprocessingService = preprocessing_service
        self.aggregationService = aggregation_service
        self.normalizationService = normalization_service
        self.sawCalculationService = saw_calculation_service

        # REPOSITORIES
        self.repoDSSProcess = repo_dss_process
        self.repoAlternatifDSS = repo_alternatif_dss
        self.repoLaptopAlternatif = repo_laptop_alternatif
        self.repoHasilSAW = repo_hasil_saw
        self.repoDetailHasilSAW = repo_detail_hasil_saw
        self.repoKriteria = repo_kriteria
        self.repoBobotKriteria = repo_bobot_kriteria
        self.repoInventori = repo_inventori
        self.repoPengadaan = repo_pengadaan
        
    def buat_proses_dss(self, data: DssProsesDTO):
        if not data.id_user:
            raise ValueError("ID User wajib diisi")

        if not data.role_dss:
            raise ValueError("Role DSS wajib diisi")

        return self.dss_repo.tambah_dss_proses(data)

    def tambah_alternatif(self, data: AlternatifDssDTO):
        if not data.id_dss:
            raise ValueError("ID DSS wajib ada")

        if not data.id_alternatif:
            raise ValueError("ID Alternatif wajib ada")

        return self.alternatif_repo.tambah_alternatif_dss(data)
    def proses_dss_lengkap(self, dss_data: DssProsesDTO, list_alternatif: map[AlternatifDssDTO]):
        hasil_dss = self.buat_proses_dss(dss_data)
        id_dss = dss_data.id_dss
        hasil_alternatif = []
        for alt in list_alternatif:
            alt.id_dss = id_dss
            res = self.tambah_alternatif(alt)
            hasil_alternatif.append(res)

        return {
            "dss": hasil_dss,
            "alternatif": hasil_alternatif
        }
        
    def get_semua_dss(self):
        return self.dss_repo.ambil_semua_dss_proses()
    
    def cari_alternatif(self, id_alternatif):
        return self.alternatif_repo.cari_alternatif_dss(id_alternatif)

    def hapus_alternatif(self, id_alternatif):
        return self.alternatif_repo.hapus_alternatif_dss(id_alternatif)

    def serialize_decimal(self, data):

        def convert(value):

            if isinstance(value, Decimal):
                return float(value)

            return value

        return [
            {
                k: convert(v)
                for k, v in dict(row).items()
            }
            for row in data
        ]
    def validate_project_roles(self, project_roles: list):

        if not project_roles:
            raise ValueError("Project roles tidak boleh kosong")

        total_percentage = sum(
            Decimal(str(r["persentase_role"]))
            for r in project_roles
        )

        if abs(total_percentage - Decimal("1")) > Decimal("0.000001"):
            raise ValueError(
                "Total persentase role harus = 1"
            )

        for role in project_roles:

            if role["persentase_role"] < 0:
                raise ValueError(
                    "Persentase role tidak boleh negatif"
                )

    def process_swara_per_role(self, project_roles: list):

        swara_per_role = {}

        for role in project_roles:

            role_id = role["id_role"]

            hasil_swara = self.swaraService.proses_swara(
                [role_id]
            )

            if hasil_swara["status"] != "success":

                raise Exception(
                    f"Gagal SWARA role {role_id}"
                )

            swara_per_role[role_id] = [
                {
                    "nama_kriteria": item["nama_kriteria"],
                    "nilai_swara": Decimal(
                        str(item["bobot_akhir"])
                    )
                }
                for item in hasil_swara["data"]["bobot_akhir"]
            ]

        return swara_per_role

    def process_final_weight(
        self,
        project_roles,
        swara_per_role
    ):

        aggregated_weights = (
            self.aggregationService.aggregate_role_weight(
                project_roles,
                swara_per_role
            )
        )

        normalized_weights = (
            self.normalizationService.normalize_weight(
                aggregated_weights
            )
        )

        valid = (
            self.normalizationService.validate_normalization(
                normalized_weights
            )
        )

        if not valid:
            raise Exception(
                "Normalisasi bobot tidak valid"
            )

        return {
            "aggregated": aggregated_weights,
            "normalized": normalized_weights
        }
    def save_initial_alternatives(
        self,
        data_raw,
        id_dss,
        sumber_data
    ):

        alternatif_list = []

        for item in data_raw:

            id_alt = (
                self.repoAlternatifDSS.tambah_alternatif_dss(
                    AlternatifDssDTO(
                        id_dss=id_dss,
                        id_laptop_inventori=item.get(
                            "id_laptop_inventori"
                        ),
                        id_laptop_pengadaan=item.get(
                            "id_laptop_pengadaan"
                        ),
                        sumber_data=sumber_data
                    )
                )
            )

            item["id"] = id_alt

            alternatif_list.append(item)

        return alternatif_list
    def process_saw_pipeline(
        self,
        alternatif_data,
        normalized_weights
    ):
        preprocessing_result = (
            self.preprocessingService.preprocessing(
                alternatif_data
            )
        )
        normalized_matrix = (
            self.sawCalculationService.normalize_decision_matrix(
                preprocessing_result
            )
        )
        saw_result = (
            self.sawCalculationService.calculate_saw_score(
                normalized_matrix,
                normalized_weights
            )
        )
        ranking = (
            self.sawCalculationService.ranking(
                saw_result
            )
        )

        for index, item in enumerate(ranking, start=1):

            item["rank"] = index

        return {
            "preprocessing": preprocessing_result,
            "normalized_matrix": normalized_matrix,
            "saw_result": saw_result,
            "ranking": ranking
        }
    def save_saw_result(
        self,
        id_dss,
        ranking
    ):

        id_hasil = (
            self.repoHasilSAW.buat_hasil_saw(
                HasilSAWDTO(
                    id_dss=id_dss
                )
            )
        )

        for item in ranking:

            self.repoDetailHasilSAW.tambah_detail_hasil_saw(
                DetailHasilSawDTO(
                    id_hasil=id_hasil,
                    nilai_normalisasi=item.get(
                        "normalisasi"
                    ),
                    nilai_rangking=item.get(
                        "skor"
                    ),
                    rangking=item.get(
                        "rank"
                    )
                )
            )

        return id_hasil
    def save_selected_laptop(
        self,
        ranking,
        id_dss,
        top_n=3
    ):

        selected = ranking[:top_n]

        for item in selected:

            data = None

            if "id_laptop_inventori" in item:

                data = self.repoInventori.ambil_by_id(
                    item["id_laptop_inventori"]
                )

            elif "id_laptop_pengadaan" in item:

                data = self.repoPengadaan.ambil_by_id(
                    item["id_laptop_pengadaan"]
                )

            if not data:
                continue

            self.repoLaptopAlternatif.tambah_laptop_alternatif(
                LaptopAlternatifDTO(
                    model_alternatif=data.get("model")
                    or data.get("model_pengadaan"),

                    brand_alternatif=data.get("brand")
                    or data.get("brand_pengadaan"),

                    id_dss=id_dss
                )
            )

    @transaction.atomic
    def process_dss_saw(
        self,
        id_user,
        id_bobot,
        sumber_data,
        filter_data,
        project_roles,
        debug=False
    ):

        self.validate_project_roles(
            project_roles
        )
        id_dss = self.repoDSSProcess.tambah_dss_proses(
            DssProsesDTO(
                id_user=id_user,
                id_bobot=id_bobot,
                role_dss=",".join(
                    [
                        str(r["id_role"])
                        for r in project_roles
                    ]
                ),
                jenis_dss="SAW",
                create_at=datetime.now()
            )
        )
        hasil_filter = (
            self.preprocessingService.filtering_data(
                sumber_data,
                filter_data
            )
        )

        if hasil_filter["status"] != "success":

            raise Exception(
                hasil_filter["message"]
            )
        data_raw = hasil_filter["data_raw"]
        alternatif_list = (
            self.save_initial_alternatives(
                data_raw,
                id_dss,
                sumber_data
            )
        )
        swara_per_role = (
            self.process_swara_per_role(
                project_roles
            )
        )
        weight_result = (
            self.process_final_weight(
                project_roles,
                swara_per_role
            )
        )
        normalized_weights = (
            weight_result["normalized"]
        )
        saw_pipeline_result = (
            self.process_saw_pipeline(
                alternatif_list,
                normalized_weights
            )
        )
        ranking = (
            saw_pipeline_result["ranking"]
        )
        id_hasil = (
            self.save_saw_result(
                id_dss,
                ranking
            )
        )
        self.save_selected_laptop(
            ranking,
            id_dss,
            top_n=3
        )
        if debug:

            return {
                "status": "success",

                "debug": {

                    "swara_per_role": swara_per_role,

                    "aggregated_weight":
                        weight_result["aggregated"],

                    "normalized_weight":
                        normalized_weights,

                    "pipeline":
                        saw_pipeline_result
                }
            }

        return {
            "status": "success",
            "meta": {
                "id_dss": id_dss,
                "id_hasil": id_hasil,
                "total_data": len(ranking)
            },
            "data": {
                "ranking": ranking
            }
        }