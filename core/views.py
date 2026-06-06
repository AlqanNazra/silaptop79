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

<<<<<<< HEAD
def tambahlaptop_hc_view(request):
    return render(request, 'hc/inventori/tambahlaptop_hc.html')

def detaillaptop_hc_view(request):
    return render(request, 'hc/inventori/detaillaptop_hc.html')

def riwayatpeminjamanlaptop_hc_view(request):
    return render(request, 'hc/inventori/riwayatpeminjamanlaptop_hc.html')

def editdatalaptop_hc_view(request):
    return render(request, 'hc/inventori/editdatalaptop_hc.html')
=======
# def tambahlaptop_hc_view(request):
#     return render(request, 'inventori/tambahlaptop_hc.html')
>>>>>>> origin/dev-alqan

def inputkriteria_hc_view(request):
    return render(request, 'hc/dss/inputkriteria_hc.html')

def hasilrekomendasi_hc_view(request):
    return render(request, 'hc/dss/hasilrekomendasi_hc.html')

def detailrekomendasi_hc_view(request):
    return render(request, 'hc/dss/detailrekomendasi_hc.html')

def detailrekomendasiscrapping_hc_view(request):
    return render(request, 'hc/dss/detailrekomendasiscrapping_hc.html')

def notifikasi_hc_view(request):
    return render(request, 'hc/inventori/notifikasi_hc.html')


# ==========================================
# 2. INFORMATION TECHNOLOGY (IT) VIEWS (START FROM SCRATCH)
# ==========================================

def dashboard_it_view(request):
    return render(request, 'it/dashboard/dashboard_it.html')

def manajemenlaptop_it_view(request):
    return render(request, 'it/inventori/manajemenlaptop_it.html')

def pengajuanlaptop_it_view(request):
    return render(request, 'it/inventori/pengajuanlaptop_it.html')

def detailpengajuan_it_view(request):
    return HttpResponse("<h3>IT Detail Pengajuan - Mulai dari Awal</h3>")

def tambahlaptop_it_view(request):
    return render(request, 'it/inventori/tambahlaptop_it.html')

def detaillaptop_it_view(request):
    return render(request, 'it/inventori/detaillaptop_it.html')

def riwayatpeminjamanlaptop_it_view(request):
    return HttpResponse("<h3>IT Riwayat Peminjaman - Mulai dari Awal</h3>")

def editdatalaptop_it_view(request):
    return HttpResponse("<h3>IT Edit Laptop - Mulai dari Awal</h3>")

def inputkriteria_it_view(request):
    return render(request, 'it/dss/inputkriteria_it.html')

def hasilrekomendasi_it_view(request):
    return render(request, 'it/dss/hasilrekomendasi_it.html')

def detailrekomendasi_it_view(request):
    return HttpResponse("<h3>IT Detail Rekomendasi - Mulai dari Awal</h3>")

def detailrekomendasiscrapping_it_view(request):
    return HttpResponse("<h3>IT Detail Scraping - Mulai dari Awal</h3>")

def notifikasi_it_view(request):
    return render(request, 'it/inventori/notifikasi_it.html')


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


