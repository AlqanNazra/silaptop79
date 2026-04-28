from dss.repositories.repositori_bobot_kriteria import BobotKriteriaRepository
from dss.repositories.repositori_kriteria import KriteriaRepository
from ..repositories.dto.dto_bobot_kriteria import BobotKriteriaDTO
from ..repositories.dto.dto_kriteria import KriteriaDTO
from collections import defaultdict


class ServiceSwara:

    def __init__(self, conn):
        self.conn = conn
        self.repoBK = BobotKriteriaRepository(conn)
        self.repoK = KriteriaRepository(conn)
        
    def ambil_dan_gabung_bobot(self, list_role: list[str]):
        data = self.repoBK.cari_bobot_kriteria_by_roles(list_role)
        
        # Code Testing
        print("DATA RAW DB:", data)
        print("REPO TYPE:", type(self.repoBK))
        print("METHOD EXIST:", hasattr(self.repoBK, "cari_bobot_kriteria_by_roles"))

        if not data:
            raise Exception("Data bobot kosong")

        group = defaultdict(list)
        meta = {}

        for item in data:
            group[item["id_kriteria"]].append(item["nilai_bobot"])

            meta[item["id_kriteria"]] = {
                "nama_kriteria": item["nama_kriteria"],
                "tipe_kriteria": item.get("tipe_kriteria", "benefit")
            }

        hasil = []

        for kriteria_id, values in group.items():
            hasil.append({
                "id_kriteria": kriteria_id,
                "nama_kriteria": meta[kriteria_id]["nama_kriteria"],
                "tipe_kriteria": meta[kriteria_id]["tipe_kriteria"],
                "nilai_bobot": sum(values) / len(values)
            })

        return hasil

    def pengurutan_kriteria(self, roles):
        data = self.ambil_dan_gabung_bobot(roles)

        if len(data) < 2:
            raise Exception("Minimal 2 kriteria untuk SWARA")

        sorted_kriteria = sorted(
            data,
            key=lambda x: x["nilai_bobot"],
            reverse=True
        )

        meta = {
            d["nama_kriteria"]: {
                "id_kriteria": d["id_kriteria"],
                "tipe_kriteria": d["tipe_kriteria"]
            }
            for d in sorted_kriteria
        }

        sorted_simple = [
            (d["nama_kriteria"], d["nilai_bobot"])
            for d in sorted_kriteria
        ]

        return sorted_simple, meta

    def mencari_nilai_sj(self, sorted_kriteria):
        sj = []

        for i in range(len(sorted_kriteria)):
            if i == 0:
                sj.append(0)
            else:
                prev = sorted_kriteria[i - 1][1]
                curr = sorted_kriteria[i][1]
                if prev == 0:
                    nilai = 0
                else:
                    nilai = (prev - curr) / prev

                sj.append(round(nilai, 4))

        return sj

    def menghitung_kj(self, sj):
        kj = []

        for i in range(len(sj)):
            if i == 0:
                kj.append(1)
            else:
                kj.append(round(sj[i] + 1, 4))

        return kj

    def menghitung_qj(self, kj):
        qj = []

        for i in range(len(kj)):
            if i == 0:
                qj.append(1)
            else:
                qj.append(round(qj[i - 1] / kj[i], 6))

        return qj

    def normalisasi_bobot(self, qj, sorted_kriteria, meta):
        total = sum(qj)

        if total == 0:
            raise Exception("Total qj tidak boleh 0")

        hasil = []

        for i in range(len(qj)):
            nama = sorted_kriteria[i][0]

            hasil.append({
                "id_kriteria": meta[nama]["id_kriteria"],
                "nama_kriteria": nama,
                "tipe_kriteria": meta[nama]["tipe_kriteria"],
                "bobot_akhir": round(qj[i] / total, 6)
            })

        return hasil
    
    def proses_swara(self, role: list, id_bobot=None):

        try:
            with self.conn:
                sorted_kriteria, meta = self.pengurutan_kriteria(role)
                print("STEP 1 - SORTED:", sorted_kriteria)

                sj = self.mencari_nilai_sj(sorted_kriteria)
                print("STEP 2 - SJ:", sj)

                kj = self.menghitung_kj(sj)
                print("STEP 3 - KJ:", kj)

                qj = self.menghitung_qj(kj)
                print("STEP 4 - QJ:", qj)

                hasil = self.normalisasi_bobot(qj, sorted_kriteria, meta)
                print("STEP 5 - HASIL:", hasil)

                total = sum([h["bobot_akhir"] for h in hasil])
                print("TOTAL:", total)

                if abs(total - 1) > 0.001:
                    raise Exception("Bobot SWARA tidak valid")

                return {
                    "status": "success",
                    "data": {
                        "sorted": sorted_kriteria,
                        "sj": sj,
                        "kj": kj,
                        "qj": qj,
                        "bobot_akhir": hasil
                    }
                }

        except Exception as e:
            print("ERROR:", str(e))  # 🔥 penting
            return {
                "status": "error",
                "message": str(e)
            }