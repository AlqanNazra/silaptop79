from django.urls import path
<<<<<<< HEAD

app_name = 'dss'

urlpatterns = [
    # TODO: Daftarkan endpoint API/View untuk DSS di sini
    # path('api/calculate/', views.calculate_spk, name='calculate_spk'),
]
=======
from .views import testing_swara

urlpatterns = [
    path('', testing_swara),  # ini untuk root
    path('api/testing-swara/', testing_swara),
]
>>>>>>> origin/dev-alqan
