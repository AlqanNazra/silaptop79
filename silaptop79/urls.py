from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
from core.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dss/', include('dss.urls')),
    path('inventori/', include('inventori.urls')),
    path('', home_view, name='home'),
=======
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dss.urls')), 
>>>>>>> origin/dev-alqan
]
