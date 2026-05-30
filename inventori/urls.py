from django.urls import path
from . import views

app_name = 'inventori'

urlpatterns = [
    # =========================================================
    # PAGE VIEWS (Render Template HTML)
    # =========================================================
    path('', views.manajemen_laptop_page, name='manajemenlaptop_hc'),
    path('tambah/', views.tambah_laptop_page, name='tambahlaptop_hc'),
    path('detail/<str:id_laptop>/', views.detail_laptop_page, name='detail_laptop'),
    path('pengajuan/', views.pengajuan_page_view, name='pengajuanlaptop_hc'),

    # =========================================================
    # API ENDPOINTS (JSON Response)
    # =========================================================
    # Processor API
    path('api/processor/', views.processor_list_create, name='processor_list_create'),
    path('api/processor/<int:id_processor>/', views.processor_detail, name='processor_detail'),

    # Laptop Inventori API
    path('api/laptop/', views.laptop_list_create, name='laptop_list_create'),
    path('api/laptop/<str:id_laptop>/', views.laptop_detail, name='laptop_detail'),

    # Pengajuan API
    path('api/pengajuan/', views.list_pengajuan_view, name='list_pengajuan'),
    path('api/pengajuan/tambah/', views.tambah_pengajuan_view, name='tambah_pengajuan'),

    # Peminjaman API
    path('api/peminjaman/', views.list_peminjaman_view, name='list_peminjaman'),
    path('api/peminjaman/tambah/', views.tambah_peminjaman_view, name='tambah_peminjaman'),
]
