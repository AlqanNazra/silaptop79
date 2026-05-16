from django.contrib import admin
from django.urls import path, include
from core.views import home_view, dashboard_hc_view, inputkriteria_hc_view, hasilrekomendasi_hc_view,pengajuanlaptop_hc_view
from inventori.views import laptop_dashboard,tambahlaptop_hc_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dss/', include('dss.urls')),
    path('inventori/', include('inventori.urls')),
    path('', home_view, name='home'),
    path('dashboardhc/', dashboard_hc_view, name='dashboardhc'), # Ini Dashboard baru
    path('pengajuanlaptop_hc/', pengajuanlaptop_hc_view, name='pengajuanlaptop_hc'),
    path('tambahlaptop_hc/', tambahlaptop_hc_view, name='tambahlaptop_hc'),
    path('inputkriteria_hc/', inputkriteria_hc_view, name='inputkriteria_hc'),
    path('hasilrekomendasi_hc/', hasilrekomendasi_hc_view, name='hasilrekomendasi_hc'),
    path("laptop/", laptop_dashboard, name="laptop_dashboard"),
]
