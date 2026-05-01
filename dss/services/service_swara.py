from dss.repositories.repositori_bobot_kriteria import BobotKriteriaRepository
from dss.repositories.repositori_kriteria import KriteriaRepository
from collections import defaultdict
import json

DEBUG = False  # 🔥 ubah True kalau mau debug


def debug_print(title, data):
    if DEBUG:
        print(f"\n=== {title} ===")
        print(json.dumps(data, indent=4, default=str))


class ServiceSwara:

    def __init__(self, conn):
        self.conn = conn
        self.repoBK = BobotKriteriaRepository(conn)
        self.repoK = KriteriaRepository(conn)

    def ambil_dan_gabung_bobot(self, list_role: list[str]):
        data = self.repoBK.cari_bobot_kriteria_by_roles(list_role)

        debug_print("DATA RAW DB", data)

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

        debug_print("HASIL GABUNG", hasil)

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

        debug_print("STEP 1 - SORTED", sorted_simple)

        return sorted_simple, meta

    def mencari_nilai_sj(self, sorted_kriteria):
        sj = []

        for i in range(len(sorted_kriteria)):
            if i == 0:
                sj.append(0)
            else:
                prev = sorted_kriteria[i - 1][1]
                curr = sorted_kriteria[i][1]
                nilai = (prev - curr) / prev if prev != 0 else 0
                sj.append(round(nilai, 4))

        debug_print("STEP 2 - SJ", sj)

        return sj

    def menghitung_kj(self, sj):
        kj = []

        for i in range(len(sj)):
            if i == 0:
                kj.append(1)
            else:
                kj.append(round(sj[i] + 1, 4))

        debug_print("STEP 3 - KJ", kj)

        return kj

    def menghitung_qj(self, kj):
        qj = []

        for i in range(len(kj)):
            if i == 0:
                qj.append(1)
            else:
                qj.append(round(qj[i - 1] / kj[i], 6))

        debug_print("STEP 4 - QJ", qj)

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

        debug_print("STEP 5 - HASIL", hasil)

        return hasil

    def proses_swara(self, role: list):

        try:
            with self.conn:
                sorted_kriteria, meta = self.pengurutan_kriteria(role)
                sj = self.mencari_nilai_sj(sorted_kriteria)
                kj = self.menghitung_kj(sj)
                qj = self.menghitung_qj(kj)
                hasil = self.normalisasi_bobot(qj, sorted_kriteria, meta)

                total = sum([h["bobot_akhir"] for h in hasil])

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
            return {
                "status": "error",
                "message": str(e)
            }