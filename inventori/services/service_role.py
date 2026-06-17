# services/role_service.py
import logging
from django.db import transaction, IntegrityError
from psycopg2 import DatabaseError
from dss.repositories.dto.dto_bobot_kriteria import BobotKriteriaDTO
from inventori.repositories.interfaces.interface_role import IRoleService, IRoleRepository
from inventori.dto.dto_role import RoleDTO
from dss.repositories.interface.interface_bobot_kriteria import IBobotkriteriaRepository

logger = logging.getLogger(__name__)

class RoleService(IRoleService):
    def __init__(self, role_repo: IRoleRepository, conn,repo_bobot: IBobotkriteriaRepository ):
        self.role_repo = role_repo
        self.repo_bobot = repo_bobot
        self.conn = conn

    def tambah_role(self, data: RoleDTO) -> str:
        try:
            with transaction.atomic():
                new_id = self.role_repo.tambah(data)
                self.conn.commit()  
                logger.info(f"Berhasil menambahkan Role baru: {new_id}")
                return new_id
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Gagal tambah_role: {str(e)}")
            raise ValueError(str(e)) 

    def update_role(self, data: RoleDTO) -> bool:
        try:
            with transaction.atomic():
                res = self.role_repo.update(data)
                self.conn.commit()
                return res
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Gagal update_role: {str(e)}")
            raise ValueError(str(e))

    # def hapus_role(self, id_role: str) -> bool:
    #     try:
    #         with transaction.atomic():
    #             res = self.role_repo.hapus(id_role)
    #             self.conn.commit()
    #             logger.info(f"Role {id_role} berhasil dihapus")
    #             return res
    #     except Exception as e:
    #         self.conn.rollback()
    #         logger.error(f"Constraint Error saat hapus_role: {str(e)}")
    #         raise ValueError(str(e))
    def hapus_role(self,id_role):
        try:
            with transaction.atomic():
                self.role_repo.hapus(id_role)
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            raise Exception(str(e))

    #  Pelajari
    # def calculate_need_score(self, id_role: str):
    #     kriteria_list = self.role_repo.get_kriteria(id_role)
    #     total_score = 0
    #     detail_score = {}
    #     for k in kriteria_list:
    #         # Misal nilai_bobot sudah dalam bentuk persentase/desimal dari MCDM method (seperti SWARA)
    #         score = float(k["nilai_bobot"]) * 1.5 # 1.5 adalah konstanta fiktif baseline spec
    #         total_score += score
    #         detail_score[k["nama_kriteria"]] = score
            
    #     return {
    #         "id_role": id_role,
    #         "total_need_score": total_score,
    #         "breakdown": detail_score
    #     }
    
    def update_role_lengkap(self,role_dto,bobot_updates):
        try:
            with transaction.atomic():
                self.role_service.update_role(role_dto)
                for item in bobot_updates:
                    dto = BobotKriteriaDTO(
                        id_role_teknologi=
                            item["id_role_teknologi"],

                        id_kriteria=
                            item["id_kriteria"],

                        nilai_bobot=
                            item["nilai_bobot"]
                    )

                    self.repo_bobot.update_bobot_role_teknologi(
                        dto
                    )
                self.conn.commit()
                return {
                    "status":"success",
                    "message":"Role berhasil diperbarui"
                }

        except Exception as e:
            self.conn.rollback()
            logger.error(str(e))
            return {
                "status":"error",
                "message":str(e)}
