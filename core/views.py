from django.shortcuts import render

def home_view(request):
    return render(request, 'inventori/manajemenlaptop_hc.html')

def dashboard_hc_view(request):
    return render(request, 'dashboard/dashboard_hc.html')

def pengajuanlaptop_hc_view(request):
    return render(request, 'inventori/pengajuanlaptop_hc.html')

def tambahlaptop_hc_view(request):
    return render(request, 'inventori/tambahlaptop_hc.html')

def inputkriteria_hc_view(request):
    return render(request, 'dss/inputkriteria_hc.html')

def hasilrekomendasi_hc_view(request):
    return render(request, 'dss/hasilrekomendasi_hc.html')

