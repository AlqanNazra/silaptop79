<div align="center">

# 💻 SILAPTOP79

### Sistem Informasi Laptop Padepokan 79

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://w3.org)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://w3.org)

<br/>

> Aplikasi web berbasis Django untuk manajemen inventori laptop, pengelolaan peminjaman/distribusi perangkat, dan sistem pengambilan keputusan (DSS) pemilihan laptop menggunakan metode SWARA-SAW di PT Padepokan Tujuh Sembilan.

<br/>

[🚀 Mulai Cepat](#%EF%B8%8F-instalasi) · [📖 Fitur](#-fitur-utama) · [🧑‍💻 Teknologi](#%EF%B8%8F-teknologi-yang-digunakan) · [📊 Alur DSS](#-alur-dss) · [👥 Tim](#-tim-pengembang)

</div>

---

## 📖 Tentang Proyek

**SILAPTOP79** adalah aplikasi manajemen aset laptop berbasis web yang dikembangkan untuk PT Padepokan Tujuh Sembilan. Sistem ini hadir untuk menggantikan proses manual dengan solusi digital yang terintegrasi — mulai dari pencatatan inventori, proses pengajuan & distribusi laptop, hingga pengambilan keputusan pemilihan laptop berbasis data menggunakan metode **MCDM (Multi Criteria Decision Making)** dengan kombinasi pembobotan **SWARA** dan perankingan **SAW**.

Proyek ini dikembangkan menggunakan pendekatan **Incremental Development** — setiap increment menghasilkan fitur yang siap digunakan dan dapat dievaluasi secara bertahap.

### 🎯 Tujuan Pengembangan

| # | Tujuan |
|---|--------|
| 1 | Mengelola inventori laptop secara terpusat |
| 2 | Mendokumentasikan riwayat penggunaan laptop |
| 3 | Mengelola proses pengajuan, distribusi, dan pengembalian laptop |
| 4 | Membantu pemilihan laptop berdasarkan kebutuhan pengguna |
| 5 | Menyediakan dashboard monitoring inventori real-time |
| 6 | Mengintegrasikan seluruh proses bisnis terkait laptop |
| 7 | Menyediakan sistem notifikasi dan manajemen pengguna |

---

## 🚀 Fitur Utama

Pengembangan SILAPTOP79 dibagi menjadi **3 Increment** yang saling berkaitan:

<details>
<summary><b>🔵 Increment 1 – Manajemen Inventori Laptop</b></summary>

<br/>

**🔐 Authentication & Authorization**
- Login & Logout pengguna berbasis Django Session & Custom Auth Backend
- Role Based Access Control (RBAC) berdasarkan Role (Talent, HC, IT, Admin)

**📦 Manajemen Inventori Laptop**
- Tambah, ubah, dan hapus data laptop
- Detail informasi laptop
- Monitoring status, kondisi, dan lokasi laptop

**📋 Pengajuan & Distribusi Laptop**
- Pengajuan laptop oleh Talent
- Validasi pengajuan oleh Human Capital (HC)
- Distribusi dan pengembalian laptop
- Riwayat penggunaan laptop

**📊 Dashboard**
- Statistik inventori & peminjaman
- Monitoring aset laptop
- Ringkasan aktivitas terkini

</details>

<details>
<summary><b>🟢 Increment 2 – Decision Support System (DSS)</b></summary>

<br/>

**🖥️ Manajemen Spesifikasi Laptop**
- Integrasi detail spesifikasi laptop pada inventori

**⚖️ Manajemen Kriteria**
- Kustomisasi parameter kriteria untuk penilaian laptop

**📐 Manajemen Bobot Kriteria (SWARA)**
- Penentuan dan perhitungan bobot kriteria menggunakan metode Step-wise Weight Assessment Ratio Analysis (SWARA)
- Penyimpanan hasil bobot kriteria

**🏆 Rekomendasi Laptop (SAW)**
- Normalisasi alternatif laptop
- Perhitungan nilai preferensi menggunakan metode Simple Additive Weighting (SAW)
- Perankingan dan rekomendasi laptop otomatis berdasarkan kebutuhan pengguna

**📈 Dashboard DSS**
- Visualisasi ranking laptop
- Hasil dan monitoring perhitungan DSS

</details>

<details>
<summary><b>🟡 Increment 3 – Integrasi & Deployment</b></summary>

<br/>

**👤 User Management**
- Kelola, tambah, ubah, dan nonaktifkan pengguna
- Reset password, kelola role pengguna

**🔔 Notification Service**
- Notifikasi status pengajuan laptop di dashboard
- Alert info notifikasi real-time jika pengajuan disetujui, ditolak, atau didistribusikan

**📋 Audit Log & Monitoring**
- Riwayat log aktivitas peminjaman dan pengembalian
- Riwayat perubahan data laptop dan status inventori

**🔗 Integrasi Sistem**
- Integrasi antarmuka Django Template dengan alur data database PostgreSQL

</details>

---

## 👥 Role Pengguna

| Role | Deskripsi | Akses Utama |
|------|-----------|-------------|
| 🛡️ **Administrator** | Mengelola seluruh sistem (melalui Django Admin) | Semua modul & Manajemen User |
| 💻 **IT Infrastructure** | Mengelola inventori & DSS | Manajemen Laptop, Kriteria, Bobot SWARA, Hasil SAW |
| 🏢 **Human Capital (HC)** | Memvalidasi pengajuan laptop | Validasi Pengajuan, Distribusi Laptop, Pengembalian |
| 👨‍💼 **Talent** | Mengajukan kebutuhan laptop | Pengajuan Laptop, Riwayat Peminjaman |

---

## 🛠️ Teknologi yang Digunakan

<table>
  <tr>
    <th>Layer</th>
    <th>Teknologi</th>
  </tr>
  <tr>
    <td>🖼️ <b>Frontend / Presentation</b></td>
    <td>Django Templates · Vanilla HTML5 · Vanilla CSS3 · JavaScript (Vanilla)</td>
  </tr>
  <tr>
    <td>⚙️ <b>Backend Framework</b></td>
    <td>Python · Django Web Framework</td>
  </tr>
  <tr>
    <td>🗄️ <b>Database</b></td>
    <td>PostgreSQL 16+</td>
  </tr>
  <tr>
    <td>🔐 <b>Authentication</b></td>
    <td>Django Session & Custom Authentication Backend (`InventoriAuthBackend`)</td>
  </tr>
  <tr>
    <td>🔄 <b>Version Control</b></td>
    <td>Git · GitHub</td>
  </tr>
</table>

---

## 📦 Prasyarat Instalasi

Pastikan perangkat Anda telah menginstal software berikut:

| Software | Versi Minimum |
|----------|:-------------:|
| ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white) | **3.11+** |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?logo=postgresql&logoColor=white) | **16+** |
| ![Git](https://img.shields.io/badge/Git-Latest-F05032?logo=git&logoColor=white) | **Terbaru** |

---

## 📂 Struktur Proyek

```
silaptop79/
│
├── ⚙️ silaptop79/          # Django project configuration (settings, urls, wsgi)
│
├── 📦 core/                # Modul inti (middleware, custom auth backend, helper)
├── ⚖️ dss/                 # Modul Decision Support System (SWARA & SAW)
├── 💻 inventori/           # Modul Inventori Laptop & Peminjaman (models, views)
├── 👥 users/               # Modul manajemen pengguna & custom user
│
├── 📂 templates/           # Berkas Django HTML Templates (Base, IT, HC, Talent)
├── 📂 static/              # Aset statis (CSS, JS, Images)
│
├── 📂 seeders/             # Script seeder untuk inisialisasi database
├── 🧪 tests/               # Berkas pengujian unit & integration test
│
├── manage.py               # Django CLI management script
├── requirement.txt         # Daftar dependencies Python
├── README.md
└── .gitignore
```

---

## ⚙️ Instalasi

### 1️⃣ Clone Repository

```bash
git clone https://github.com/username/silaptop79.git
cd silaptop79
```

### 2️⃣ Setup Database PostgreSQL

```sql
CREATE DATABASE silaptop79;
```

### 3️⃣ Setup Environment & Install Dependencies

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirement.txt
```

**Linux / macOS:**

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

### 4️⃣ Konfigurasi `.env` (Optional/Django Settings)

Sesuaikan konfigurasi database Anda pada `silaptop79/settings.py` atau pastikan kredensial database lokal telah sesuai dengan konfigurasi database PostgreSQL Anda.

### 5️⃣ Jalankan Migrasi Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Seed Data Awal (Optional)

Gunakan scripts seeder untuk mengisi data awal (user dummy, role, kriteria, laptop):

```bash
python manage.py loaddata seeders/seed_data.json
# Atau menggunakan python script seeder jika tersedia
```

### 7️⃣ Jalankan Server Development Django

```bash
python manage.py runserver
```

Buka peramban (browser) dan akses:
🔗 **http://localhost:8000**

---

## 🧪 Testing

Untuk menjalankan pengujian unit test dan verifikasi fungsionalitas CRUD:

```bash
python manage.py test
```

Atau jalankan file test spesifik secara manual:

```bash
python test_it_crud.py
python test_hc_crud.py
python test_talent_crud.py
```

---

## 📊 Alur DSS

Berikut adalah alur kerja Decision Support System pada SILAPTOP79:

```
┌─────────────────────┐
│    Input Kriteria   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Perhitungan SWARA  │  ← Penentuan bobot kriteria
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Bobot Kriteria    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Normalisasi SAW    │  ← Simple Additive Weighting
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Perankingan Laptop  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Rekomendasi Laptop  │ ✅
└─────────────────────┘
```

---

## 🛣️ Roadmap Pengembangan

- [x] **Increment 1** – Manajemen Inventori Laptop
  - [x] Session-based Authentication & Authorization
  - [x] CRUD Inventori Laptop (IT & HC view)
  - [x] Pengajuan & Peminjaman Laptop oleh Talent
  - [x] Dashboard Monitoring

- [x] **Increment 2** – Decision Support System (DSS)
  - [x] Manajemen Kriteria & Parameter Penilaian
  - [x] Integrasi Pembobotan SWARA
  - [x] Perhitungan dan Perankingan Rekomendasi SAW
  - [x] Dashboard Hasil Rekomendasi

- [x] **Increment 3** – Integrasi & Deployment
  - [x] User Management & Custom Authentication Backend
  - [x] Log Audit & Riwayat Peminjaman
  - [x] Toast & Banner Notification pada aksi sukses/gagal CRUD
  - [x] Integration Testing & UAT

---

## 👨‍💻 Tim Pengembang

<div align="center">

**KoTA 302**

| Nama | NIM |
|------|-----|
| Alqan Nazra | 231511068 |
| Muhammad Daffa Tridya Atha | 231511082 |
| Yulina Anggraeni | 231511096 |

<br/>

🎓 **Program Studi D3 Teknik Informatika**  
🏛️ Jurusan Teknik Komputer dan Informatika  
🏫 **Politeknik Negeri Bandung**

</div>

---

## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan **Tugas Akhir Program Diploma 3 Teknik Informatika** Politeknik Negeri Bandung. Seluruh hak cipta dimiliki oleh tim pengembang.

---

<div align="center">

Made with ❤️ by **KoTA 302** — Politeknik Negeri Bandung © 2024

</div>
