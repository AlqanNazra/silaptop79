from datetime import datetime
import traceback

from dss.services.service_bobotkriteria import ServiceBobotKriteria
from dss.services.service_swara import ServiceSwara
from dss.services.service_preposesdata import Servicepreposesdata

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
from inventori.repositories.repositori_role import RoleRepository
from inventori.dto.dto_role import RoleDTO

from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository
from dss.repositories.repositori_laptop_pengadaan import LaptopPengadaanRepository
from decimal import Decimal

from inventori.repositories.repositori_role_teknologi import RoleTeknologiRepository
class Servicesaw:

    def __init__(self, conn):
        self.conn = conn
        self.servisBK = ServiceSwara(conn)
        self.servisPD = Servicepreposesdata(conn)
        self.repodssprosses = DssprossesRepository(conn)
        self.repoalternatifdss = AlternatifDssRepository (conn)
        self.repolaptopalternatif = LaptopAlternatifRepository (conn)
        self.repohasilsaw = HasilSawRepository (conn)
        self.repodetailhasilsaw = DetailHasilSawRepository (conn)
        self.repoK = KriteriaRepository(conn)
        self.repoBK = BobotKriteriaRepository(conn)
        self.repoInventori = LaptopInventoriRepository(conn)
        self.repoPengadaan = LaptopPengadaanRepository(conn)
        self.repoRole = RoleRepository(conn)
        self.servisBobotKriteria = ServiceBobotKriteria(conn)
        self.repoRoleTeknologi = RoleTeknologiRepository(conn)

    def serialize(self, data):
        def convert(val):
            if isinstance(val, Decimal):
                return float(val)
            return val

        return [
            {k: convert(v) for k, v in dict(row).items()}
            for row in data
        ]

    def proses_dual_dataset(
        self,
        data_raw,
        role_requirement,
        role
    ):
        hasil_split = (
            self.servisPD.split_role_requirement(
                data_raw,
                role_requirement
            )
        )
        role_match = (hasil_split["role_match"])
        fallback = ( hasil_split["fallback"])
        hasil_role = None
        hasil_fallback = None
        hasil_role = (
                self.proses_saw_pipeline(
                    role_match,
                    role
                )
            )
        return {
            "role_result": hasil_role,
            "fallback_result": hasil_fallback,
            "warning":
                None
                if role_match
                else
                "Tidak ditemukan laptop yang memenuhi spesifikasi minimum role"
        }

    def get_role_requirement(
        self,
        id_role
    ):
        print("ROLE YANG DICARI =", id_role)

        role = self.repoRole.get_by_id(id_role)

        print("\n=== ROLE RAW ===")
        print(role)
        print(type(role))

        if not role:
            raise Exception(
                f"Role {id_role} tidak ditemukan"
            )

        return {
            "id_role": role[0],
            "nama_role": role[1],
            "min_ram": role[2],
            "min_storage": role[3],
            "min_processor_score": role[4]
        }
    def normalisasi_saw(self, data_preproses):  
        print("\n=== DEBUG NORMALISASI START ===")

        if not data_preproses:
            print("DATA PREPROCESS KOSONG")
            return []

        print("JUMLAH DATA:", len(data_preproses))
        print("SAMPLE:", data_preproses[0])

        kriteria_data = self.repoK.ambil_kriteria()

        print("KRITERIA:")
        print(kriteria_data)
        for i, k in enumerate(kriteria_data):
            print(
                f"KRITERIA[{i}] =",
                k,
                "TYPE=",
                type(k)
            )
        map_tipe = {k['nama_kriteria']: k['tipe_kriteria'].lower() for k in kriteria_data}
        keys = data_preproses[0].keys()
        max_values = {}
        min_values = {}
        
        for key in keys:
            if key == "id":
                continue
            all_vals = [item[key] for item in data_preproses if item[key] is not None]
            max_values[key] = max(all_vals) if all_vals else 0
            min_values[key] = min(all_vals) if all_vals else 0

        hasil_normalisasi = []

        for item in data_preproses:
            normal_item = {"id": item["id"]}

            for key in keys:
                if key == "id":
                    continue

                tipe = map_tipe.get(key, "benefit")
                nilai = item.get(key, 0)

                if nilai == 0:
                    normal_item[key] = 0
                    continue

                if tipe == 'benefit':
                    normal_item[key] = nilai / max_values[key] if max_values[key] != 0 else 0
                elif tipe == 'cost':
                    normal_item[key] = min_values[key] / nilai if nilai != 0 else 0
                else:
                    normal_item[key] = 0

            hasil_normalisasi.append(normal_item)

        return hasil_normalisasi
    
    def get_bobot_saw(self, role: list):

        role_teknologi_list = (
            self.repoRoleTeknologi
            .get_by_role(role[0])
        )

        hasil_role = (
            self.servisBK.proses_role(
                role[0],
                role_teknologi_list
            )
        )
        print("\n====================")
        print("BOBOT HASIL AGREGASI ROLE")
        print("====================")


        for k,v in hasil_role["hasil_role"].items():

            print(
                k,
                "=",
                v
            )
        

        return hasil_role["hasil_role"]
    
    def hitung_saw_data(self, data_normalisasi, role: list):
        if not data_normalisasi:
            return []
        print("\n=== DEBUG HITUNG SAW ===")

        print("ROLE:")
        print(role)

        print("DATA NORMALISASI:")
        print(data_normalisasi)

        if len(data_normalisasi) > 0:
            print("SAMPLE:")
            print(data_normalisasi[0])

        bobot = self.get_bobot_saw(role)
        print("BOBOT:")
        print(bobot)

        for k,v in bobot.items():
            print(k, v)
        hasil = []

        for item in data_normalisasi:
            skor = 0
            for key, nilai_bobot in bobot.items():
                if key not in item:
                    raise KeyError(f"Kriteria '{key}' tidak ada di data")
                skor += item[key] * nilai_bobot

            hasil.append({
                "id": item["id"],
                "skor": round(skor, 6)
            })
            
        # print("\n=== DEBUG SAW ===")
        # print("BOBOT:", bobot)

        # for item in data_normalisasi[:3]:
        #     print("DATA:", item)

        return hasil
    
    
    def ranking_saw(self, hasil_saw):
        return sorted(
            hasil_saw,
            key=lambda x: x["skor"],
            reverse=True
        )
    
    def simpan_alternatif_awal(self, data_raw, id_dss, sumber_data):
        list_alternatif = []

        for item in data_raw:
            id_alt = self.repoalternatifdss.tambah_alternatif_dss(
                AlternatifDssDTO(
                    id_dss=id_dss,
                    id_laptop_inventori=item.get("id_laptop_inventori"),
                    id_laptop_pengadaan=item.get("id_laptop_pengadaan"),
                    sumber_data=sumber_data
                )
            )

            item["id"] = id_alt
            list_alternatif.append(item)

        return list_alternatif
    
    def proses_saw_pipeline(self, list_alternatif, role):
        data_pre = self.servisPD.preprocessing(list_alternatif)
        print("\n=== PREPROCESSING ===")
        print(data_pre[0])
        
        data_normalisasi = self.normalisasi_saw(data_pre)
        hasil_saw = self.hitung_saw_data(data_normalisasi, role)
        ranking = self.ranking_saw(hasil_saw)

        for i, item in enumerate(ranking, start=1):
            item["rank"] = i

        return {
            "preprocessing": data_pre,
            "normalisasi": data_normalisasi,
            "hasil_saw": hasil_saw,
            "ranking": ranking
        }
        
    def simpan_hasil_saw(self, id_dss, ranking):
        id_hasil = self.repohasilsaw.buat_hasil_saw(
            HasilSAWDTO(id_dss=id_dss)
        )

        for item in ranking:
            self.repodetailhasilsaw.tambah_detail_hasil_saw(
                DetailHasilSawDTO(
                    id_hasil=id_hasil,
                    nilai_normalisasi=item.get("normalisasi"),
                    nilai_rangking=item.get("skor"),  
                    rangking=item.get("rank")
                )
            )

        return id_hasil
    
    def simpan_laptop_terpilih(self, ranking, id_dss, top_n=10):
        selected = ranking[:top_n]

        for item in selected:
            data = None
            if "id_laptop_inventori" in item:
                data = self.repoInventori.ambil_by_id(item["id_laptop_inventori"])
            elif "id_laptop_pengadaan" in item:
                data = self.repoPengadaan.ambil_by_id(item["id_laptop_pengadaan"])
            if not data:
                continue
            self.repolaptopalternatif.tambah_laptop_alternatif(
                LaptopAlternatifDTO(
                    model_alternatif=data.get("model") or data.get("model_pengadaan"),
                    brand_alternatif=data.get("brand") or data.get("brand_pengadaan"),
                    id_dss=id_dss
                )
            )

    def proses_dss_saw(self,id_user,id_bobot,sumber_data,filter_data,role: list,debug=False):
        conn = self.conn
        try:
            # conn.autocommit = False
            id_dss = self.repodssprosses.tambah_dss_proses(
                DssProsesDTO(
                    id_user=id_user,
                    id_bobot=id_bobot,
                    role_dss=",".join(role),
                    jenis_dss="SAW",
                    create_at=datetime.now()
                )
            )
            print("\n=== ID DSS HASIL INSERT ===")
            print(id_dss)
            print(type(id_dss))
            hasil_filter = self.servisPD.filtering_data(
                sumber_data,
                filter_data
            )
            if hasil_filter["status"] != "success":
                conn.rollback()
                return hasil_filter
            data_raw = hasil_filter["data"]
            semua_data = (
                self.servisPD
                .ambil_semua_data(
                    sumber_data
                )
            )

            print(
                "TOTAL DATA INVENTORI =",
                len(semua_data)
            )
            # print("=== RAW DATA ===")
            # print(data_raw[0])
            # if not data_raw:
            #     conn.rollback()
            #     return {
            #         "status": "error",
            #         "message": "Data laptop tidak ditemukan"
            #     }
            role_requirement = self.get_role_requirement(role[0])
            hasil_split = (
                self.servisPD.split_role_requirement(
                    data_raw,
                    role_requirement
                )
            )

            role_match_data = (
                hasil_split["role_match"]
            )
            # DATASET 1 REKOMENDASI SESUAI ROLE
            ranking_role = []
            hasil_role = None
            if role_match_data:
                hasil_role = (
                    self.proses_saw_pipeline(
                        role_match_data,
                        role
                    )
                )
                ranking_role = (
                    hasil_role["ranking"]
                )
            # DATASET 2 ALTERNATIF LAIN
            hasil_fallback = (
                self.proses_saw_pipeline(
                    semua_data,
                    role
                )
            )
            ranking_fallback = (hasil_fallback["ranking"])
            
            if ranking_role:
                id_hasil_role = (
                    self.simpan_hasil_saw(
                        id_dss,
                        ranking_role
                    )
                )
            else:
                id_hasil_role = None
            print("\n=== DEBUG ID DSS ===")
            print(id_dss)
            print(type(id_dss))
            id_hasil_fallback = (
                self.simpan_hasil_saw(
                    id_dss,
                    ranking_fallback
                )
            )

            if ranking_role:
                self.simpan_laptop_terpilih(
                    ranking_role,
                    id_dss,
                    top_n=3
                )
            else:
                self.simpan_laptop_terpilih(
                    ranking_fallback,
                    id_dss,
                    top_n=3
                )
            conn.commit()

            # if debug == True:

                # print("\n" + "=" * 80)
                # print("HASIL DSS SAW")
                # print("=" * 80)

                # meta = {
                #     "id_dss": id_dss,
                #     "id_hasil_role": id_hasil_role,
                #     "id_hasil_fallback": id_hasil_fallback,
                #     "total_role_match": len(role_match),
                #     "total_fallback": len(fallback)
                # }

                # print(f"ID DSS            : {meta['id_dss']}")
                # print(f"ID Role Match     : {meta['id_hasil_role']}")
                # print(f"ID Fallback       : {meta['id_hasil_fallback']}")
                # print(f"Total Role Match  : {meta['total_role_match']}")
                # print(f"Total Fallback    : {meta['total_fallback']}")

                # print("\n" + "-" * 80)
                # print("REKOMENDASI SESUAI ROLE")
                # print("-" * 80)

                # for item in ranking_role:
                #     print(
                #         f"Rank {item['rank']:>2} | "
                #         f"{item['id']} | "
                #         f"Score = {item['skor']:.6f}"
                #     )

                # print("\n" + "-" * 80)
                # print("ALTERNATIF LAIN (SEMUA DATA)")
                # print("-" * 80)

                # for item in ranking_fallback:
                #     print(
                #         f"Rank {item['rank']:>2} | "
                #         f"{item['id']} | "
                #         f"Score = {item['skor']:.6f}"
                #     )

                # print("=" * 80)
            
            # if debug == True:
            #     return {
            #         "status": "success",
            #         "warning":
            #             None
            #             if role_match_data
            #             else
            #             (
            #                 "Tidak ditemukan laptop "
            #                 "yang memenuhi minimum "
            #                 "requirement role"
            #             ),
            #         "debug": {
            #             "role_requirement":
            #                 role_requirement,
            #             "total_role_match":
            #                 len(role_match_data),
            #             "total_fallback":
            #                 len(fallback_data),
            #             "hasil_role":
            #                 hasil_role,
            #             "hasil_fallback":
            #                 hasil_fallback
            #         },

            #         "data": {
            #             "rekomendasi_sesuai_role": {
            #                 "ranking":
            #                     ranking_role
            #             },
            #             "alternatif_lain": {
            #                 "ranking":
            #                     ranking_fallback
            #             }
            #         }
            #     }

            # ==========================================
            # NORMAL MODE
            # ==========================================
            return {
                "status": "success",
                "warning":
                    None
                    if role_match_data
                    else
                    (
                        "Tidak ditemukan laptop "
                        "yang memenuhi minimum "
                        "requirement role"
                    ),
                "meta": {
                    "id_dss":
                        id_dss,
                    "id_hasil_role":
                        id_hasil_role,
                    "id_hasil_fallback":
                        id_hasil_fallback,
                    "total_role_match":
                        len(ranking_role),
                    "total_fallback":
                        len(ranking_fallback)
                },
                "data": {
                    "rekomendasi_sesuai_role": {
                        "ranking":
                            ranking_role
                    },
                    "alternatif_lain": {
                        "ranking":
                            ranking_fallback
                    }
                }
            }
        # except Exception as e:
        #     conn.rollback()

        #     print("\n=== ERROR DSS ===")
        #     traceback.print_exc()

        #     return {
        #         "status": "error",
        #         "message": str(e)
        #     }
        except Exception as e:
            conn.rollback()

            import traceback

            print("\n=== ERROR DSS FULL ===")
            traceback.print_exc()

            raise
        finally:
            conn.autocommit = True