from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
<<<<<<< HEAD
from django.contrib.auth import views as auth_views
from core.views import home_view, dashboard_hc_view, tambahlaptop_hc_view
=======
=======
from django.views.generic import TemplateView
>>>>>>> origin/dev-lina
from core.views import (
    # HC Views
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
    detailrekomendasiscrapping_hc_view,

    # IT Views
    dashboard_it_view,
    manajemenlaptop_it_view,
    pengajuanlaptop_it_view,
    detailpengajuan_it_view,
    tambahlaptop_it_view,
    inputkriteria_it_view,
    hasilrekomendasi_it_view,
    detaillaptop_it_view,
    riwayatpeminjamanlaptop_it_view,
    editdatalaptop_it_view,
    detailrekomendasi_it_view,
    detailrekomendasiscrapping_it_view,

    # Talent Views
    dashboard_talent_view,
    manajemenlaptop_talent_view,
    pengajuanlaptop_talent_view,
    detailpengajuan_talent_view,
    tambahlaptop_talent_view,
    inputkriteria_talent_view,
    hasilrekomendasi_talent_view,
    detaillaptop_talent_view,
    riwayatpeminjamanlaptop_talent_view,
    pengembalianlaptop_talent_view,
    editdatalaptop_talent_view,
    detailrekomendasi_talent_view,
    detailrekomendasiscrapping_talent_view,
)
>>>>>>> origin/dev-lina

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dss/', include('dss.urls')),
    path('inventori/', include('inventori.urls')),
<<<<<<< HEAD
    path('', home_view, name='home'),
    path('dashboardhc/', dashboard_hc_view, name='dashboardhc'), # Ini Dashboard baru
    path('tambahlaptop_hc/', tambahlaptop_hc_view, name='tambahlaptop_hc'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
=======

    # Landing Page (Directly to HC Dashboard as requested)
    path('', dashboard_hc_view, name='index'),

    # ==========================================
    # HUMAN CAPITAL (HC) ROUTES
    # ==========================================
    path('hc/', dashboard_hc_view, name='dashboardhc'),
    path('hc/manajemen-laptop/', manajemenlaptop_hc_view, name='manajemen_laptop'),
    path('hc/pengajuan-laptop/', pengajuanlaptop_hc_view, name='pengajuanlaptop_hc'),
    path('hc/detail-pengajuan/', detailpengajuan_hc_view, name='detailpengajuan_hc'),
    path('hc/tambah-laptop/', tambahlaptop_hc_view, name='tambahlaptop_hc'),
    path('hc/detail-laptop/', detaillaptop_hc_view, name='detaillaptop_hc'),
    path('hc/riwayat-peminjaman/', riwayatpeminjamanlaptop_hc_view, name='riwayatpeminjamanlaptop_hc'),
    path('hc/edit-laptop/', editdatalaptop_hc_view, name='editdatalaptop_hc'),
    path('hc/input-kriteria/', inputkriteria_hc_view, name='inputkriteria_hc'),
    path('hc/hasil-rekomendasi/', hasilrekomendasi_hc_view, name='hasilrekomendasi_hc'),
    path('hc/detail-rekomendasi/', detailrekomendasi_hc_view, name='detailrekomendasi_hc'),
    path('hc/detail-scrapping/', detailrekomendasiscrapping_hc_view, name='detailrekomendasiscrapping_hc'),

<<<<<<< HEAD
    path('input-kriteria/', inputkriteria_hc_view, name='inputkriteria_hc'),
    path('hasil-rekomendasi/', hasilrekomendasi_hc_view, name='hasilrekomendasi_hc'),
    path('detail-rekomendasi/', detailrekomendasi_hc_view, name='detailrekomendasi_hc'),
    path('detail-scrapping/', detailrekomendasiscrapping_hc_view, name='detailrekomendasiscrapping_hc'),
]
>>>>>>> origin/dev-lina
=======
    # ==========================================
    # INFORMATION TECHNOLOGY (IT) ROUTES
    # ==========================================
    path('it/', dashboard_it_view, name='dashboard_it'),
    path('it/manajemen-laptop/', manajemenlaptop_it_view, name='manajemen_laptop_it'),
    path('it/pengajuan-laptop/', pengajuanlaptop_it_view, name='pengajuanlaptop_it'),
    path('it/detail-pengajuan/', detailpengajuan_it_view, name='detailpengajuan_it'),
    path('it/tambah-laptop/', tambahlaptop_it_view, name='tambahlaptop_it'),
    path('it/detail-laptop/', detaillaptop_it_view, name='detaillaptop_it'),
    path('it/riwayat-peminjaman/', riwayatpeminjamanlaptop_it_view, name='riwayatpeminjamanlaptop_it'),
    path('it/edit-laptop/', editdatalaptop_it_view, name='editdatalaptop_it'),
    path('it/input-kriteria/', inputkriteria_it_view, name='inputkriteria_it'),
    path('it/hasil-rekomendasi/', hasilrekomendasi_it_view, name='hasilrekomendasi_it'),
    path('it/detail-rekomendasi/', detailrekomendasi_it_view, name='detailrekomendasi_it'),
    path('it/detail-scrapping/', detailrekomendasiscrapping_it_view, name='detailrekomendasiscrapping_it'),

    # ==========================================
    # TALENT ROUTES
    # ==========================================
    path('talent/', dashboard_talent_view, name='dashboard_talent'),
    path('talent/manajemen-laptop/', manajemenlaptop_talent_view, name='manajemen_laptop_talent'),
    path('talent/pengajuan-laptop/', pengajuanlaptop_talent_view, name='pengajuanlaptop_talent'),
    path('talent/detail-pengajuan/', detailpengajuan_talent_view, name='detailpengajuan_talent'),
    path('talent/tambah-laptop/', tambahlaptop_talent_view, name='tambahlaptop_talent'),
    path('talent/detail-laptop/', detaillaptop_talent_view, name='detaillaptop_talent'),
    path('talent/riwayat-peminjaman/', riwayatpeminjamanlaptop_talent_view, name='riwayatpeminjamanlaptop_talent'),
    path('talent/pengembalian/', pengembalianlaptop_talent_view, name='pengembalianlaptop_talent'),
    path('talent/edit-laptop/', editdatalaptop_talent_view, name='editdatalaptop_talent'),
    path('talent/input-kriteria/', inputkriteria_talent_view, name='inputkriteria_talent'),
    path('talent/hasil-rekomendasi/', hasilrekomendasi_talent_view, name='hasilrekomendasi_talent'),
    path('talent/detail-rekomendasi/', detailrekomendasi_talent_view, name='detailrekomendasi_talent'),
    path('talent/detail-scrapping/', detailrekomendasiscrapping_talent_view, name='detailrekomendasiscrapping_talent'),
]
>>>>>>> origin/dev-lina
