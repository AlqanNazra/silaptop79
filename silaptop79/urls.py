from django.contrib import admin
from django.urls import path, include
from core.views import (
    dashboard_hc_view, 
    manajemenlaptop_hc_view, 
    pengajuanlaptop_hc_view, 
    detailpengajuan_hc_view,
    tambahlaptop_hc_view, 
    inputkriteria_hc_view, 
    hasilrekomendasi_hc_view, 
    detaillaptop_hc_view, 
    riwayatpeminjamanlaptop_hc_view, 
    editdatalaptop_hc_view,
    detailrekomendasi_hc_view,
    detailrekomendasiscrapping_hc_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dss/', include('dss.urls')),
    path('inventori/', include('inventori.urls')),

    path('', dashboard_hc_view, name='dashboardhc'),
    
    path('manajemen-laptop/', manajemenlaptop_hc_view, name='manajemen_laptop'),

    path('pengajuan-laptop/', pengajuanlaptop_hc_view, name='pengajuanlaptop_hc'),
    path('detail-pengajuan/', detailpengajuan_hc_view, name='detailpengajuan_hc'),
    path('tambah-laptop/', tambahlaptop_hc_view, name='tambahlaptop_hc'),
    path('detail-laptop/', detaillaptop_hc_view, name='detaillaptop_hc'),
    path('riwayat-peminjaman/', riwayatpeminjamanlaptop_hc_view, name='riwayatpeminjamanlaptop_hc'),
    path('edit-laptop/', editdatalaptop_hc_view, name='editdatalaptop_hc'),

    path('input-kriteria/', inputkriteria_hc_view, name='inputkriteria_hc'),
    path('hasil-rekomendasi/', hasilrekomendasi_hc_view, name='hasilrekomendasi_hc'),
    path('detail-rekomendasi/', detailrekomendasi_hc_view, name='detailrekomendasi_hc'),
    path('detail-scrapping/', detailrekomendasiscrapping_hc_view, name='detailrekomendasiscrapping_hc'),
]