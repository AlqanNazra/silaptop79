import logging

from django.db import transaction

# from apps.teknologi.validations.teknologi_validation import (
#     TeknologiValidation
# )

logger = logging.getLogger(__name__)


class TeknologiService:

    def __init__(
        self,
        teknologi_repo,
        conn
    ):
        self.teknologi_repo = teknologi_repo
        self.conn = conn

    # ====================================
    # TAMBAH
    # ====================================
    def tambah(self, data):

        # TeknologiValidation.validate_nama_teknologi(
        #     data.nama_teknologi
        # )
        try:
            with transaction.atomic():
                result = self.teknologi_repo.tambah_teknologi(
                    data
                )
                self.conn.commit()
                logger.info(
                    f"Tambah teknologi sukses: "
                    f"{data.nama_teknologi}"
                )
                return {
                    "success": True,
                    "message": "Berhasil tambah teknologi"
                }
        except Exception as e:
            self.conn.rollback()
            logger.error(str(e))
            raise e

    # ====================================
    # UPDATE
    # ====================================
    def update(self, data):
        try:
            with transaction.atomic():
                result = self.teknologi_repo.update_teknologi(
                    data
                )
                self.conn.commit()
                return {
                    "success": True,
                    "message": "Berhasil update teknologi"
                }
        except Exception as e:
            self.conn.rollback()
            logger.error(str(e))
            raise e

    # ====================================
    # HAPUS
    # ====================================
    def hapus_teknologi(self, id_teknologi):
        try:
            with transaction.atomic():
                result = (self.teknologi_repo.hapus_teknologi(id_teknologi))
                self.conn.commit()
                return {"success": result,"message": "Berhasil hapus teknologi"}
        except Exception as e:
            self.conn.rollback()
            logger.error(str(e))
            raise Exception(str(e))

    # ====================================
    # GET COMPATIBILITY
    # ====================================
    def getCompatibility(self, nama_teknologi):

        return self.teknologi_repo.get_compatibility(
            nama_teknologi
        )

    # ====================================
    # VALIDATE VERSION
    # ====================================
    def validateVersion(self, version):

        # TeknologiValidation.validate_version(version)

        return {
            "success": True,
            "message": "Versi valid"
        }

    # ====================================
    # GET RECOMMENDED LAPTOP
    # ====================================
    def getRecommendedLaptop(
        self,
        nama_teknologi
    ):

        compatibility = self.getCompatibility(
            nama_teknologi
        )

        if not compatibility:
            raise Exception(
                "Compatibility tidak ditemukan"
            )

        # simulasi DSS
        return {
            "teknologi": nama_teknologi,
            "minimal_ram": compatibility["minimal_ram"],
            "minimal_core": compatibility["minimal_core"],
            "gpu_required": compatibility["gpu_required"],
            "recommended_laptop": [
                {
                    "nama": "Lenovo Legion",
                    "score": 0.95
                },
                {
                    "nama": "ASUS ROG",
                    "score": 0.92
                }
            ]
        }
    def ambil_semua(self):
        return (self.teknologi_repo.get_all_teknologi())