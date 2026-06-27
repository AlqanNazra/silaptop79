from django.test import TestCase
import psycopg2

from dss.services.service_swara import ServiceSwara
from dss.services.service_agregiasi import AggregationService
from dss.services.service_normalisasi import NormalizationService


class TestDSSPipeline(TestCase):

    def setUp(self):

        self.raw_conn = psycopg2.connect(
            dbname="TA",
            user="postgres",
            password="190105",
            host="127.0.0.1",
            port="5433"
        )

        self.swara = ServiceSwara(
            self.raw_conn
        )

        self.aggregate = AggregationService(
            self.raw_conn
        )

        # =========================
        # KHUSUS SWARA
        # =========================

        self.swara_roles = [
            "Backend Developer",
            "Data Engineer"
        ]

        # =========================
        # KHUSUS AGGREGATE
        # =========================

        self.aggregate_roles = [
            {
                "role": "Backend Developer",
                "weight": 0.7
            },
            {
                "role": "Data Engineer",
                "weight": 0.3
            }
        ]

    def tearDown(self):
        self.raw_conn.close()

    def test_1_ambil_dan_gabung_bobot(self):

        hasil = self.swara.ambil_dan_gabung_bobot(
            self.swara_roles
        )

        print("\n=== TEST 1 : AMBIL DAN GABUNG BOBOT ===")

        for h in hasil:
            print(h)

        self.assertTrue(len(hasil) > 0)

    # =====================================================
    # 2. TEST SORT KRITERIA
    # =====================================================

    def test_2_pengurutan_kriteria(self):

        sorted_kriteria, meta = (
            self.swara.pengurutan_kriteria(
                self.swara_roles
            )
        )

        print("\n=== TEST 2 : SORT KRITERIA ===")

        for item in sorted_kriteria:
            print(item)

        self.assertTrue(
            sorted_kriteria[0][1]
            >=
            sorted_kriteria[-1][1]
        )

    # =====================================================
    # 3. TEST HITUNG SJ
    # =====================================================

    def test_3_hitung_sj(self):

        sorted_kriteria, meta = (
            self.swara.pengurutan_kriteria(
                self.swara_roles
            )
        )

        sj = self.swara.mencari_nilai_sj(
            sorted_kriteria
        )

        print("\n=== TEST 3 : HITUNG SJ ===")

        for i, item in enumerate(sj):
            print(f"SJ-{i+1}: {item}")

        self.assertEqual(sj[0], 0)

    # =====================================================
    # 4. TEST HITUNG KJ
    # =====================================================

    def test_4_hitung_kj(self):

        sorted_kriteria, meta = (
            self.swara.pengurutan_kriteria(
                self.swara_roles
            )
        )

        sj = self.swara.mencari_nilai_sj(
            sorted_kriteria
        )

        kj = self.swara.menghitung_kj(sj)

        print("\n=== TEST 4 : HITUNG KJ ===")

        for i, item in enumerate(kj):
            print(f"KJ-{i+1}: {item}")

        self.assertEqual(kj[0], 1)

    # =====================================================
    # 5. TEST HITUNG QJ
    # =====================================================

    def test_5_hitung_qj(self):

        sorted_kriteria, meta = (
            self.swara.pengurutan_kriteria(
                self.swara_roles
            )
        )

        sj = self.swara.mencari_nilai_sj(
            sorted_kriteria
        )

        kj = self.swara.menghitung_kj(sj)

        qj = self.swara.menghitung_qj(kj)

        print("\n=== TEST 5 : HITUNG QJ ===")

        for i, item in enumerate(qj):
            print(f"QJ-{i+1}: {item}")

        self.assertEqual(qj[0], 1)

    # =====================================================
    # 6. TEST NORMALISASI BOBOT
    # =====================================================

    def test_6_normalisasi_bobot(self):

        sorted_kriteria, meta = (
            self.swara.pengurutan_kriteria(
                self.swara_roles
            )
        )

        sj = self.swara.mencari_nilai_sj(
            sorted_kriteria
        )

        kj = self.swara.menghitung_kj(sj)

        qj = self.swara.menghitung_qj(kj)

        hasil = self.swara.normalisasi_bobot(
            qj,
            sorted_kriteria,
            meta
        )

        print("\n=== TEST 6 : NORMALISASI ===")

        total = 0

        for item in hasil:

            print(item)

            total += item["bobot_akhir"]

        print("\nTOTAL =", total)

        self.assertAlmostEqual(
            total,
            1.0,
            places=3
        )

    # =====================================================
    # 7. TEST FULL SWARA
    # =====================================================

    def test_7_full_swara(self):

        hasil = self.swara.proses_swara(
            self.swara_roles
        )

        print("\n=== TEST 7 : FULL SWARA ===")

        print("\nSORTED")
        print(hasil["data"]["sorted"])

        print("\nSJ")
        print(hasil["data"]["sj"])

        print("\nKJ")
        print(hasil["data"]["kj"])

        print("\nQJ")
        print(hasil["data"]["qj"])

        print("\nHASIL AKHIR")

        total = 0

        for item in hasil["data"]["bobot_akhir"]:

            print(item)

            total += item["bobot_akhir"]

        print("\nTOTAL =", total)

        self.assertEqual(
            hasil["status"],
            "success"
        )

        self.assertAlmostEqual(
            total,
            1.0,
            places=3
        )

    def test_5_full_pipeline(self):

        hasil_swara = {}

        # =========================
        # SWARA PER ROLE
        # =========================

        for role_name in self.swara_roles:

            swara = (
                self.swara
                .proses_swara([role_name])
            )

            bobot = {}

            for item in swara["data"]["bobot_akhir"]:

                bobot[
                    item["nama_kriteria"]
                ] = item["bobot_akhir"]

            hasil_swara[role_name] = bobot

        print("\n=== HASIL SWARA ===")

        for k, v in hasil_swara.items():
            print(k, v)

        # =========================
        # AGGREGATE
        # =========================

        aggregate_result = (
            self.aggregate
            .aggregate_role_weight(
                self.aggregate_roles,
                hasil_swara
            )
        )

        print("\n=== HASIL AGGREGATE ===")

        for k, v in aggregate_result.items():
            print(k, v)

        # =========================
        # NORMALISASI
        # =========================

        normalized = (
            NormalizationService
            .normalize_weight(
                aggregate_result
            )
        )

        print("\n=== HASIL NORMALISASI ===")

        total = 0

        for k, v in normalized.items():

            print(f"{k} = {v}")

            total += v

        print("\nTOTAL =", total)

        self.assertAlmostEqual(
            total,
            1.0,
            places=5
        )

        self.assertTrue(
            NormalizationService
            .validate_normalization(
                normalized
            )
        )