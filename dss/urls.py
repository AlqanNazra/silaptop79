from django.urls import path
from .views import testing_swara

urlpatterns = [
    path('', testing_swara),  # ini untuk root
    path('api/testing-swara/', testing_swara),
]