from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import (
    # HC Views
    dashboard_hc_view, 
    manajemenlaptop_hc_view, 
    pengajuanlaptop_hc_view, 
    detailpengajuan_hc_view,
    setujui_pengajuan_hc_view,
    tambahlaptop_hc_view, 
    inputkriteria_hc_view, 
    hasilrekomendasi_hc_view, 
    detaillaptop_hc_view, 
    riwayatpeminjamanlaptop_hc_view, 
    editdatalaptop_hc_view,
    editriwayatpeminjamanlaptop_hc_view,
    detailrekomendasi_hc_view,
    detailrekomendasiscrapping_hc_view,
    notifikasi_hc_view,

    # IT Views
    dashboard_it_view,
    manajemenlaptop_it_view,
    pengajuanlaptop_it_view,
    detailpengajuan_it_view,
    setujui_pengajuan_it_view,
    tambahlaptop_it_view,
    tambahspek_it_view,
    inputkriteria_it_view,
    hasilrekomendasi_it_view,
    detaillaptop_it_view,
    riwayatpeminjamanlaptop_it_view,
    editdatalaptop_it_view,
    detailrekomendasi_it_view,
    detailrekomendasiscrapping_it_view,
    notifikasi_it_view,
    manajemenpengadaan_it_view,
    detailpengadaan_it_view,
    editpengadaan_it_view,
    manajemenproyek_it_view,
    tambahproyek_it_view,
    editproyek_it_view,
    hapusproyek_it_view,

    # Talent Views
    # Talent Views
    dashboard_talent_view,
    pengajuanlaptop_talent_view,
    detaillaptop_talent_view,
    riwayatpeminjamanlaptop_talent_view,
    pengembalianlaptop_talent_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dss/', include('dss.urls')),
    path('inventori/', include('inventori.urls')),
    
    # Authentication (login sementara dinonaktifkan)
    # path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Landing Page (Directly to HC Dashboard as requested)
    path('', dashboard_hc_view, name='index'),

    # ==========================================
    # HUMAN CAPITAL (HC) ROUTES
    # ==========================================
    path('hc/', dashboard_hc_view, name='dashboardhc'),
    path('hc/manajemen-laptop/', manajemenlaptop_hc_view, name='manajemen_laptop'),
    path('hc/pengajuan-laptop/', pengajuanlaptop_hc_view, name='pengajuanlaptop_hc'),
    path('hc/detail-pengajuan/', detailpengajuan_hc_view, name='detailpengajuan_hc'),
    path('hc/setujui-pengajuan/', setujui_pengajuan_hc_view, name='setujui_pengajuan_hc'),
    path('hc/tambah-laptop/', tambahlaptop_hc_view, name='tambahlaptop_hc'),
    path('hc/detail-laptop/', detaillaptop_hc_view, name='detaillaptop_hc'),
    path('hc/riwayat-peminjaman/', riwayatpeminjamanlaptop_hc_view, name='riwayatpeminjamanlaptop_hc'),
    path('hc/edit-laptop/', editdatalaptop_hc_view, name='editdatalaptop_hc'),
    path('hc/edit-riwayat-peminjaman/', editriwayatpeminjamanlaptop_hc_view, name='editriwayatpeminjaman_hc'),
    path('hc/input-kriteria/', inputkriteria_hc_view, name='inputkriteria_hc'),
    path('hc/hasil-rekomendasi/', hasilrekomendasi_hc_view, name='hasilrekomendasi_hc'),
    path('hc/detail-rekomendasi/', detailrekomendasi_hc_view, name='detailrekomendasi_hc'),
    path('hc/detail-scrapping/', detailrekomendasiscrapping_hc_view, name='detailrekomendasiscrapping_hc'),
    path('hc/notifikasi/', notifikasi_hc_view, name='notifikasi_hc'),

    # ==========================================
    # INFORMATION TECHNOLOGY (IT) ROUTES
    # ==========================================
    path('it/', dashboard_it_view, name='dashboard_it'),
    path('it/manajemen-laptop/', manajemenlaptop_it_view, name='manajemen_laptop_it'),
    path('it/pengajuan-laptop/', pengajuanlaptop_it_view, name='pengajuanlaptop_it'),
    path('it/detail-pengajuan/', detailpengajuan_it_view, name='detailpengajuan_it'),
    path('it/setujui-pengajuan/', setujui_pengajuan_it_view, name='setujui_pengajuan_it'),
    path('it/tambah-laptop/', tambahlaptop_it_view, name='tambahlaptop_it'),
    path('it/dss/tambah-spek/', tambahspek_it_view, name='tambahspek_it'),
    path('it/detail-laptop/', detaillaptop_it_view, name='detaillaptop_it'),
    path('it/riwayat-peminjaman/', riwayatpeminjamanlaptop_it_view, name='riwayatpeminjamanlaptop_it'),
    path('it/edit-laptop/', editdatalaptop_it_view, name='editdatalaptop_it'),
    path('it/input-kriteria/', inputkriteria_it_view, name='inputkriteria_it'),
    path('it/hasil-rekomendasi/', hasilrekomendasi_it_view, name='hasilrekomendasi_it'),
    path('it/detail-rekomendasi/', detailrekomendasi_it_view, name='detailrekomendasi_it'),
    path('it/detail-scrapping/', detailrekomendasiscrapping_it_view, name='detailrekomendasiscrapping_it'),
    path('it/notifikasi/', notifikasi_it_view, name='notifikasi_it'),
    path('it/manajemen-pengadaan/', manajemenpengadaan_it_view, name='manajemen_pengadaan_it'),
    path('it/detail-pengadaan/', detailpengadaan_it_view, name='detailpengadaan_it'),
    path('it/edit-pengadaan/', editpengadaan_it_view, name='editpengadaan_it'),
    path('it/manajemen-proyek/', manajemenproyek_it_view, name='manajemen_proyek_it'),
    path('it/tambah-proyek/', tambahproyek_it_view, name='tambahproyek_it'),
    path('it/edit-proyek/<str:id_proyek>/', editproyek_it_view, name='editproyek_it'),
    path('it/hapus-proyek/<str:id_proyek>/', hapusproyek_it_view, name='hapusproyek_it'),

    # ==========================================
    # TALENT ROUTES
    # ==========================================
    path('talent/', dashboard_talent_view, name='dashboard_talent'),
    path('talent/pengajuan-laptop/', pengajuanlaptop_talent_view, name='pengajuanlaptop_talent'),
    path('talent/detail-laptop/', detaillaptop_talent_view, name='detaillaptop_talent'),
    path('talent/riwayat-peminjaman/', riwayatpeminjamanlaptop_talent_view, name='riwayatpeminjamanlaptop_talent'),
    path('talent/pengembalian/', pengembalianlaptop_talent_view, name='pengembalianlaptop_talent'),
]
