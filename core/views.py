from django.shortcuts import render

def dashboard_hc_view(request):
    return render(request, 'dashboard/dashboard_hc.html')

def manajemenlaptop_hc_view(request):
    return render(request, 'inventori/manajemenlaptop_hc.html')

def pengajuanlaptop_hc_view(request):
    return render(request, 'inventori/pengajuanlaptop_hc.html')

def detailpengajuan_hc_view(request):
    return render(request, 'inventori/detailpengajuan_hc.html')

def tambahlaptop_hc_view(request):
    return render(request, 'inventori/tambahlaptop_hc.html')

def detaillaptop_hc_view(request):
    return render(request, 'inventori/detaillaptop_hc.html')

def riwayatpeminjamanlaptop_hc_view(request):
    return render(request, 'inventori/riwayatpeminjamanlaptop_hc.html')

def editdatalaptop_hc_view(request):
    return render(request, 'inventori/editdatalaptop_hc.html')

def inputkriteria_hc_view(request):
    return render(request, 'dss/inputkriteria_hc.html')

def hasilrekomendasi_hc_view(request):
    return render(request, 'dss/hasilrekomendasi_hc.html')

def detailrekomendasi_hc_view(request):
    return render(request, 'dss/detailrekomendasi_hc.html')

def detailrekomendasiscrapping_hc_view(request):
    return render(request, 'dss/detailrekomendasiscrapping_hc.html')