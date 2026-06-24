# from ..repositories.interface.interface_bobot_kriteria import IBobotKriteriaRepositoryImpl
# from ..repositories.interface.interface_kriteria import IKriteriaRepositoryImpl
from ..repositories.dto.dto_bobot_kriteria import BobotKriteriaDTO
from ..repositories.dto.dto_kriteria import KriteriaDTO
from collections import defaultdict

from ..repositories.repositori_kriteria import KriteriaRepository
from ..repositories.repositori_bobot_kriteria import BobotKriteriaRepository

class ServiceBobotKriteria:

    def __init__(self, conn):
        self.conn = conn
        # self.repoBK = IBobotKriteriaRepositoryImpl(conn)
        # self.repoK = IKriteriaRepositoryImpl(conn)
        self.repoK = KriteriaRepository(conn)
        self.repoBK = BobotKriteriaRepository(conn)


    def input_bobot_batch(self, role, list_kriteria):
        print("🔥 SERVICE MASUK")

        try:
            total = sum([k["bobot"] for k in list_kriteria])

            # if abs(total - 1) > 0.00001:
            #     raise Exception("Total bobot harus = 1")

            with self.conn:
                for item in list_kriteria:

                    dto = KriteriaDTO(
                        nama_kriteria=item["nama"].strip(),
                        tipe_kriteria=item["tipe"],
                        golongan_kriteria=item["golongan"]
                    )

                    id_kriteria = self.repoK.tambah_kriteria(dto)

                    print("ID KRITERIA:", id_kriteria)
                    
                    dtobobot = BobotKriteriaDTO(
                        id_kriteria=id_kriteria,
                        role=role,
                        nilai_bobot = item ["bobot"],
                        nilai_swara= None
                    )

                    self.repoBK.tambah_bobot_kriteria(dtobobot)

            return {"status": "success", "message": "Berhasil input batch"}

        except Exception as e:
            print("❌ SERVICE ERROR:", e)
            return {"status": "error", "message": str(e)}
    
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

    def get_unique_roles(self):
        try:
            roles = self.repoBK.ambil_semua_role()
            clean_roles = list(set(
                r.strip() for r in roles if r
            ))
            clean_roles.sort()

            return {
                "status": "success",
                "data": clean_roles
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
            
    def input_bobot_role_teknologi(
        self,
        id_role_teknologi,
        list_bobot
    ):
        print("\n====================")
        print("SERVICE BOBOT")
        print("====================")

        print(
            "ROLE TEKNOLOGI:",
            id_role_teknologi
        )
        try:

            with self.conn:

                for item in list_bobot:

                    dto = BobotKriteriaDTO(

                        id_role_teknologi=
                            id_role_teknologi,

                        id_kriteria=
                            item["id_kriteria"],

                        nilai_bobot=
                            float(
                                item["nilai_bobot"]
                            ),

                        nilai_swara=None
                    )
                    # print(
                    #     "KRITERIA:",
                    #     item["id_kriteria"],
                    #     "BOBOT:",
                    #     item["nilai_bobot"]
                    # )

                    self.repoBK.tambah_bobot_kriteria(
                        dto
                    )

            return {
                "status": "success",
                "message":
                    "Berhasil input bobot"
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }
    def update_bobot_role_teknologi(
        self,
        id_role_teknologi,
        list_bobot
    ):

        try:

            with self.conn:

                for item in list_bobot:

                    dto = BobotKriteriaDTO(

                        id_role_teknologi=
                            id_role_teknologi,

                        id_kriteria=
                            item["id_kriteria"],

                        nilai_bobot=
                            item["nilai_bobot"]
                    )

                    self.repoBK.update_bobot_role_teknologi(
                        dto
                    )

            return {

                "status":
                    "success",

                "message":
                    "Bobot berhasil diperbarui"
            }

        except Exception as e:

            return {

                "status":
                    "error",

                "message":
                    str(e)
            }