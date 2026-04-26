from service_swara import ServiceBobotKriteria
from service_preposesdata import Servicepreposesdata
from ..repositories.interface.interface_bobot_kriteria import IBobotKriteriaRepositoryImpl
from ..repositories.interface.interface_kriteria import IKriteriaRepositoryImpl


class Servicesaw:
    
    def __init__(self, conn):
        self.conn = conn
        self.servisBK = ServiceBobotKriteria(conn)
        self.servisPD = Servicepreposesdata(conn)
        self.repoK = IKriteriaRepositoryImpl(conn)
        self.repoBK = IBobotKriteriaRepositoryImpl(conn)
        
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
    
    def get_bobot_saw(self,role,id_bobot):
        hasil = self.servisBK.proses_swara(role,id_bobot)
        if hasil["status"] != "success":
            raise Exception(hasil["message"])
        bobot_list = hasil["data"]["bobot_akhir"]
        bobot = {
            item["nama_kriteria"]: item["bobot_akhir"]
            for item in bobot_list
        }
        return bobot
    
    def hitung_saw_data(self,data_normalisasi,role,id_bobot):
        if not data_normalisasi:
            return[]
        
        bobot = self.get_bobot_saw(role,id_bobot)
        hasil = []
        
        for item in data_normalisasi:
            skor = 0
            for key,nilai_bobot in bobot.items():
                nilai = item.get(key, 0)
                skor += nilai * nilai_bobot
        
            hasil.append({
                "id": item["id"],
                "skor": round(skor, 6)
            })

        return hasil
    
    
    def ranking_saw(self, hasil_saw):
        return sorted(
            hasil_saw,
            key=lambda x: x["skor"],
            reverse=True
        )
    
    def proses_dss_saw(self,sumber_data,filter_data,role,id_bobot):
        try:
            hasil_filter = self.servisPD.filtering_data(sumber_data,filter_data)
            if hasil_filter["status"] != "success":
                return hasil_filter

            data_raw = hasil_filter["data_raw"]
            data_pre = self.servisPD.preprocessing(data_raw)
            data_normalisasi = self.normalisasi_saw(data_pre)
            hasil_saw = self.hitung_saw_data(data_normalisasi,role,id_bobot)
            ranking = self.ranking_saw(hasil_saw)
            return {
                "status": "success",
                "data": {
                    "data_awal": data_raw,
                    "data_preprocessing": data_pre,
                    "data_normalisasi": data_normalisasi,
                    "hasil_saw": hasil_saw,
                    "ranking": ranking
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def hitung_average_golongan(self, roles: list[str]):
        """
        roles = ["Backend", "Frontend", "Data Analyst"]
        """

        if not roles:
            raise ValueError("Role tidak boleh kosong")

        # =========================
        # 1. Grouping Golongan
        # =========================
        golongan_map = {}

        for role in roles:
            data = self.repoBK.cari_bobot_kriteria_by_role(role)

            if not data:
                raise ValueError(f"Bobot tidak ditemukan untuk role {role}")

            gol = data["golongan"]

            if gol not in golongan_map:
                golongan_map[gol] = []

            golongan_map[gol].append(data)

        # =========================
        # 2. Average dalam golongan
        # =========================
        hasil_golongan = {}

        for gol, bobot_list in golongan_map.items():
            avg = {}
            keys = bobot_list[0].keys()

            for k in keys:
                if k == "golongan":
                    continue

                avg[k] = sum(b[k] for b in bobot_list) / len(bobot_list)

            hasil_golongan[gol] = avg

        # =========================
        # 3. Average antar golongan
        # =========================
        hasil_final = {}
        gol_keys = list(hasil_golongan.keys())
        keys = hasil_golongan[gol_keys[0]].keys()

        for k in keys:
            hasil_final[k] = sum(hasil_golongan[g][k] for g in gol_keys) / len(gol_keys)

        return hasil_final
    
    def hitung_weighted_golongan(self, roles: list[dict]):
        """
        roles = [
            {"role": "Backend", "weight": 0.6},
            {"role": "Frontend", "weight": 0.4}
        ]
        """

        if not roles:
            raise ValueError("Role tidak boleh kosong")

        # =========================
        # 1. Grouping Golongan
        # =========================
        golongan_map = {}

        for r in roles:
            role_name = r["role"]
            weight = r.get("weight")

            data = self.repoBK.cari_bobot_kriteria_by_role(roles)

            if not data:
                raise ValueError(f"Bobot tidak ditemukan untuk role {role_name}")

            gol = data["golongan"]

            if gol not in golongan_map:
                golongan_map[gol] = {
                    "bobot": [],
                    "weights": []
                }

            golongan_map[gol]["bobot"].append(data)
            golongan_map[gol]["weights"].append(weight)

        # =========================
        # 2. Average dalam golongan
        # =========================
        hasil_golongan = {}

        for gol, val in golongan_map.items():
            bobot_list = val["bobot"]

            avg = {}
            keys = bobot_list[0].keys()

            for k in keys:
                if k == "golongan":
                    continue

                avg[k] = sum(b[k] for b in bobot_list) / len(bobot_list)

            hasil_golongan[gol] = avg

        # =========================
        # 3. Weighted antar golongan
        # =========================
        gol_keys = list(hasil_golongan.keys())

        # hitung weight golongan dari role
        weight_gol = []

        for gol in gol_keys:
            w = [w for w in golongan_map[gol]["weights"] if w is not None]

            if w:
                weight_gol.append(sum(w) / len(w))  # rata-rata weight dalam golongan
            else:
                weight_gol.append(1)

        # normalisasi
        total = sum(weight_gol)
        weight_gol = [w / total for w in weight_gol]

        # final combine
        hasil_final = {}
        keys = hasil_golongan[gol_keys[0]].keys()

        for k in keys:
            total_val = 0

            for i, gol in enumerate(gol_keys):
                total_val += hasil_golongan[gol][k] * weight_gol[i]

            hasil_final[k] = round(total_val, 6)

        return hasil_final