from django.urls import path
from .views import testing_swara

app_name = 'dss'

urlpatterns = [
    path('', testing_swara, name='testing_swara'),
    path('api/testing-swara/', testing_swara, name='api_testing_swara'),
]
