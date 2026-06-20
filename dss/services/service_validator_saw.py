# dss/services/service_validator_saw.py

class ServiceValidatorSAW:

    def __init__(self):
        self.errors = []
        self.warnings = []

    # =====================================
    # HELPER
    # =====================================

    def add_error(self, msg):
        self.errors.append(msg)

    def add_warning(self, msg):
        self.warnings.append(msg)

    # =====================================
    # VALIDASI BOBOT
    # =====================================

    def validate_bobot(self, bobot):

        print("\n" + "=" * 50)
        print("VALIDASI BOBOT")
        print("=" * 50)

        total = 0

        for nama, nilai in bobot.items():

            print(
                f"{nama:<15}: {nilai}"
            )

            if nilai is None:
                self.add_error(
                    f"Bobot {nama} bernilai NULL"
                )
                continue

            if nilai < 0:
                self.add_error(
                    f"Bobot {nama} negatif"
                )

            total += float(nilai)

        print("-" * 50)
        print("TOTAL =", round(total, 6))

        if abs(total - 1) > 0.001:
            self.add_error(
                f"Total bobot tidak sama dengan 1 ({total})"
            )

        return len(self.errors) == 0

    # =====================================
    # VALIDASI DATA ALTERNATIF
    # =====================================

    def validate_alternatif(self, data):

        print("\n" + "=" * 50)
        print("VALIDASI DATA ALTERNATIF")
        print("=" * 50)

        if not data:

            self.add_error(
                "Data alternatif kosong"
            )

            return False

        required = [
            "processor",
            "ram",
            "storage",
            "berat",
            "layar",
            "baterai"
        ]

        for item in data:

            nama = (
                item.get("nama")
                or item.get("id")
                or "UNKNOWN"
            )

            for field in required:

                if field not in item:

                    self.add_error(
                        f"{nama} tidak memiliki field {field}"
                    )

                    continue

                nilai = item[field]

                if nilai is None:

                    self.add_error(
                        f"{nama} -> {field} NULL"
                    )

                if (
                    isinstance(
                        nilai,
                        (int, float)
                    )
                    and nilai < 0
                ):
                    self.add_error(
                        f"{nama} -> {field} negatif"
                    )

            # warning khusus

            if item.get("berat") == 0:

                self.add_warning(
                    f"{nama} memiliki berat = 0"
                )

            if item.get("ram") == 0:

                self.add_warning(
                    f"{nama} memiliki RAM = 0"
                )

            if item.get("storage") == 0:

                self.add_warning(
                    f"{nama} memiliki Storage = 0"
                )

        print(
            f"Jumlah Alternatif: {len(data)}"
        )

        return len(self.errors) == 0

    # =====================================
    # VALIDASI NORMALISASI
    # =====================================

    def validate_normalisasi(self,data_normalisasi):
        print("\n" + "=" * 50)
        print("VALIDASI NORMALISASI")
        print("=" * 50)
        print(f"Jumlah Data : {len(data_normalisasi)}")

        if data_normalisasi:
            print("Sample Data :",data_normalisasi[0])

        for item in data_normalisasi:
            nama = (item.get("nama")or item.get("id")or "UNKNOWN")
            for key, value in item.items():
                if key in ["id", "nama"]:
                    continue
                if not isinstance(value,(int, float)):
                    continue
                if value < 0:
                    self.add_error(f"{nama} -> {key} < 0")
                if value > 1:
                    self.add_warning(f"{nama} -> {key} > 1 ({value})")

        return len(self.errors) == 0

    # =====================================
    # VALIDASI SKOR SAW
    # =====================================

    def validate_skor(self,ranking):
        print("\n" + "=" * 50)
        print("VALIDASI SKOR SAW")
        print("=" * 50)
        print(f"Jumlah Ranking : {len(ranking)}")
        if ranking:
            skor_list = [
                item["skor"]
                for item in ranking
                if "skor" in item
            ]
            print(f"Skor Tertinggi : {max(skor_list):.6f}")
            print(f"Skor Terendah  : {min(skor_list):.6f}")
            print("Top 3 Ranking :")
            for item in ranking[:3]:
                print(
                    f"  {item.get('rank','-')} | "
                    f"{item.get('id')} | "
                    f"{item.get('skor')}"
                )
        for item in ranking:
            skor = (
                item.get("skor")
                or item.get("nilai_saw")
                or item.get("score")
            )
            nama = (
                item.get("nama")
                or item.get("id")
                or "UNKNOWN"
            )
            if skor is None:
                self.add_error(f"{nama} tidak memiliki skor")
                continue
            if skor < 0:
                self.add_error(f"{nama} skor negatif")

            if skor > 1.5:
                self.add_warning(f"{nama} skor terlalu besar ({skor})")

        return len(self.errors) == 0

    # =====================================
    # VALIDASI RANKING
    # =====================================

    def validate_ranking(self,ranking):
        print("\n" + "=" * 50)
        print("VALIDASI RANKING")
        print("=" * 50)
        print(f"Jumlah Ranking : {len(ranking)}")
        if ranking:
            print("Peringkat Pertama :",ranking[0])
            print("Peringkat Terakhir :",ranking[-1])
        prev = None
        for item in ranking:
            skor = (
                item.get("skor")
                or item.get("nilai_saw")
                or item.get("score")
            )
            if skor is None:
                continue
            if (
                prev is not None
                and skor > prev
            ):
                self.add_error("Ranking tidak terurut DESC")

            prev = skor

        return len(self.errors) == 0

    # =====================================
    # LAPORAN
    # =====================================

    def print_report(self):

        print("\n" + "=" * 60)
        print("HASIL VALIDASI DSS SAW")
        print("=" * 60)

        if not self.errors:

            print("STATUS : VALID")

        else:

            print("STATUS : INVALID")

        print("\nERROR:")

        if self.errors:

            for err in self.errors:
                print("-", err)

        else:
            print("Tidak ada")

        print("\nWARNING:")

        if self.warnings:

            for warn in self.warnings:
                print("-", warn)

        else:
            print("Tidak ada")

        print("=" * 60)

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings
        }