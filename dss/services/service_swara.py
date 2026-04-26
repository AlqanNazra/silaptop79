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
        
    def ambil_dan_gabung_bobot(self, list_role: list[str]):
        semua_bobot = []
        for role in list_role:
            data = self.repoBK.cari_bobot_kriteria_by_role(role)
            semua_bobot.append(data)
        hasil = {}
        keys = semua_bobot[0].keys()

        for k in keys:
            total = 0
            for bobot in semua_bobot:
                total += bobot[k]

            hasil[k] = total / len(semua_bobot)

        return hasil

    def pengurutan_kriteria(self, role):
        data = self.ambil_dan_gabung_bobot(role)

        if not data:
            raise Exception("Data bobot kosong")

        group = defaultdict(list)
        meta = {}

        for d in data:
            group[d["nama_kriteria"]].append(d["nilai_bobot"])
            meta[d["nama_kriteria"]] = {
                "id_kriteria": d["id_kriteria"],
                "tipe_kriteria": d.get("tipe_kriteria", "benefit")
            }

        rata = {
            k: sum(v) / len(v)
            for k, v in group.items()
        }

        sorted_kriteria = sorted(rata.items(), key=lambda x: x[1], reverse=True)

        if len(sorted_kriteria) < 2:
            raise Exception("Minimal 2 kriteria untuk SWARA")

        return sorted_kriteria, meta

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
    
    def proses_swara(self, role,id_bobot):

        try:
            with self.conn:
                sorted_kriteria, meta = self.pengurutan_kriteria(role)
                sj = self.mencari_nilai_sj(sorted_kriteria)
                kj = self.menghitung_kj(sj)
                qj = self.menghitung_qj(kj)
                hasil = self.normalisasi_bobot(qj, sorted_kriteria, meta) 
                total = sum([h["bobot_akhir"] for h in hasil])
                if round(total, 5) != 1:
                    raise Exception("Bobot SWARA tidak valid")
                for item in hasil:
                    bobot_dto = BobotKriteriaDTO(
                        id_kriteria=item["id_kriteria"],
                        role=role,
                        nilai_swara=item["bobot_akhir"]
                    )

                    self.repoBK.update_nilai_swara(bobot_dto)
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
            
# 