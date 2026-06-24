from collections import defaultdict
from copy import deepcopy
from datetime import datetime
from itertools import combinations
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
from dss.services.service_validator_saw import ServiceValidatorSAW
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

    def get_role_requirement(self,id_role):
        # print("ROLE YANG DICARI =", id_role)
        role = self.repoRole.get_by_id(id_role)
        # print("\n=== ROLE RAW ===")
        # print(role)
        # print(type(role))
        if not role:
            raise Exception(f"Role {id_role} tidak ditemukan")
        return {
            "id_role": role["id_role"],
            "nama_role": role["nama_role"],
            "min_ram": role["min_ram"],
            "min_storage": role["min_storage"],
            "min_processor_score": role["min_processor_score"]
        }
    def normalisasi_saw(self, data_preproses):  
        # print("\n=== DEBUG NORMALISASI START ===")
        # print("=== NORMALISASI SAW VERSI BARU ===")

        # if not data_preproses:
        #     print("DATA PREPROCESS KOSONG")
        #     return []

        # print("JUMLAH DATA:", len(data_preproses))
        # print("SAMPLE:", data_preproses[0])

        kriteria_data = self.repoK.ambil_kriteria()

        # print("KRITERIA:")
        # print(kriteria_data)
        # for i, k in enumerate(kriteria_data):
        #     print(
        #         f"KRITERIA[{i}] =",
        #         k,
        #         "TYPE=",
        #         type(k)
        #     )
        map_tipe = {k['nama_kriteria']: k['tipe_kriteria'].lower() for k in kriteria_data}
        # print("\n" + "="*50)
        # print("KLASIFIKASI KRITERIA")
        # print("="*50)

        # for nama, tipe in map_tipe.items():
        #     print(
        #         f"{nama:<20} -> {tipe.upper()}"
        #     )
        keys = list(data_preproses[0].keys())
        # print("KEYS =", keys)
        max_values = {}
        min_values = {}
        keys = list(data_preproses[0].keys())
        # print("\n=== DEBUG KEYS ===")
        # print(keys)
        for key in keys:
            # print(f"\nPROSES -> {key}")
            # if key == "id":
            #     print("SKIP ID")
            #     continue
            try:
                all_vals = [item[key] for item in data_preproses if item[key] is not None]
                # print("JUMLAH =", len(all_vals))
                max_values[key] = max(all_vals)
                min_values[key] = min(all_vals)
                # print( f"MAX={max_values[key]} "f"MIN={min_values[key]}")
            except Exception as e:
                print(f"ERROR SAAT PROSES {key}")
                print(str(e))

        hasil_normalisasi = []
        # print("\n=== CEK KEY PREPROSES ===")
        # for i, item in enumerate(data_preproses):
        #     print(f"ITEM {i}:",list(item.keys()))

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
                    # if key not in max_values:
                    #     print("\nERROR KEY")
                    #     print("KEY =", key)
                    #     print("MAX VALUES")
                    #     print(max_values)
                    #     print("ITEM")
                    #     print(item)
                    # normal_item[key] = nilai / max_values[key] if max_values[key] != 0 else 0\
                    # =======================================
                    #  TESTING
                    # =======================================
                    hasil = nilai / max_values[key]
                    # print(
                    #     f"[BENEFIT] "
                    #     f"{key}: "
                    #     f"{nilai}/{max_values[key]}"
                    #     f" = {hasil:.4f}"
                    # )
                    normal_item[key] = hasil
                elif tipe == 'cost':
                    # if key not in max_values:
                    #     print("\nERROR KEY")
                    #     print("KEY =", key)
                    #     print("MAX VALUES")
                    #     print(max_values)
                    #     print("ITEM")
                    #     print(item)
                    # normal_item[key] = min_values[key] / nilai if nilai != 0 else 0
                    # =======================================
                    #  TESTING
                    # =====================================
                    hasil = min_values[key] / nilai
                    # print(
                    #     f"[COST] "
                    #     f"{key}: "
                    #     f"{min_values[key]}/{nilai}"
                    #     f" = {hasil:.4f}"
                    # )
                    normal_item[key] = hasil
                else:
                    normal_item[key] = 0

            hasil_normalisasi.append(normal_item)
            # print("\n" + "="*50)
            # print("HASIL NORMALISASI")
            # print("="*50)
            # print("\n" + "="*50)
            # print("VALIDASI NORMALISASI")
            # print("="*50)
            for item in hasil_normalisasi:
                for key, value in item.items():
                    if key == "id":
                        continue
            #         if value < 0 or value > 1:
            #             valid = False
            #             print(f"ERROR "f"{item['id']} "f"{key}={value}")
            # if valid:
            #     print("STATUS : VALID")
            #     print("Semua nilai berada pada rentang 0-1")
            # else:
            #     print("STATUS : INVALID")

            # for item in hasil_normalisasi:
            #     print(item)

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
        # print("\n====================")
        # print("BOBOT HASIL AGREGASI ROLE")
        # print("====================")


        # for k,v in hasil_role["hasil_role"].items():

        #     print(
        #         k,
        #         "=",
        #         v
        #     )
        

        return hasil_role["hasil_role"]
    
    def hitung_saw_data(self, data_normalisasi, role: list):
        if not data_normalisasi:
            return []
        # print("\n=== DEBUG HITUNG SAW ===")

        # print("ROLE:")
        # print(role)

        # print("DATA NORMALISASI:")
        # print(data_normalisasi)

        # if len(data_normalisasi) > 0:
        #     print("SAMPLE:")
        #     print(data_normalisasi[0])

        bobot = self.get_bobot_saw(role)
        validator = ServiceValidatorSAW()
        validator.validate_bobot(bobot)
        # print("BOBOT:")
        # print(bobot)

        # for k,v in bobot.items():
        #     print(k, v)
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
        validator = ServiceValidatorSAW()
        validator.validate_bobot(bobot)
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
        validator = ServiceValidatorSAW()
        validator.validate_normalisasi(data_normalisasi)
        hasil_saw = self.hitung_saw_data(data_normalisasi, role)
        ranking = self.ranking_saw(hasil_saw)
        validator.validate_skor(ranking)
        validator.validate_ranking(ranking)

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

    from itertools import combinations
    from collections import defaultdict
    from copy import deepcopy

    def jalankan_simulasi_sensitivitas_43(self,data_preproses,role):
        print(">>> VERSI SENSITIVITAS 43 AKTIF <<<")
        print("\n" + "=" * 80)
        print("UJI SENSITIVITAS SWARA-SAW")
        print("=" * 80)
        data_norm = self.normalisasi_saw(data_preproses)
        base_bobot = self.get_bobot_saw(role)
        data_kriteria = self.repoK.ambil_kriteria()
        # print("\n=== KRITERIA DB ===")
        # for x in data_kriteria:
        #     print(x)
        hardware = []
        fisik = []
        for item in data_kriteria:
            if (item["golongan_kriteria"].lower()== "hardware"):
                hardware.append(item["nama_kriteria"])
            elif (item["golongan_kriteria"].lower()== "fisik"):
                fisik.append(item["nama_kriteria"])
        kombinasi_uji = []
        print("HARDWARE =", hardware)
        print("FISIK =", fisik)
        # =====================================
        # SINGLE CRITERIA
        # =====================================
        for k in hardware + fisik:
            kombinasi_uji.append([k])
        for r in [2, 3]:
            for combo in combinations(hardware,r):
                kombinasi_uji.append(list(combo))
        # =====================================
        # FISIK
        # =====================================
        for r in [2, 3]:
            for combo in combinations(fisik,r):
                kombinasi_uji.append(list(combo))
        persentase_uji = [0.10,0.20,0.30]
        # =====================================
        # BASELINE
        # =====================================
        hasil_baseline = self.hitung_saw_data(data_norm,role)
        ranking_baseline = self.ranking_saw(hasil_baseline)
        baseline_top1 = (ranking_baseline[0]["id"])
        perubahan_rank1 = 0
        detail_kasus = []
        total_kasus = 1
        # =====================================
        # SIMULASI
        # =====================================
        for combo in kombinasi_uji:
            for pct in persentase_uji:
                bobot_baru = deepcopy(base_bobot)
                for k in combo:
                    if k in bobot_baru:
                        bobot_baru[k] *= (1 + pct)
                total = sum(bobot_baru.values())
                for k in bobot_baru:
                    bobot_baru[k] /= total
                hasil_saw = []
                for item in data_norm:
                    skor = 0
                    for nama_kriteria, bobot in bobot_baru.items():
                        skor += (item.get(nama_kriteria,0)* bobot)
                    hasil_saw.append({"id": item["id"],"skor": round(skor,6)})
                ranking = self.ranking_saw(hasil_saw)
                total_kasus += 1
                top1 = ranking[0]["id"]
                if top1 != baseline_top1:
                    perubahan_rank1 += 1
                detail_kasus.append({
                    "kombinasi": combo,
                    "persentase":int(pct * 100),
                    "rank1":top1,
                    "skor":ranking[0]["skor"]
                })
        stabilitas = round(((total_kasus - 1- perubahan_rank1)/(total_kasus - 1)) * 100,2)
        print("\n" + "=" * 80)
        print("BASELINE")
        print("=" * 80)

        for i, item in enumerate(
                ranking_baseline[:5],
                start=1):

            print(
                f"{i}. "
                f"{item['id']} "
                f"({item['skor']:.6f})"
            )
        print("\n" + "-" * 80)
        print(
            f"SKENARIO "
            f"{'+'.join(combo)} "
            f"+{int(pct*100)}%"
        )

        print("-" * 80)

        for i, item in enumerate(
                ranking[:5],
                start=1):

            print(
                f"{i}. "
                f"{item['id']} "
                f"({item['skor']:.6f})"
            )
        if top1 != baseline_top1:
            print(
                f"PERUBAHAN TOP-1 : "
                f"{baseline_top1}"
                f" -> "
                f"{top1}"
            )
        print("\n" + "=" * 80)
        print("RINGKASAN SENSITIVITAS")
        print("=" * 80)

        print(
            "BASELINE TOP-1 :",
            baseline_top1
        )

        print(
            "TOTAL KASUS :",
            total_kasus
        )

        print(
            "PERUBAHAN TOP-1 :",
            perubahan_rank1
        )

        print(
            "STABILITAS :",
            f"{stabilitas}%"
        )
        return {
            "total_kasus":total_kasus,
            "baseline_rank1":baseline_top1,
            "perubahan_rank1":perubahan_rank1,
            "stabilitas":stabilitas,
            "detail":detail_kasus
        }

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
            # print("\n=== ID DSS HASIL INSERT ===")
            # print(id_dss)
            # print(type(id_dss))
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

            # print(
            #     "TOTAL DATA INVENTORI =",
            #     len(semua_data)
            # )
            # print("=== RAW DATA ===")
            # print(data_raw[0])
            # if not data_raw:
            #     conn.rollback()
            #     return {
            #         "status": "error",
            #         "message": "Data laptop tidak ditemukan"
            #     }
            role_requirement = self.get_role_requirement(role[0])
            print(role_requirement)
            hasil_split = (self.servisPD.split_role_requirement(data_raw,role_requirement))
            print("\n=== HASIL SPLIT ===")
            print("TOTAL RAW =", len(data_raw))
            print("TOTAL ROLE MATCH =", len(hasil_split["role_match"]))
            role_match_data = (hasil_split["role_match"])
            # DATASET 1 REKOMENDASI SESUAI ROLE
            ranking_role = []
            hasil_role = None
            hasil_sensitivitas = None
            if role_match_data:
                print(
                "PIPELINE MENERIMA",
                len(role_match_data),
                "DATA")
                hasil_role = (self.proses_saw_pipeline(role_match_data,role))
                print("\n=== HASIL ROLE KEYS ===")
                print(hasil_role.keys())
                
                ranking_role = (hasil_role["ranking"])
                # ==================================
                # UJI SENSITIVITAS
                # ==================================
                hasil_sensitivitas = (self.jalankan_simulasi_sensitivitas_43(hasil_role["preprocessing"],role))
                
            validator = ServiceValidatorSAW()
            # validator.validate_alternatif(role_match_data)
            if hasil_role and "ranking" in hasil_role:
                validator.validate_skor(
                    hasil_role["ranking"]
                )
                validator.validate_ranking(
                    hasil_role["ranking"]
                )

            validator.print_report()
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
            # print("\n=== DEBUG ID DSS ===")
            # print(id_dss)
            # print(type(id_dss))
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
                "sensitivitas":hasil_sensitivitas,
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