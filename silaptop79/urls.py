from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import home_view, dashboard_hc_view, tambahlaptop_hc_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dss/', include('dss.urls')),
    path('inventori/', include('inventori.urls')),
    path('', home_view, name='home'),
    path('dashboardhc/', dashboard_hc_view, name='dashboardhc'), # Ini Dashboard baru
    path('tambahlaptop_hc/', tambahlaptop_hc_view, name='tambahlaptop_hc'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
