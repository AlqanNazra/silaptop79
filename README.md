<div align="center">

# 💻 SILAPTOP79

### Sistem Informasi Laptop Padepokan 79

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14+-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://typescriptlang.org)

<br/>

> Aplikasi web terpadu untuk manajemen inventori laptop, pengelolaan peminjaman/distribusi perangkat, dan sistem pengambilan keputusan berbasis MCDM di lingkungan PT Padepokan Tujuh Sembilan.

<br/>

[🚀 Mulai Cepat](#%EF%B8%8F-instalasi) · [📖 Fitur](#-fitur-utama) · [🧑‍💻 Teknologi](#%EF%B8%8F-teknologi-yang-digunakan) · [📊 Alur DSS](#-alur-dss) · [👥 Tim](#-tim-pengembang)

</div>

---

## 📖 Tentang Proyek

**SILAPTOP79** adalah aplikasi manajemen aset laptop berbasis web yang dikembangkan untuk PT Padepokan Tujuh Sembilan. Sistem ini hadir untuk menggantikan proses manual dengan solusi digital yang terintegrasi — mulai dari pencatatan inventori, proses pengajuan & distribusi laptop, hingga pengambilan keputusan berbasis data menggunakan metode **MCDM (Multi Criteria Decision Making)**.

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
- Login & Logout pengguna
- Role Based Access Control (RBAC)

**📦 Manajemen Inventori Laptop**
- Tambah, ubah, dan hapus data laptop
- Detail informasi laptop
- Monitoring status, kondisi, dan lokasi laptop

**📋 Pengajuan & Distribusi Laptop**
- Pengajuan laptop oleh Talent
- Validasi pengajuan oleh Human Capital
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
- Tambah, ubah, dan hapus spesifikasi laptop

**⚖️ Manajemen Kriteria**
- Tambah, ubah, dan hapus kriteria penilaian

**📐 Manajemen Bobot Kriteria (SWARA)**
- Penentuan dan perhitungan bobot kriteria
- Penyimpanan hasil bobot SWARA

**🏆 Rekomendasi Laptop (SAW)**
- Normalisasi alternatif laptop
- Perhitungan nilai preferensi
- Perankingan dan rekomendasi laptop

**📈 Dashboard DSS**
- Visualisasi ranking laptop
- Hasil dan monitoring perhitungan DSS

</details>

<details>
<summary><b>🟡 Increment 3 – Integrasi & Deployment</b></summary>

<br/>

**👤 User Management**
- Kelola, tambah, ubah, dan nonaktifkan pengguna
- Aktivasi pengguna, reset password, kelola role

**🔔 Notification Service**
- Notifikasi pengajuan, persetujuan, dan penolakan laptop
- Notifikasi distribusi, pengembalian, dan perubahan status
- Notifikasi hasil rekomendasi DSS

**📋 Audit Log & Monitoring**
- Riwayat login, aktivitas, dan perubahan data pengguna
- Riwayat pengajuan, distribusi, dan proses DSS

**🔗 Integrasi Sistem**
- Integrasi modul Inventori, DSS, Pengajuan, User Management, dan Notification

**🚀 Deployment**
- Konfigurasi environment produksi
- UAT (User Acceptance Testing) & Integration Testing
- Monitoring aplikasi

</details>

---

## 👥 Role Pengguna

| Role | Deskripsi | Akses Utama |
|------|-----------|-------------|
| 🛡️ **Administrator** | Mengelola seluruh sistem | Semua modul |
| 💻 **IT Infrastructure** | Mengelola inventori & DSS | Inventori, Spesifikasi, Kriteria, DSS |
| 🏢 **Human Capital (HC)** | Memvalidasi pengajuan laptop | Validasi, Distribusi |
| 👨‍💼 **Talent** | Mengajukan kebutuhan laptop | Pengajuan Laptop |

---

## 🛠️ Teknologi yang Digunakan

<table>
  <tr>
    <th>Layer</th>
    <th>Teknologi</th>
  </tr>
  <tr>
    <td>🖼️ <b>Frontend</b></td>
    <td>Next.js · React.js · TypeScript · Tailwind CSS · Shadcn UI</td>
  </tr>
  <tr>
    <td>⚙️ <b>Backend</b></td>
    <td>Python · FastAPI</td>
  </tr>
  <tr>
    <td>🗄️ <b>Database</b></td>
    <td>PostgreSQL 16+</td>
  </tr>
  <tr>
    <td>🔐 <b>Authentication</b></td>
    <td>JWT Authentication</td>
  </tr>
  <tr>
    <td>📄 <b>API Docs</b></td>
    <td>Swagger / OpenAPI</td>
  </tr>
  <tr>
    <td>🔄 <b>Version Control</b></td>
    <td>Git · GitHub</td>
  </tr>
</table>

---

## 📦 Prasyarat Instalasi

Pastikan perangkat Anda telah menginstal semua software berikut:

| Software | Versi Minimum |
|----------|:-------------:|
| ![Node.js](https://img.shields.io/badge/Node.js-20+-339933?logo=nodedotjs&logoColor=white) | **20+** |
| ![npm](https://img.shields.io/badge/npm-10+-CB3837?logo=npm&logoColor=white) | **10+** |
| ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white) | **3.11+** |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?logo=postgresql&logoColor=white) | **16+** |
| ![Git](https://img.shields.io/badge/Git-Latest-F05032?logo=git&logoColor=white) | **Terbaru** |

---

## 📂 Struktur Proyek

```
silaptop79/
│
├── 🖼️  frontend/
│   ├── src/
│   │   ├── app/              # Halaman & routing (App Router)
│   │   ├── components/       # Komponen UI reusable
│   │   ├── hooks/            # Custom React hooks
│   │   ├── services/         # API service layer
│   │   ├── lib/              # Utility & helper functions
│   │   └── types/            # TypeScript type definitions
│   │
│   ├── public/               # Static assets
│   └── package.json
│
├── ⚙️  backend/
│   ├── app/
│   │   ├── api/              # Endpoint API (routers)
│   │   ├── models/           # Model database (ORM)
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── repositories/     # Database access layer
│   │   ├── services/
│   │   │   ├── auth/         # Autentikasi & otorisasi
│   │   │   ├── inventory/    # Manajemen inventori
│   │   │   ├── submission/   # Pengajuan laptop
│   │   │   ├── dss/          # Decision Support System
│   │   │   ├── notification/ # Layanan notifikasi
│   │   │   └── user_management/
│   │   │
│   │   ├── core/             # Konfigurasi inti aplikasi
│   │   └── main.py           # Entry point FastAPI
│   │
│   ├── migrations/           # Alembic migrations
│   ├── requirements.txt
│   └── .env
│
├── 📚 docs/
│   ├── SRS/                  # Software Requirements Specification
│   ├── SDD/                  # Software Design Document
│   ├── UML/                  # Diagram UML
│   ├── Testing/              # Dokumen pengujian
│   └── Deployment/           # Panduan deployment
│
├── docker-compose.yml
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

### 3️⃣ Konfigurasi Backend

Masuk ke folder backend:

```bash
cd backend
```

Buat file `.env` dan isi dengan konfigurasi berikut:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/silaptop79
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4️⃣ Install Dependency Backend

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python -m venv venv
source venv/bin/activate
```

Install package:

```bash
pip install -r requirements.txt
```

### 5️⃣ Jalankan Migration

```bash
alembic upgrade head
```

### 6️⃣ Jalankan Backend

```bash
uvicorn app.main:app --reload
```

| Service | URL |
|---------|-----|
| 🔗 Backend API | http://localhost:8000 |
| 📄 Swagger Docs | http://localhost:8000/docs |

### 7️⃣ Setup Frontend

```bash
cd frontend
npm install
```

Buat file `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Jalankan aplikasi:

```bash
npm run dev
```

| Service | URL |
|---------|-----|
| 🖼️ Frontend | http://localhost:3000 |

---

## 🧪 Testing

**Backend:**

```bash
pytest
```

**Frontend:**

```bash
npm run test
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
  - [x] Authentication & Authorization
  - [x] CRUD Inventori Laptop
  - [x] Pengajuan & Distribusi Laptop
  - [x] Dashboard Monitoring

- [x] **Increment 2** – Decision Support System
  - [x] Manajemen Kriteria & Spesifikasi
  - [x] Perhitungan Bobot (SWARA)
  - [x] Rekomendasi Laptop (SAW)
  - [x] Dashboard DSS

- [x] **Increment 3** – Integrasi & Deployment
  - [x] User Management
  - [x] Notification Service
  - [x] Audit Log & Monitoring
  - [x] Integration Testing & UAT
  - [x] Deployment

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
