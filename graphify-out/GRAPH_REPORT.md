# Graph Report - .  (2026-06-07)

## Corpus Check
- 196 files · ~50,512 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 837 nodes · 1227 edges · 113 communities (69 shown, 44 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 131 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_DSS Proses Core|DSS Proses Core]]
- [[_COMMUNITY_SAW Algorithm Engine|SAW Algorithm Engine]]
- [[_COMMUNITY_DSS Result DTOs|DSS Result DTOs]]
- [[_COMMUNITY_Core View Routing|Core View Routing]]
- [[_COMMUNITY_Database Seeders|Database Seeders]]
- [[_COMMUNITY_Peminjaman Service|Peminjaman Service]]
- [[_COMMUNITY_Pengajuan Service|Pengajuan Service]]
- [[_COMMUNITY_Laptop Inventori CRUD|Laptop Inventori CRUD]]
- [[_COMMUNITY_SQL Schema Definitions|SQL Schema Definitions]]
- [[_COMMUNITY_Inventori Views Controller|Inventori Views Controller]]
- [[_COMMUNITY_Storage Repository|Storage Repository]]
- [[_COMMUNITY_Bobot Kriteria Interface|Bobot Kriteria Interface]]
- [[_COMMUNITY_Processor CRUD Service|Processor CRUD Service]]
- [[_COMMUNITY_Riwayat Aktivitas|Riwayat Aktivitas]]
- [[_COMMUNITY_DSS Kriteria DTOs|DSS Kriteria DTOs]]
- [[_COMMUNITY_Laptop Pengadaan DTO|Laptop Pengadaan DTO]]
- [[_COMMUNITY_HC Template Hierarchy|HC Template Hierarchy]]
- [[_COMMUNITY_Pengadaan Repository|Pengadaan Repository]]
- [[_COMMUNITY_Hasil SAW Service|Hasil SAW Service]]
- [[_COMMUNITY_SWARA Testing Views|SWARA Testing Views]]
- [[_COMMUNITY_Module Group 20|Module Group 20]]
- [[_COMMUNITY_Module Group 21|Module Group 21]]
- [[_COMMUNITY_Module Group 22|Module Group 22]]
- [[_COMMUNITY_Module Group 23|Module Group 23]]
- [[_COMMUNITY_Module Group 24|Module Group 24]]
- [[_COMMUNITY_Module Group 25|Module Group 25]]
- [[_COMMUNITY_Module Group 26|Module Group 26]]
- [[_COMMUNITY_Module Group 27|Module Group 27]]
- [[_COMMUNITY_Module Group 28|Module Group 28]]
- [[_COMMUNITY_Module Group 29|Module Group 29]]
- [[_COMMUNITY_Module Group 30|Module Group 30]]
- [[_COMMUNITY_Module Group 31|Module Group 31]]
- [[_COMMUNITY_Module Group 32|Module Group 32]]
- [[_COMMUNITY_Module Group 33|Module Group 33]]
- [[_COMMUNITY_Module Group 34|Module Group 34]]
- [[_COMMUNITY_Module Group 35|Module Group 35]]
- [[_COMMUNITY_Module Group 36|Module Group 36]]
- [[_COMMUNITY_Module Group 37|Module Group 37]]
- [[_COMMUNITY_Module Group 38|Module Group 38]]
- [[_COMMUNITY_Module Group 39|Module Group 39]]
- [[_COMMUNITY_Module Group 40|Module Group 40]]
- [[_COMMUNITY_Module Group 41|Module Group 41]]
- [[_COMMUNITY_Module Group 42|Module Group 42]]
- [[_COMMUNITY_Module Group 43|Module Group 43]]
- [[_COMMUNITY_Module Group 44|Module Group 44]]
- [[_COMMUNITY_Module Group 45|Module Group 45]]
- [[_COMMUNITY_Module Group 46|Module Group 46]]
- [[_COMMUNITY_Module Group 47|Module Group 47]]
- [[_COMMUNITY_Module Group 48|Module Group 48]]
- [[_COMMUNITY_Module Group 49|Module Group 49]]
- [[_COMMUNITY_Module Group 50|Module Group 50]]
- [[_COMMUNITY_Module Group 51|Module Group 51]]
- [[_COMMUNITY_Module Group 52|Module Group 52]]
- [[_COMMUNITY_Module Group 53|Module Group 53]]
- [[_COMMUNITY_Module Group 54|Module Group 54]]
- [[_COMMUNITY_Module Group 55|Module Group 55]]
- [[_COMMUNITY_Module Group 56|Module Group 56]]
- [[_COMMUNITY_Module Group 57|Module Group 57]]
- [[_COMMUNITY_Module Group 58|Module Group 58]]
- [[_COMMUNITY_Module Group 59|Module Group 59]]
- [[_COMMUNITY_Module Group 60|Module Group 60]]
- [[_COMMUNITY_Module Group 61|Module Group 61]]
- [[_COMMUNITY_Module Group 62|Module Group 62]]
- [[_COMMUNITY_Module Group 64|Module Group 64]]
- [[_COMMUNITY_Module Group 65|Module Group 65]]
- [[_COMMUNITY_Module Group 67|Module Group 67]]
- [[_COMMUNITY_Module Group 68|Module Group 68]]
- [[_COMMUNITY_Module Group 69|Module Group 69]]
- [[_COMMUNITY_Module Group 76|Module Group 76]]
- [[_COMMUNITY_Module Group 84|Module Group 84]]
- [[_COMMUNITY_Module Group 99|Module Group 99]]
- [[_COMMUNITY_Module Group 100|Module Group 100]]
- [[_COMMUNITY_Module Group 101|Module Group 101]]
- [[_COMMUNITY_Module Group 102|Module Group 102]]

## God Nodes (most connected - your core abstractions)
1. `LaptopInventoriRepository` - 39 edges
2. `PeminjamanRepository` - 26 edges
3. `ServiceSwara` - 25 edges
4. `BobotKriteriaRepository` - 24 edges
5. `Servicesaw` - 24 edges
6. `LaptopPengadaanRepository` - 23 edges
7. `ProcessorRepository` - 22 edges
8. `Servicepreposesdata` - 19 edges
9. `PengajuanRepository` - 18 edges
10. `get_connection()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `SeederSAWReady` --uses--> `LaptopPengadaanDTO`  [INFERRED]
  tests/seeder_dss.py → dss/repositories/dto/dto_laptop_pengadaan.py
- `SeederSAWReady` --uses--> `BobotKriteriaRepository`  [INFERRED]
  tests/seeder_dss.py → dss/repositories/repositori_bobot_kriteria.py
- `SeederSAWReady` --uses--> `KriteriaRepository`  [INFERRED]
  tests/seeder_dss.py → dss/repositories/repositori_kriteria.py
- `SeederSAWReady` --uses--> `LaptopPengadaanRepository`  [INFERRED]
  tests/seeder_dss.py → dss/repositories/repositori_laptop_pengadaan.py
- `Servicepreposesdata` --uses--> `FilterInventoriDTO`  [INFERRED]
  dss/services/service_preposesdata.py → inventori/repositories/dto/dto_laptop_inventori.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **DSS Pipeline Tables** — crud_kriteria_table, crud_bobot_kriteria_table, crud_dss_proses_table, crud_nilai_alternatif_table, crud_hasil_saw_table, crud_detail_hasil_saw_table [EXTRACTED 0.95]
- **Hardware Specification Tables** — crud_processor_table, crud_ram_table, crud_storage_table [EXTRACTED 0.95]
- **HC DSS Recommendation Flow** — template_hc_input_kriteria, template_hc_hasil_rekomendasi, template_hc_detail_rekomendasi, template_hc_detail_scrapping [INFERRED 0.85]
- **HC Inventory Management Flow** — template_hc_manajemen_laptop, template_hc_detail_laptop, template_hc_edit_laptop, template_hc_detail_pengajuan [INFERRED 0.85]
- **Talent User Workflow** — template_talent_dashboard, template_talent_pengajuan, template_talent_detail_laptop, template_talent_riwayat, template_talent_pengembalian [INFERRED 0.85]

## Communities (113 total, 44 thin omitted)

### Community 0 - "DSS Proses Core"
Cohesion: 0.05
Nodes (18): AlternatifDssDTO, DssProsesDTO, AlternatifDssDTO, DssProsesDTO, IDssProssesRepositoryImpl, AlternatifDssDTO, DssProsesDTO, IAlternatifDssImpl (+10 more)

### Community 1 - "SAW Algorithm Engine"
Cohesion: 0.06
Nodes (23): Servicesaw, buat_data_preprocessed(), cetak_summary(), DummySawService, DummySwaraService, jalankan_simulasi(), int, simulate_saw.py ================ Simulasi SWARA-SAW — 25 Kasus menggunakan modul (+15 more)

### Community 2 - "DSS Result DTOs"
Cohesion: 0.07
Nodes (12): DetailHasilSawDTO, HasilSAWDTO, DetailHasilSawDTO, HasilSAWDTO, IDetailHasilSawImpl, IHasilSawRepositoryImpl, IDetailHasilSaw, IDetailHasilSawImpl (+4 more)

### Community 3 - "Core View Routing"
Cohesion: 0.10
Nodes (37): dashboard_hc_view(), dashboard_it_view(), dashboard_talent_view(), detaillaptop_hc_view(), detaillaptop_it_view(), detaillaptop_talent_view(), detailpengajuan_hc_view(), detailpengajuan_it_view() (+29 more)

### Community 4 - "Database Seeders"
Cohesion: 0.14
Nodes (21): BaseCommand, Command, Command, AlternatifDSS, BobotKriteria, DetailHasilSAW, DSSProses, HasilSAW (+13 more)

### Community 5 - "Peminjaman Service"
Cohesion: 0.12
Nodes (7): PeminjamanDTO, PeminjamanDTO, PeminjamanDTO, list_peminjaman_view(), tambah_peminjaman_view(), PeminjamanRepository, PeminjamanService

### Community 6 - "Pengajuan Service"
Cohesion: 0.13
Nodes (9): PengajuanDTO, PengajuanDTO, PengajuanDTO, list_pengajuan_view(), pengajuan_page_view(), Halaman daftar pengajuan laptop.     Mengambil data dari PengajuanService lalu r, tambah_pengajuan_view(), PengajuanRepository (+1 more)

### Community 7 - "Laptop Inventori CRUD"
Cohesion: 0.13
Nodes (4): ILaptopInventoriRepository, ReadLaptopInventoriService, UpdateLaptopInventoriService, LaptopInventoriRepository

### Community 8 - "SQL Schema Definitions"
Cohesion: 0.14
Nodes (19): Laptop Inventory Management, Alternatif DSS Table, Bobot Kriteria Table, Detail Hasil SAW Table, DSS Proses Table, Hasil SAW Table, Kriteria Table, Laptop Alternatif Table (+11 more)

### Community 9 - "Inventori Views Controller"
Cohesion: 0.20
Nodes (13): LaptopInventoriDTO, error_response(), laptop_detail(), laptop_list_create(), manajemen_laptop_page(), _parse_body(), processor_detail(), processor_list_create() (+5 more)

### Community 10 - "Storage Repository"
Cohesion: 0.17
Nodes (6): BaseRepository, IStorageRepository, str, BaseRepository, AlternatifDSSRepository, StorageDTO

### Community 12 - "Processor CRUD Service"
Cohesion: 0.15
Nodes (6): IProcessorRepository, CreateProcessorService, DeleteProcessorService, ReadProcessorService, UpdateProcessorService, ProcessorRepository

### Community 13 - "Riwayat Aktivitas"
Cohesion: 0.15
Nodes (3): RiwayatAktivitasDTO, RiwayatAktivitasRepository, RiwayatAktivitasDTO

### Community 14 - "DSS Kriteria DTOs"
Cohesion: 0.24
Nodes (3): BobotKriteriaDTO, KriteriaDTO, SeederSAWReady

### Community 16 - "HC Template Hierarchy"
Cohesion: 0.19
Nodes (13): Human Capital Role, Django Template Inheritance, Base Template, HC Dashboard Template, HC Detail Laptop, HC Detail Pengajuan, HC Detail Rekomendasi, HC Detail Rekomendasi Scrapping (+5 more)

### Community 17 - "Pengadaan Repository"
Cohesion: 0.19
Nodes (3): LaptopPengadaanDTO, ILaptopPengadaanRepositoryImpl, LaptopPengadaanRepository

### Community 18 - "Hasil SAW Service"
Cohesion: 0.21
Nodes (6): DetailHasilSawDTO, HasilSAWDTO, IDetailHasilSawImpl, IHasilSawRepositoryImpl, HasilSawService, Alur:         1. Buat hasil SAW         2. Simpan semua detail ranking

### Community 20 - "Module Group 20"
Cohesion: 0.32
Nodes (3): debug_print(), ServiceSwara, service_db()

### Community 24 - "Module Group 24"
Cohesion: 0.23
Nodes (3): RamDTO, RamDTO, RamRepository

### Community 25 - "Module Group 25"
Cohesion: 0.18
Nodes (6): AppConfig, CoreConfig, DssConfig, InventoriConfig, SeederConfig, UsersConfig

### Community 26 - "Module Group 26"
Cohesion: 0.20
Nodes (11): Role-Based View Separation, Talent Role, HC Pengajuan Laptop, HC Riwayat Peminjaman Laptop, Talent Dashboard Template, Talent Detail Laptop, Talent Pengajuan Laptop, Talent Pengembalian Laptop (+3 more)

### Community 27 - "Module Group 27"
Cohesion: 0.22
Nodes (4): ILaptopPengadaanRepositoryImpl, LaptopPengadaanDTO, str, LaptopPengadaanService

### Community 28 - "Module Group 28"
Cohesion: 0.27
Nodes (7): str, FilterInventoriDTO, FilterPengadaanDTO, FilterInventoriDTO, LaptopInventoriDetailDTO, DTO untuk parameter filter laptop inventori, Mengembalikan parameter dalam bentuk tuple sesuai urutan function SQL

### Community 29 - "Module Group 29"
Cohesion: 0.20
Nodes (4): str, str, KriteriaDTO, KriteriaRepository

### Community 32 - "Module Group 32"
Cohesion: 0.18
Nodes (7): FilterInventoriDTO, LaptopInventoriDetailDTO, DTO untuk parameter filter laptop inventori, Mengembalikan parameter dalam bentuk tuple sesuai urutan function SQL, float, int, str

### Community 36 - "Module Group 36"
Cohesion: 0.25
Nodes (5): float, int, str, FilterPengadaanDTO, test_dss_saw_pengadaan()

### Community 39 - "Module Group 39"
Cohesion: 0.39
Nodes (6): get_mock_bobot_roles(), service(), test_ambil_dan_gabung_bobot_multi_role(), test_multi_role_complex(), test_pengurutan_kriteria_real(), test_proses_swara_realcase()

### Community 46 - "Module Group 46"
Cohesion: 0.50
Nodes (3): float, int, str

### Community 47 - "Module Group 47"
Cohesion: 0.50
Nodes (3): detail_laptop_page(), Halaman detail laptop berdasarkan ID.     GET: Tampilkan detail lengkap laptop b, DeleteLaptopInventoriService

### Community 48 - "Module Group 48"
Cohesion: 0.67
Nodes (3): Full All Query SQL, Database Update Increment 2, Database Utility Queries

## Knowledge Gaps
- **49 isolated node(s):** `Migration`, `AlternatifDSS`, `Meta`, `str`, `float` (+44 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `LaptopInventoriRepository` connect `Laptop Inventori CRUD` to `SAW Algorithm Engine`, `Module Group 35`, `Module Group 36`, `Inventori Views Controller`, `Module Group 43`, `Module Group 44`, `Module Group 47`, `Pengadaan Repository`, `Module Group 22`, `Module Group 28`, `Module Group 29`?**
  _High betweenness centrality (0.196) - this node is a cross-community bridge._
- **Why does `ILaptopInventoriRepository` connect `Module Group 35` to `Module Group 40`, `Laptop Inventori CRUD`?**
  _High betweenness centrality (0.126) - this node is a cross-community bridge._
- **Why does `Servicesaw` connect `SAW Algorithm Engine` to `Laptop Inventori CRUD`, `Module Group 44`, `Pengadaan Repository`, `Module Group 20`, `Module Group 21`, `Module Group 29`?**
  _High betweenness centrality (0.081) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `LaptopInventoriRepository` (e.g. with `str` and `str`) actually correct?**
  _`LaptopInventoriRepository` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `PeminjamanRepository` (e.g. with `PeminjamanDTO` and `PeminjamanDTO`) actually correct?**
  _`PeminjamanRepository` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `ServiceSwara` (e.g. with `str` and `Servicesaw`) actually correct?**
  _`ServiceSwara` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `BobotKriteriaRepository` (e.g. with `str` and `str`) actually correct?**
  _`BobotKriteriaRepository` has 5 INFERRED edges - model-reasoned connections that need verification._