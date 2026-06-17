from datetime import datetime
import random

# DTO
from dss.repositories.dto.dto_kriteria import KriteriaDTO
from dss.repositories.dto.dto_bobot_kriteria import BobotKriteriaDTO
from dss.repositories.dto.dto_laptop_pengadaan import LaptopPengadaanDTO

# REPO
from dss.repositories.repositori_kriteria import KriteriaRepository
from dss.repositories.repositori_bobot_kriteria import BobotKriteriaRepository
from dss.repositories.repositori_laptop_pengadaan import LaptopPengadaanRepository


class SeederSAWReady:

    def __init__(self, conn):
        self.conn = conn
        self.repoK = KriteriaRepository(conn)
        self.repoBK = BobotKriteriaRepository(conn)
        self.repoLP = LaptopPengadaanRepository(conn)

    def seed_all(self):
        self.seed_kriteria()
        self.seed_bobot()

    # =========================
    # 1. KRITERIA (WAJIB MATCH SAW)
    # =========================
    def seed_kriteria(self):
        print("Seeding Kriteria...")

        data = [
            KriteriaDTO(None, "processor", "benefit", "hardware"),
            KriteriaDTO(None, "ram", "benefit", "hardware"),
            KriteriaDTO(None, "storage", "benefit", "hardware"),
            KriteriaDTO(None, "berat", "cost", "fisik"),
            KriteriaDTO(None, "layar", "benefit", "fisik"),
            KriteriaDTO(None, "baterai", "benefit", "fisik"),
        ]

        for k in data:
            try:
                self.repoK.tambah_kriteria(k)
            except Exception as e:
                print("Skip kriteria:", e)

    # =========================
    # 2. BOBOT (VARIASI ROLE)
    # =========================
    def seed_bobot(self):
        print("Seeding Bobot...")

        roles = {
            "Backend":  [0.9, 0.8, 0.7, 0.3, 0.5, 0.6],
            "Frontend": [0.7, 0.8, 0.6, 0.5, 0.9, 0.7],
            "Data":     [0.95, 0.85, 0.75, 0.4, 0.5, 0.8],
        }

        for role, bobot_list in roles.items():
            for i, nilai in enumerate(bobot_list, start=1):
                dto = BobotKriteriaDTO(
                    id_kriteria=i,
                    role=role,
                    nilai_bobot=nilai
                )
                try:
                    self.repoBK.tambah_bobot_kriteria(dto)
                except Exception as e:
                    print("Skip bobot:", e)
