import logging

from django.db import transaction

logger = logging.getLogger(__name__)

class ProyekValidation:

    @staticmethod
    def validate_input(data):

        if not data.nama_proyek:
            raise ValueError(
                "Nama proyek wajib diisi"
            )

        if not data.user_perusahaan:
            raise ValueError(
                "Client perusahaan wajib diisi"
            )

        if data.mulai_proyek > data.akhir_proyek:
            raise ValueError(
                "Tanggal proyek tidak valid"
            )

        return True

class ProyekService:

    def __init__(
        self,
        proyek_repo,
        conn
    ):
        self.proyek_repo = proyek_repo
        self.conn = conn
    
        
    def tambah_proyek(self, data):
        ProyekValidation.validate_input(data)
        try:
            with transaction.atomic():
                id_proyek = (self.proyek_repo.tambah(data))
                
                print("ID DARI REPO =", id_proyek)
                print("TYPE =", type(id_proyek))
                
                self.conn.commit()
                return {
                    "success": True,
                    "id_proyek": id_proyek
                }
        except Exception as e:
            self.conn.rollback()
            raise Exception(str(e))
    def update_proyek(self, data):
        try:
            with transaction.atomic():
                is_exist = self.proyek_repo.validate(
                    data.id_proyek
                )
                if not is_exist:
                    raise Exception(
                        "Proyek tidak ditemukan"
                    )
                self.proyek_repo.update(data)
                # trigger DSS recalculation
                if hasattr(self, "calculate_project_requirement"):
                    self.calculate_project_requirement(
                        data.id_proyek
                    )
                self.conn.commit()
                return {
                    "success": True,
                    "message": "Berhasil update proyek"
                }

        except Exception as e:

            self.conn.rollback()

            raise Exception(str(e))

    def hapus_proyek(self,id_proyek):
        try:
            with transaction.atomic():
                result = (self.proyek_repo.hapus(id_proyek))
                self.conn.commit()
                logger.info(f"Berhasil hapus proyek "f"{id_proyek}")
                return {"success": result}

        except Exception as e:
            self.conn.rollback()
            logger.error(str(e))
            raise Exception(str(e))

    def getBobot(self, id_proyek):

        return self.proyek_repo.get_bobot(
            id_proyek
        )

    def getRoles(self, id_proyek):

        return self.proyek_repo.get_roles(
            id_proyek
        )

    def getTeknologi(self, id_proyek):

        return self.proyek_repo.get_teknologi(
            id_proyek
        )
        
    def getProjectSummary(self, id_proyek):

        return self.proyek_repo.get_summary(
            id_proyek
        )