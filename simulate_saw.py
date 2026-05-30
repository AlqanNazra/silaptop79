"""
simulate_saw.py
================
Simulasi SWARA-SAW — 25 Kasus menggunakan modul asli dari dss/services.

Strategy
--------
- ServiceSwara  → di-subclass (DummySwaraService) sehingga `ambil_dan_gabung_bobot`
  mengembalikan data dummy tanpa menyentuh database.
- Servicesaw    → di-subclass (DummySawService) sehingga `normalisasi_saw` memakai
  tipe_kriteria dari dummy, dan SWARA yang dipakai adalah DummySwaraService.
- Semua matematika asli (Sj, Kj, Qj, normalisasi, ranking) tetap dipanggil dari
  modul orisinalnya.

Requirement
-----------
  venv/bin/python simulate_saw.py
"""

import os
import sys
import django
from collections import defaultdict

# ── Setup Django (dibutuhkan agar import app bisa jalan) ──────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

# ── Import modul ASLI dari aplikasi ───────────────────────────────────────────
from dss.services.service_swara import ServiceSwara
from dss.services.service_saw import Servicesaw

# =============================================================================
# DATA DUMMY
# =============================================================================

# 20 laptop alternatif — nilai sengaja dibuat overlapping agar ranking berubah
# antar skenario (saling bersaing di beberapa kriteria).
# Kolom: processor(score), ram(GB), storage(GB), berat(kg), layar(inch), baterai(Wh)
DUMMY_LAPTOPS = [
    # id    nama                       proc  ram  stor  berat  layar  baterai
    {"id": "L01", "nama": "ASUS ROG G1",        "processor": 14, "ram": 32, "storage": 1024, "berat": 2.5, "layar": 16.0, "baterai": 4500},
    {"id": "L02", "nama": "Lenovo ThinkPad X1", "processor": 13, "ram": 16, "storage": 512,  "berat": 1.3, "layar": 14.0, "baterai": 7200},
    {"id": "L03", "nama": "Dell XPS 15",        "processor": 14, "ram": 16, "storage": 512,  "berat": 1.8, "layar": 15.6, "baterai": 6500},
    {"id": "L04", "nama": "MacBook Pro 14",      "processor": 16, "ram": 16, "storage": 512,  "berat": 1.6, "layar": 14.2, "baterai": 7000},
    {"id": "L05", "nama": "HP Spectre 360",      "processor": 11, "ram":  8, "storage": 256,  "berat": 1.3, "layar": 13.5, "baterai": 6800},
    {"id": "L06", "nama": "Acer Swift 5",        "processor": 10, "ram":  8, "storage": 512,  "berat": 1.1, "layar": 14.0, "baterai": 7500},
    {"id": "L07", "nama": "MSI Raider GE",       "processor": 15, "ram": 32, "storage": 1024, "berat": 2.8, "layar": 17.3, "baterai": 5000},
    {"id": "L08", "nama": "Razer Blade 14",      "processor": 15, "ram": 16, "storage": 1024, "berat": 1.7, "layar": 14.0, "baterai": 4000},
    {"id": "L09", "naam": "ASUS Zenbook 14",     "processor": 12, "ram": 16, "storage": 512,  "berat": 1.4, "layar": 14.0, "baterai": 6600},
    {"id": "L10", "nama": "Microsoft Surface 4","processor": 12, "ram": 16, "storage": 256,  "berat": 1.3, "layar": 13.5, "baterai": 7000},
    {"id": "L11", "nama": "LG Gram 16",         "processor": 11, "ram": 16, "storage": 512,  "berat": 1.2, "layar": 16.0, "baterai": 8000},
    {"id": "L12", "nama": "HP EliteBook 840",   "processor": 13, "ram": 16, "storage": 512,  "berat": 1.5, "layar": 14.0, "baterai": 6000},
    {"id": "L13", "nama": "Lenovo IdeaPad 5",   "processor":  9, "ram": 16, "storage": 512,  "berat": 1.7, "layar": 15.6, "baterai": 5600},
    {"id": "L14", "nama": "Dell Inspiron 15",   "processor":  9, "ram":  8, "storage": 256,  "berat": 2.0, "layar": 15.6, "baterai": 5000},
    {"id": "L15", "nama": "ASUS VivoBook 15",   "processor":  8, "ram":  8, "storage": 256,  "berat": 1.8, "layar": 15.6, "baterai": 5000},
    {"id": "L16", "nama": "Acer Predator H500", "processor": 14, "ram": 32, "storage": 1024, "berat": 2.9, "layar": 15.6, "baterai": 4200},
    {"id": "L17", "nama": "HP Victus 16",       "processor": 12, "ram": 16, "storage": 512,  "berat": 2.3, "layar": 16.1, "baterai": 4600},
    {"id": "L18", "nama": "Lenovo Legion 5 Pro","processor": 14, "ram": 16, "storage": 512,  "berat": 2.4, "layar": 16.0, "baterai": 4700},
    {"id": "L19", "nama": "MacBook Air M2",     "processor": 15, "ram":  8, "storage": 256,  "berat": 1.2, "layar": 13.6, "baterai": 8000},
    {"id": "L20", "nama": "Samsung Galaxy Book", "processor": 11, "ram": 16, "storage": 512, "berat": 1.6, "layar": 15.6, "baterai": 6900},
]

# Pastikan setiap record punya key 'nama' (L09 ada typo 'naam')
for d in DUMMY_LAPTOPS:
    if "naam" in d:
        d["nama"] = d.pop("naam")

# Bobot "raw" awal SWARA untuk 1 role (format sama dengan output DB)
# Nilai ini adalah nilai preferensi, bukan bobot akhir — SWARA yang akan
# mengubahnya menjadi bobot ternormalisasi.
BASE_BOBOT_RAW = [
    {"id_kriteria": "K01", "nama_kriteria": "processor", "tipe_kriteria": "benefit", "nilai_bobot": 0.35},
    {"id_kriteria": "K02", "nama_kriteria": "ram",       "tipe_kriteria": "benefit", "nilai_bobot": 0.25},
    {"id_kriteria": "K03", "nama_kriteria": "storage",   "tipe_kriteria": "benefit", "nilai_bobot": 0.15},
    {"id_kriteria": "K04", "nama_kriteria": "berat",     "tipe_kriteria": "cost",    "nilai_bobot": 0.10},
    {"id_kriteria": "K05", "nama_kriteria": "layar",     "tipe_kriteria": "benefit", "nilai_bobot": 0.10},
    {"id_kriteria": "K06", "nama_kriteria": "baterai",   "tipe_kriteria": "benefit", "nilai_bobot": 0.05},
]

# Peta tipe kriteria (dipakai oleh DummySawService.normalisasi_saw)
TIPE_KRITERIA = {d["nama_kriteria"]: d["tipe_kriteria"] for d in BASE_BOBOT_RAW}

# =============================================================================
# SUBCLASS SWARA — Override bagian DB dengan dummy data
# =============================================================================

class DummySwaraService(ServiceSwara):
    """
    Menggunakan semua logika kalkulasi SWARA yang asli, hanya mengganti
    `ambil_dan_gabung_bobot` dan `proses_swara` agar tidak membutuhkan conn.
    """

    def __init__(self, bobot_raw: list):
        # Sengaja TIDAK memanggil super().__init__() agar tidak butuh conn
        self._bobot_raw = bobot_raw

    def ambil_dan_gabung_bobot(self, list_role):
        """Return dummy bobot_raw langsung tanpa DB."""
        return [d.copy() for d in self._bobot_raw]

    def proses_swara(self, role: list):
        """
        Override proses_swara agar tidak menggunakan `with self.conn`.
        Semua logika kalkulasi (pengurutan, sj, kj, qj, normalisasi)
        tetap dipanggil dari metode parent.
        """
        try:
            sorted_kriteria, meta = self.pengurutan_kriteria(role)
            sj    = self.mencari_nilai_sj(sorted_kriteria)
            kj    = self.menghitung_kj(sj)
            qj    = self.menghitung_qj(kj)
            hasil = self.normalisasi_bobot(qj, sorted_kriteria, meta)

            total = sum(h["bobot_akhir"] for h in hasil)
            if abs(total - 1) > 0.001:
                raise Exception(f"Bobot SWARA tidak valid (total={total})")

            return {
                "status": "success",
                "data": {
                    "sorted":      sorted_kriteria,
                    "sj":          sj,
                    "kj":          kj,
                    "qj":          qj,
                    "bobot_akhir": hasil,
                },
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}


# =============================================================================
# SUBCLASS SAW — Override bagian DB, pakai DummySwaraService
# =============================================================================

class DummySawService(Servicesaw):
    """
    Menggunakan semua logika kalkulasi SAW yang asli, hanya mengganti:
    - normalisasi_saw  → pakai TIPE_KRITERIA dummy (tidak butuh repoK)
    - servisBK (SWARA) → diganti dengan DummySwaraService
    """

    def __init__(self, bobot_raw: list):
        # Sengaja TIDAK memanggil super().__init__() agar tidak butuh conn
        self.servisBK = DummySwaraService(bobot_raw)

    def normalisasi_saw(self, data_preproses: list) -> list:
        """Override: gunakan TIPE_KRITERIA dummy, bukan dari self.repoK."""
        if not data_preproses:
            return []

        map_tipe = TIPE_KRITERIA          # pakai peta dummy
        keys = data_preproses[0].keys()

        max_values, min_values = {}, {}
        for key in keys:
            if key == "id":
                continue
            vals = [item[key] for item in data_preproses if item.get(key) is not None]
            max_values[key] = max(vals) if vals else 0
            min_values[key] = min(vals) if vals else 0

        hasil = []
        for item in data_preproses:
            normal_item = {"id": item["id"]}
            for key in keys:
                if key == "id":
                    continue
                tipe  = map_tipe.get(key, "benefit")
                nilai = item.get(key, 0)
                if nilai == 0:
                    normal_item[key] = 0
                elif tipe == "benefit":
                    normal_item[key] = nilai / max_values[key] if max_values[key] else 0
                else:  # cost
                    normal_item[key] = min_values[key] / nilai if nilai else 0
            hasil.append(normal_item)

        return hasil

    def get_bobot_saw(self, role: list) -> dict:
        """Override: panggil DummySwaraService, bukan servis DB."""
        hasil = self.servisBK.proses_swara(role)
        if hasil["status"] != "success":
            raise Exception(hasil["message"])
        return {
            item["nama_kriteria"]: item["bobot_akhir"]
            for item in hasil["data"]["bobot_akhir"]
        }

# =============================================================================
# DEFINISI 8 KOMBINASI × 3 PERSENTASE  (→ 24 kasus variasi + 1 baseline = 25)
# =============================================================================

KRITERIA_5 = ["processor", "ram", "storage", "berat", "layar"]

KOMBINASI_8 = [
    ["processor"],                            # 1 – hanya Processor
    ["ram"],                                  # 2 – hanya RAM
    ["storage"],                              # 3 – hanya Storage
    ["berat"],                                # 4 – hanya Berat
    ["layar"],                                # 5 – hanya Layar
    ["processor", "ram"],                     # 6 – Processor + RAM
    ["processor", "ram", "storage"],          # 7 – Processor + RAM + Storage
    ["processor", "ram", "storage", "berat", "layar"],  # 8 – Semua 5
]

PERSENTASE = [0.05, 0.10, 0.15]

# =============================================================================
# PERSIAPAN DATA PREPROCESSING (tanpa DB)
# =============================================================================

def buat_data_preprocessed() -> list:
    """
    Konversi DUMMY_LAPTOPS ke format yang diterima normalisasi_saw:
    dict {id, processor, ram, storage, berat, layar, baterai}
    """
    return [
        {
            "id":        d["id"],
            "processor": d["processor"],
            "ram":       d["ram"],
            "storage":   d["storage"],
            "berat":     d["berat"],
            "layar":     d["layar"],
            "baterai":   d["baterai"],
        }
        for d in DUMMY_LAPTOPS
    ]

ID_TO_NAMA = {d["id"]: d["nama"] for d in DUMMY_LAPTOPS}

# =============================================================================
# EKSEKUSI SIMULASI 25 KASUS
# =============================================================================

def jalankan_simulasi():
    print("=" * 70)
    print("         SIMULASI SWARA-SAW  ─  25 KASUS (Modul Asli + Dummy Data)")
    print("=" * 70)

    data_pre = buat_data_preprocessed()

    # laptop_id → {ranks: [], total_score: float, nama: str}
    laptop_stats = defaultdict(lambda: {"ranks": [], "total_score": 0.0, "nama": ""})
    detail_kasus  = []
    total_kasus   = 0

    def jalankan_satu(label: str, bobot_raw: list):
        nonlocal total_kasus
        total_kasus += 1

        # Inisialisasi service dengan dummy data yang sudah dimodifikasi
        saw_service = DummySawService(bobot_raw)

        # Normalisasi
        data_norm = saw_service.normalisasi_saw(data_pre)

        # Hitung skor (get_bobot_saw memanggil DummySwaraService.proses_swara)
        hasil_saw = saw_service.hitung_saw_data(data_norm, role=["Programmer"])

        # Ranking (metode asli dari Servicesaw)
        ranking = saw_service.ranking_saw(hasil_saw)
        for i, item in enumerate(ranking, 1):
            item["rank"] = i

        top20 = ranking[:20]
        for item in top20:
            lid = item["id"]
            laptop_stats[lid]["nama"] = ID_TO_NAMA.get(lid, lid)
            laptop_stats[lid]["ranks"].append(item["rank"])
            laptop_stats[lid]["total_score"] += item["skor"]

        detail_kasus.append({
            "label": label,
            "top5": [(item["id"], ID_TO_NAMA.get(item["id"], item["id"]), item["skor"])
                     for item in top20[:5]],
        })

        top1_nama = ID_TO_NAMA.get(top20[0]["id"], top20[0]["id"])
        print(f"  Kasus {total_kasus:02d}  [{label}]")
        print(f"          ↳ Rank 1: {top1_nama}  (skor={top20[0]['skor']:.5f})")

    # Kasus 0: Baseline
    jalankan_satu("Baseline", BASE_BOBOT_RAW)

    # Kasus 1-24: Variasi
    for idx, comb in enumerate(KOMBINASI_8, 1):
        for pct in PERSENTASE:
            label = f"K{idx} ({'+'.join(comb)}) +{int(pct*100)}%"
            modified = []
            for d in BASE_BOBOT_RAW:
                nd = d.copy()
                if nd["nama_kriteria"] in comb:
                    nd["nilai_bobot"] *= (1 + pct)
                modified.append(nd)
            jalankan_satu(label, modified)

    print(f"\n✓ Total kasus dieksekusi: {total_kasus}")
    return laptop_stats, total_kasus, detail_kasus

# =============================================================================
# TABEL KUANTITAS RANKING
# =============================================================================

def cetak_kuantitas_ranking(laptop_stats: dict):
    print("\n" + "=" * 90)
    print("    TABEL KUANTITAS RANKING — FREKUENSI SETIAP LAPTOP DI SETIAP POSISI RANK")
    print("=" * 90)

    header_rank = "".join([f"R{r:<3}" for r in range(1, 21)])
    print(f"{'Laptop':<28}" + header_rank)
    print("-" * 108)

    rows = sorted(laptop_stats.items(), key=lambda x: x[0])
    for lid, stats in rows:
        rank_freq = defaultdict(int)
        for r in stats["ranks"]:
            rank_freq[r] += 1
        row = f"{stats['nama']:<28}"
        for r in range(1, 21):
            row += f"{rank_freq.get(r, 0):<4}"
        print(row)

# =============================================================================
# FINAL SUMMARY RANKING + TIE-BREAKER
# =============================================================================

def cetak_summary(laptop_stats: dict, total_kasus: int):
    print("\n" + "=" * 90)
    print("           FINAL SUMMARY RANKING — TOP 20 LAPTOP")
    print("=" * 90)
    print("  Logika  : Frekuensi rank tertinggi → rank akhir laptop.")
    print("  Tie-Breaker: Bila frekuensi sama → rata-rata skor SAW tertinggi menang.\n")

    summary = []
    for lid, stats in laptop_stats.items():
        rank_freq = defaultdict(int)
        for r in stats["ranks"]:
            rank_freq[r] += 1

        max_freq  = max(rank_freq.values())
        best_rank = min(r for r, c in rank_freq.items() if c == max_freq)
        avg_score = stats["total_score"] / total_kasus

        summary.append({
            "id":         lid,
            "nama":       stats["nama"],
            "best_rank":  best_rank,
            "max_freq":   max_freq,
            "avg_score":  avg_score,
            "rank_freq":  dict(rank_freq),
        })

    # Sort primary: best_rank ASC, secondary: avg_score DESC
    summary.sort(key=lambda x: (x["best_rank"], -x["avg_score"]))

    # Deteksi posisi mana saja yang tie
    tie_notes = []
    seen_pairs = set()
    for i in range(len(summary)):
        for j in range(i + 1, len(summary)):
            a, b = summary[i], summary[j]
            if a["best_rank"] == b["best_rank"] and a["max_freq"] == b["max_freq"]:
                pair_key = (min(a["id"], b["id"]), max(a["id"], b["id"]))
                if pair_key not in seen_pairs:
                    seen_pairs.add(pair_key)
                    pemenang = a["nama"] if a["avg_score"] >= b["avg_score"] else b["nama"]
                    tie_notes.append(
                        f"  ⚠ SERI di Rank-{a['best_rank']}: "
                        f"'{a['nama']}' (avg={a['avg_score']:.5f}) vs "
                        f"'{b['nama']}' (avg={b['avg_score']:.5f})  → Pemenang: {pemenang}"
                    )

    tied_ids = {n for note in tie_notes for n in [s["id"] for s in summary if s["nama"] in note]}

    fmt = "  {:<4} {:<28} {:<16} {:<12} {:<15} {}"
    print(fmt.format("Rank", "Nama Laptop", "Freq Rank", "Kuantitas", "Avg SAW Score", ""))
    print("  " + "-" * 85)

    for i, item in enumerate(summary[:20], 1):
        flag = " ⚡ tie" if item["id"] in tied_ids else ""
        print(fmt.format(
            i,
            item["nama"],
            f"Rank {item['best_rank']}",
            f"x{item['max_freq']}",
            f"{item['avg_score']:.5f}",
            flag
        ))

    if tie_notes:
        print("\n── Log Tie-Breaker ─────────────────────────────────────────────────────────")
        for note in tie_notes:
            print(note)

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    laptop_stats, total_kasus, detail_kasus = jalankan_simulasi()
    cetak_kuantitas_ranking(laptop_stats)
    cetak_summary(laptop_stats, total_kasus)
    print("\n✓ Selesai.")
