from django.shortcuts import render
from django.http import HttpResponse

# ==========================================
# 1. HUMAN CAPITAL (HC) VIEWS
# ==========================================

def dashboard_hc_view(request):
    return render(request, 'hc/dashboard/dashboard_hc.html')

def manajemenlaptop_hc_view(request):
    return render(request, 'hc/inventori/manajemenlaptop_hc.html')

def pengajuanlaptop_hc_view(request):
    return render(request, 'hc/inventori/pengajuanlaptop_hc.html')

def detailpengajuan_hc_view(request):
    return render(request, 'hc/inventori/detailpengajuan_hc.html')

def tambahlaptop_hc_view(request):
    return render(request, 'hc/inventori/tambahlaptop_hc.html')

def detaillaptop_hc_view(request):
    return render(request, 'hc/inventori/detaillaptop_hc.html')

def riwayatpeminjamanlaptop_hc_view(request):
    return render(request, 'hc/inventori/riwayatpeminjamanlaptop_hc.html')

def editdatalaptop_hc_view(request):
    return render(request, 'hc/inventori/editdatalaptop_hc.html')

def inputkriteria_hc_view(request):
    return render(request, 'hc/dss/inputkriteria_hc.html')

def hasilrekomendasi_hc_view(request):
    return render(request, 'hc/dss/hasilrekomendasi_hc.html')

def detailrekomendasi_hc_view(request):
    return render(request, 'hc/dss/detailrekomendasi_hc.html')

def detailrekomendasiscrapping_hc_view(request):
    return render(request, 'hc/dss/detailrekomendasiscrapping_hc.html')


# ==========================================
# 2. INFORMATION TECHNOLOGY (IT) VIEWS (START FROM SCRATCH)
# ==========================================

def dashboard_it_view(request):
    return HttpResponse("<h3>IT Dashboard - Mulai dari Awal</h3><p>Silakan buat file template Anda di <code>templates/it/dashboard/dashboard_it.html</code></p>")

def manajemenlaptop_it_view(request):
    return HttpResponse("<h3>IT Manajemen Laptop - Mulai dari Awal</h3>")

def pengajuanlaptop_it_view(request):
    return HttpResponse("<h3>IT Pengajuan Laptop - Mulai dari Awal</h3>")

def detailpengajuan_it_view(request):
    return HttpResponse("<h3>IT Detail Pengajuan - Mulai dari Awal</h3>")

def tambahlaptop_it_view(request):
    return HttpResponse("<h3>IT Tambah Laptop - Mulai dari Awal</h3>")

def detaillaptop_it_view(request):
    return HttpResponse("<h3>IT Detail Laptop - Mulai dari Awal</h3>")

def riwayatpeminjamanlaptop_it_view(request):
    return HttpResponse("<h3>IT Riwayat Peminjaman - Mulai dari Awal</h3>")

def editdatalaptop_it_view(request):
    return HttpResponse("<h3>IT Edit Laptop - Mulai dari Awal</h3>")

def inputkriteria_it_view(request):
    return HttpResponse("<h3>IT Input Kriteria - Mulai dari Awal</h3>")

def hasilrekomendasi_it_view(request):
    return HttpResponse("<h3>IT Hasil Rekomendasi - Mulai dari Awal</h3>")

def detailrekomendasi_it_view(request):
    return HttpResponse("<h3>IT Detail Rekomendasi - Mulai dari Awal</h3>")

def detailrekomendasiscrapping_it_view(request):
    return HttpResponse("<h3>IT Detail Scraping - Mulai dari Awal</h3>")


# ==========================================
# 3. TALENT VIEWS
# ==========================================

def dashboard_talent_view(request):
    return render(request, 'talent/dashboard/dashboard_talent.html')

def pengajuanlaptop_talent_view(request):
    return render(request, 'talent/inventori/pengajuanlaptop_talent.html')

def riwayatpeminjamanlaptop_talent_view(request):
    return render(request, 'talent/inventori/riwayatpeminjamanlaptop_talent.html')

def pengembalianlaptop_talent_view(request):
    return render(request, 'talent/inventori/pengembalianlaptop_talent.html')

def detaillaptop_talent_view(request):
    return render(request, 'talent/inventori/detaillaptop_talent.html')

# --- Stub views (belum ada template, akan dikembangkan nanti) ---
def manajemenlaptop_talent_view(request):
    return HttpResponse("<h3>Talent Manajemen Laptop - Coming Soon</h3>")

def detailpengajuan_talent_view(request):
    return HttpResponse("<h3>Talent Detail Pengajuan - Coming Soon</h3>")

def tambahlaptop_talent_view(request):
    return HttpResponse("<h3>Talent Tambah Laptop - Coming Soon</h3>")

def editdatalaptop_talent_view(request):
    return HttpResponse("<h3>Talent Edit Laptop - Coming Soon</h3>")

def inputkriteria_talent_view(request):
    return HttpResponse("<h3>Talent Input Kriteria - Coming Soon</h3>")

def hasilrekomendasi_talent_view(request):
    return HttpResponse("<h3>Talent Hasil Rekomendasi - Coming Soon</h3>")

def detailrekomendasi_talent_view(request):
    return HttpResponse("<h3>Talent Detail Rekomendasi - Coming Soon</h3>")

def detailrekomendasiscrapping_talent_view(request):
    return HttpResponse("<h3>Talent Detail Scraping - Coming Soon</h3>")
