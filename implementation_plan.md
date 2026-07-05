# Ekstrak Inline CSS ke File Eksternal

Memindahkan semua `<style>` block dari 54 file HTML template ke file CSS terpisah, sehingga setiap template hanya me-load CSS dari file eksternal.

## Scope

- **54 file HTML** dengan total ~15,000 baris CSS inline
- **3 role group**: `hc/`, `it/`, `talent/` + `auth/`, `users/`, `components/`
- Banyak CSS yang **duplikat** antar file (layout, sidebar override, page header, form card, tabel, status badge, dll)

## Proposed Changes

### Struktur CSS Baru

```
static/css/
├── style.css              ← Global (sudah ada - sidebar, navbar, pagination, dll)
├── layout.css             ← [NEW] Layout shared (body, dashboard-wrapper, main-content)
├── components.css         ← [NEW] Shared components (form-card, page-header, btn, badge, table, modal, dll)
├── pages/
│   ├── dashboard.css      ← [NEW] Dashboard pages (hc, it, talent)
│   ├── pengajuan.css      ← [NEW] Pengajuan laptop pages
│   ├── manajemen.css      ← [NEW] Manajemen laptop/proyek/role pages
│   ├── detail.css         ← [NEW] Detail pages (laptop, pengajuan, pengadaan)
│   ├── dss.css            ← [NEW] DSS pages (inputkriteria, hasilrekomendasi)
│   ├── form.css           ← [NEW] Form pages (tambah, edit)
│   ├── auth.css           ← [NEW] Login page
│   └── profile.css        ← [NEW] Profile page
```

> [!IMPORTANT]
> **Pendekatan**: CSS yang **identik/hampir identik** di banyak file akan di-merge ke satu file bersama. CSS yang **unik** untuk satu halaman akan ditaruh di file page-specific. Tujuannya: **zero inline CSS** di semua HTML template.

### Fase Eksekusi

#### Fase 1: Shared Layout & Components
Ekstrak class-class yang muncul di hampir semua page:
- `body`, `.dashboard-wrapper`, `.main-dashboard-content`, `.main-content`
- `.sidebar` overrides
- `.page-header`, `.page-top`
- `.form-card`, `.form-group`, `.form-control`
- `.status-badge`, `.badge-*`
- `.btn-back`, `.btn-submit`, `.btn-*`
- Table styles (`.data-table`, row hover, etc)
- Modal styles (`.modal-overlay`, `.modal-box`)
- Animations (`@keyframes`, transitions)

**File**: `layout.css` + `components.css`

#### Fase 2: Page-Specific CSS
Group per page type:
- **Dashboard** (3 files): `dashboard_hc`, `dashboard_it`, `dashboard_talent`
- **Pengajuan** (3 files): `pengajuanlaptop_hc/it/talent`
- **Manajemen** (7 files): `manajemenlaptop`, `manajemenpengadaan`, `manajemenproyek`, `manajemenroleteknologi`, `manajemenuser`
- **Detail** (8 files): `detaillaptop`, `detailpengajuan`, `detailpengadaan`, `detailrekomendasi`
- **DSS** (6 files): `inputkriteria`, `hasilrekomendasi`, `tambahspek`, `detailrekomendasiscrapping`
- **Form** (10 files): `tambahlaptop`, `tambahproyek`, `tambahrole`, `tambahpengadaan`, `editdatalaptop`, `editproyek`, `editrole`, `editpengadaan`
- **Lainnya**: `riwayatpeminjaman`, `setujuipengajuan`, `notifikasi`, `pengembalianlaptop`

#### Fase 3: Update Templates
- Hapus `<style>...</style>` dari setiap HTML
- Tambahkan `<link rel="stylesheet" href="{% static 'css/layout.css' %}">` dll di `<head>`
- Pastikan urutan load CSS benar: `style.css` → `layout.css` → `components.css` → page-specific

## Open Questions

> [!IMPORTANT]
> 1. **Inline `style=""` attributes**: Banyak template juga menggunakan inline `style=""` langsung di elemen HTML (bukan `<style>` block). Apakah mau sekalian dipindah juga? Ini akan menambah scope signifikan.
> 2. **Apakah boleh saya merge CSS yang sangat mirip tapi sedikit beda value** (misal `padding: 40px 60px` vs `padding: 48px 60px`)? Saya akan normalisasi ke satu value.
> 3. **Prioritas**: Mau dikerjakan semua sekaligus, atau mau per-batch (misal Fase 1 dulu, test, lalu lanjut)?

## Verification Plan

### Manual Verification
- Buka setiap halaman di browser setelah migration dan pastikan tampilan identik
- Check semua halaman: dashboard, pengajuan, manajemen, detail, DSS, form, auth, profile
