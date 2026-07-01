from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from core.decorators import hc_required, it_required, talent_required
from core.views import (
    # HC Views
    dashboard_hc_view,
    manajemenlaptop_hc_view,
    edit_role_it_view,
    edit_teknologi_it_view,
    hapus_role_it_view,
    hapus_teknologi_it_view, 
    inputkriteria_hc_view, 
    hasilrekomendasi_hc_view, 
    detailrekomendasi_hc_view,
    detailrekomendasiscrapping_hc_view,
    manajemen_role_teknologi_it_view,
    notifikasi_hc_view,
    konfirmasi_pengembalian_hc_view,
    manajementalent_hc_view,
    manajemenuser_hc_view,
    tambahuser_hc_view,
    edit_user_hc_view,
    hapus_user_hc_view,

    # IT Views
    dashboard_it_view,
    manajemenlaptop_it_view,
    pengajuanlaptop_it_view,
    detailpengajuan_it_view,
    tambah_role_it_view,
    tambah_teknologi_it_view,
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
    konfirmasi_pengembalian_it_view,
    manajemenpengadaan_it_view,
    detailpengadaan_it_view,
    editpengadaan_it_view,
    tambahpengadaan_it_view,
    setujui_pengajuan_it_view,
    tambah_komponen_it_view,
    manajemenproyek_it_view,
    tambahproyek_it_view,
    editproyek_it_view,
    hapusproyek_it_view,

    # Talent Views
    dashboard_talent_view,
    pengajuanlaptop_talent_view,
    detaillaptop_talent_view,
    riwayatpeminjamanlaptop_talent_view,
    konfirmasi_penerimaan_talent_view,
    pengembalianlaptop_talent_view,
    editdatalaptop_talent_view,
    inputkriteria_talent_view,
    hasilrekomendasi_talent_view,
    detailrekomendasi_talent_view,
    detailrekomendasiscrapping_talent_view,

    # Home View
    home_view,
    login_redirect_view,
    logout_view,
    profile_view,
)
from inventori.views import (
    pengajuan_page_view as pengajuanlaptop_hc_view,
    detailpengajuan_hc_view,
    setujui_pengajuan_hc_view,
    assign_laptop_hc_view,
    tambah_laptop_page as tambahlaptop_hc_view,
    detail_laptop_page as detaillaptop_hc_view,
    riwayatpeminjamanlaptop_hc_view,
    editdatalaptop_hc_view,
    laptop_dashboard,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dss/', include('dss.urls')),
    path('inventori/', include('inventori.urls')),
    
    # Authentication (login sementara dinonaktifkan)
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('login-redirect/', login_redirect_view, name='login_redirect'),

    # Landing Page (Redirects directly to Login Page)
    path('', RedirectView.as_view(url='/login/', permanent=False), name='index'),

    # ==========================================
    # HUMAN CAPITAL (HC) ROUTES
    # ==========================================
    path('hc/', hc_required(dashboard_hc_view), name='dashboard_hc'),
    path('hc/manajemen-laptop/', hc_required(manajemenlaptop_hc_view), name='manajemen_laptop_hc'),
    path('hc/pengajuan-laptop/', hc_required(pengajuanlaptop_hc_view), name='pengajuanlaptop_hc'),
    path('hc/detail-pengajuan/', hc_required(detailpengajuan_hc_view), name='detailpengajuan_hc'),
    path('hc/setujui-pengajuan/', hc_required(setujui_pengajuan_hc_view), name='setujui_pengajuan_hc'),
    path('hc/assign-laptop/', hc_required(assign_laptop_hc_view), name='assign_laptop_hc'),
    path('hc/tambah-laptop/', hc_required(tambahlaptop_hc_view), name='tambahlaptop_hc'),
    path('hc/detail-laptop/<str:id_laptop>/', hc_required(detaillaptop_hc_view), name='detaillaptop_hc'),
    path('hc/riwayat-peminjaman/<str:id_laptop>/', hc_required(riwayatpeminjamanlaptop_hc_view), name='riwayatpeminjamanlaptop_hc'),
    path('hc/riwayat-peminjaman/', hc_required(riwayatpeminjamanlaptop_hc_view), name='riwayatpeminjamanlaptop_hc'),
    path('hc/konfirmasi-pengembalian/', hc_required(konfirmasi_pengembalian_hc_view), name='konfirmasi_pengembalian_hc'),
    path('hc/edit-laptop/<str:id_laptop>/', hc_required(editdatalaptop_hc_view), name='editdatalaptop_hc'),
    path('hc/input-kriteria/', hc_required(inputkriteria_hc_view), name='inputkriteria_hc'),
    path('hc/hasil-rekomendasi/', hc_required(hasilrekomendasi_hc_view), name='hasilrekomendasi_hc'),
    path('hc/detail-rekomendasi/', hc_required(detailrekomendasi_hc_view), name='detailrekomendasi_hc'),
    path('hc/detail-scrapping/', hc_required(detailrekomendasiscrapping_hc_view), name='detailrekomendasiscrapping_hc'),
    path('hc/notifikasi/', hc_required(notifikasi_hc_view), name='notifikasi_hc'),
    path('hc/manajemen-talent/', hc_required(manajementalent_hc_view), name='manajementalent_hc'),
    path('hc/manajemen-user/', hc_required(manajemenuser_hc_view), name='manajemenuser_hc'),
    path('hc/tambah-user/', hc_required(tambahuser_hc_view), name='tambahuser_hc'),
    path('hc/edit-user/', hc_required(edit_user_hc_view), name='edit_user_hc'),
    path('hc/hapus-user/', hc_required(hapus_user_hc_view), name='hapus_user_hc'),

    # ==========================================
    # INFORMATION TECHNOLOGY (IT) ROUTES
    # ==========================================
    path('it/', it_required(dashboard_it_view), name='dashboard_it'),
    path('it/manajemen-laptop/', it_required(manajemenlaptop_it_view), name='manajemen_laptop_it'),
    path('it/tambah-komponen/', it_required(tambah_komponen_it_view), name='tambah_komponen_it'),
    path('it/pengajuan-laptop/', it_required(pengajuanlaptop_it_view), name='pengajuanlaptop_it'),
    path('it/detail-pengajuan/', it_required(detailpengajuan_it_view), name='detailpengajuan_it'),
    path('it/tambah-laptop/', it_required(tambahlaptop_it_view), name='tambahlaptop_it'),
    path('it/detail-laptop/<str:id_laptop>/', it_required(detaillaptop_it_view), name='detaillaptop_it'),
    path('it/dss/tambah-spek/', it_required(tambahspek_it_view), name='tambahspek_it'),
    path('it/detail-laptop/', it_required(detaillaptop_it_view), name='detaillaptop_it'),
    path('it/riwayat-peminjaman/<str:id_laptop>/', it_required(riwayatpeminjamanlaptop_it_view), name='riwayatpeminjamanlaptop_it'),
    path('it/riwayat-peminjaman/', it_required(riwayatpeminjamanlaptop_it_view), name='riwayatpeminjamanlaptop_it'),
    path('it/edit-laptop/<str:id_laptop>/', it_required(editdatalaptop_it_view), name='editdatalaptop_it'),
    path('it/input-kriteria/', it_required(inputkriteria_it_view), name='inputkriteria_it'),
    path('it/hasil-rekomendasi/', it_required(hasilrekomendasi_it_view), name='hasilrekomendasi_it'),
    path('it/detail-rekomendasi/', it_required(detailrekomendasi_it_view), name='detailrekomendasi_it'),
    path('it/detail-scrapping/', it_required(detailrekomendasiscrapping_it_view), name='detailrekomendasiscrapping_it'),
    path('it/notifikasi/', it_required(notifikasi_it_view), name='notifikasi_it'),
    path('it/konfirmasi-pengembalian/', it_required(konfirmasi_pengembalian_it_view), name='konfirmasi_pengembalian_it'),
    path('it/manajemen-pengadaan/', it_required(manajemenpengadaan_it_view), name='manajemen_pengadaan_it'),
    path('it/detail-pengadaan/', it_required(detailpengadaan_it_view), name='detailpengadaan_it'),
    path('it/edit-pengadaan/', it_required(editpengadaan_it_view), name='editpengadaan_it'),
    path('it/tambah-pengadaan/', it_required(tambahpengadaan_it_view), name='tambah_pengadaan_it'),
    path('it/setujui-pengajuan/', it_required(setujui_pengajuan_it_view), name='setujui_pengajuan_it'),
    path('it/manajemen-proyek/', it_required(manajemenproyek_it_view), name='manajemen_proyek_it'),
    path('it/tambah-proyek/', it_required(tambahproyek_it_view), name='tambahproyek_it'),
    path('it/edit-proyek/<str:id_proyek>/', it_required(editproyek_it_view), name='editproyek_it'),
    path('it/hapus-proyek/<str:id_proyek>/', it_required(hapusproyek_it_view), name='hapusproyek_it'),

    # ==========================================
    # TALENT ROUTES
    # ==========================================
    path('talent/', talent_required(dashboard_talent_view), name='dashboard_talent'),
    path('talent/pengajuan-laptop/', talent_required(pengajuanlaptop_talent_view), name='pengajuanlaptop_talent'),
    path('talent/detail-laptop/', talent_required(detaillaptop_talent_view), name='detaillaptop_talent'),
    path('talent/riwayat-peminjaman/', talent_required(riwayatpeminjamanlaptop_talent_view), name='riwayatpeminjamanlaptop_talent'),
    path('talent/konfirmasi-penerimaan/', talent_required(konfirmasi_penerimaan_talent_view), name='konfirmasi_penerimaan_talent'),
    path('talent/pengembalian/', talent_required(pengembalianlaptop_talent_view), name='pengembalianlaptop_talent'),
    path('talent/edit-laptop/', talent_required(editdatalaptop_talent_view), name='editdatalaptop_talent'),
    path('talent/input-kriteria/', talent_required(inputkriteria_talent_view), name='inputkriteria_talent'),
    path('talent/hasil-rekomendasi/', talent_required(hasilrekomendasi_talent_view), name='hasilrekomendasi_talent'),
    path('talent/detail-rekomendasi/', talent_required(detailrekomendasi_talent_view), name='detailrekomendasi_talent'),
    path('talent/detail-scrapping/', talent_required(detailrekomendasiscrapping_talent_view), name='detailrekomendasiscrapping_talent'),
    path("laptop/", it_required(laptop_dashboard), name="laptop_dashboard"),
    path('it/manajemen-role-teknologi/', it_required(manajemen_role_teknologi_it_view), name='manajemenroleteknologi_it'),

    path('it/tambah-role/', it_required(tambah_role_it_view), name='tambah_role_it'),
    path('it/edit-role/<str:id_role>/', it_required(edit_role_it_view), name='edit_role_it'),
    path('it/hapus-role/<str:id_role>/', it_required(hapus_role_it_view), name='hapus_role_it'),
    path('it/tambah-teknologi/', it_required(tambah_teknologi_it_view), name='tambah_teknologi_it'),
    path('it/edit-teknologi/<str:id_teknologi>/', it_required(edit_teknologi_it_view), name='edit_teknologi_it'),
    path('it/hapus-teknologi/<str:id_teknologi>/', it_required(hapus_teknologi_it_view), name='hapus_teknologi_it'),

    path('profile/', profile_view, name='profile'),
]
