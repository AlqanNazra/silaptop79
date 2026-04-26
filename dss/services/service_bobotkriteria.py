from ..repositories.interface.interface_bobot_kriteria import IBobotKriteriaRepositoryImpl
from ..repositories.interface.interface_kriteria import IKriteriaRepositoryImpl
from ..repositories.dto.dto_bobot_kriteria import BobotKriteriaDTO
from ..repositories.dto.dto_kriteria import KriteriaDTO
from collections import defaultdict


class ServiceBobotKriteria:

    def __init__(self, conn):
        self.conn = conn
        self.repoBK = IBobotKriteriaRepositoryImpl(conn)
        self.repoK = IKriteriaRepositoryImpl(conn)

    def input_bobot_batch(self, role, list_kriteria):
        try:
            with self.conn:
                total = sum([k["bobot"] for k in list_kriteria])
                if round(total, 5) != 1:
                    raise Exception("Total bobot harus = 1")

                nama_list = [k["nama"] for k in list_kriteria]
                if len(nama_list) != len(set(nama_list)):
                    raise Exception("Kriteria duplikat")

                for item in list_kriteria:
                    kriteria_dto = KriteriaDTO(
                        nama_kriteria=item["nama"],
                        tipe_kriteria=item["tipe"]
                    )

                    id_kriteria = self.repoK.tambah_kriteria(kriteria_dto)


                    bobot_dto = BobotKriteriaDTO(
                        id_kriteria=id_kriteria,
                        role=role,
                        nilai_bobot=item["bobot"],
                        nilai_swara= "Null"
                    )

                    self.repoBK.tambah_bobot_kriteria(bobot_dto)

            return {"status": "success", "message": "Berhasil input batch"}

        except Exception as e:
            return {"status": "error", "message": str(e)}
    # =========================
    # Kriteria
    # =========================
    
    def ambil_kriteria(self):
        try:
            data = self.repoK.ambil_kriteria()

            return {
                "status": "success",
                "data": data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    def update_kriteria(self, id_kriteria, nama, tipe):
        try:
            with self.conn:
                dto = KriteriaDTO(
                    id_kriteria=id_kriteria,
                    nama_kriteria=nama,
                    tipe_kriteria=tipe
                )

                result = self.repoK.update_kriteria(dto)

                return {
                    "status": "success",
                    "message": result
                }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    # =========================
    # Bobot Kriteria
    # =========================
    def ambil_bobot_by_kriteria(self, id_bobot, id_kriteria):
        try:
            data = self.repoBK.ambil_bobot_by_kriteria(id_bobot, id_kriteria)

            return {
                "status": "success",
                "data": data
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def ambil_bobot_by_roles(self, roles: list):
        try:
            if not roles:
                raise Exception("Roles tidak boleh kosong")

            data = self.repoBK.cari_bobot_kriteria_by_roles(roles)

            return {
                "status": "success",
                "data": data,
                "total": len(data)
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def update_bobot(self, id_bobot, nilai_bobot):
        try:
            with self.conn:
                dto = BobotKriteriaDTO(
                    id_bobot=id_bobot,
                    nilai_bobot=nilai_bobot
                )

                result = self.repoBK.update_bobot_kriteria(dto)

                return {
                    "status": "success",
                    "message": result
                }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def hapus_bobot(self, id_bobot):
        try:
            with self.conn:
                result = self.repoBK.hapus_bobot_kriteria(id_bobot)

                return {
                    "status": "success",
                    "message": result
                }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }