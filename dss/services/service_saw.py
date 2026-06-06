from datetime import datetime

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

from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository
from dss.repositories.repositori_laptop_pengadaan import LaptopPengadaanRepository
from decimal import Decimal
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

    def serialize(self, data):
        def convert(val):
            if isinstance(val, Decimal):
                return float(val)
            return val

        return [
            {k: convert(v) for k, v in dict(row).items()}
            for row in data
        ]
        
    def normalisasi_saw(self, data_preproses):  
        if not data_preproses:
            return []
        kriteria_data = self.repoK.ambil_kriteria()
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
        if not role:
            raise ValueError("Role tidak boleh kosong")

        hasil = self.servisBK.proses_swara(role)

        if hasil["status"] != "success":
            raise Exception(hasil["message"])
        
        bobot_list = hasil["data"]["bobot_akhir"]

        return {
            item["nama_kriteria"]: item["bobot_akhir"]
            for item in bobot_list
        }
    
    def hitung_saw_data(self, data_normalisasi, role: list):
        if not data_normalisasi:
            return []

        bobot = self.get_bobot_saw(role)
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

    def proses_dss_saw(self, id_user, id_bobot, sumber_data, filter_data, role: list, debug=False):
        conn = self.conn

        try:
            conn.autocommit = False      
            id_dss = self.repodssprosses.tambah_dss_proses(
                DssProsesDTO(
                    id_user=id_user,
                    id_bobot=id_bobot,
                    role_dss=",".join(role),
                    jenis_dss="SAW",
                    create_at=datetime.now()
                )
            )

            hasil_filter = self.servisPD.filtering_data(sumber_data, filter_data)
            if hasil_filter["status"] != "success":
                conn.rollback()
                return hasil_filter
            data_raw = hasil_filter["data_raw"]

            list_alternatif = self.simpan_alternatif_awal(
                data_raw, id_dss, sumber_data
            )
            hasil = self.proses_saw_pipeline(list_alternatif, role)
            ranking = hasil["ranking"]
            id_hasil = self.simpan_hasil_saw(id_dss, ranking)

            self.simpan_laptop_terpilih(ranking, id_dss, top_n=3)

            conn.commit()

            if debug:
                return {
                    "status": "success",
                    "debug": hasil,
                    "data": {"ranking": ranking}
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

        except Exception as e:
            conn.rollback()
            return {
                "status": "error",
                "message": str(e)
            }

        finally:
            conn.autocommit = True

  