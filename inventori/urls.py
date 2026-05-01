from django.urls import path

app_name = 'inventori'

from . import views

urlpatterns = [
    # Processor API
    path('api/processor/', views.processor_list_create, name='processor_list_create'),
    path('api/processor/<int:id_processor>/', views.processor_detail, name='processor_detail'),
    
    # Laptop Inventori API
    path('api/laptop/', views.laptop_list_create, name='laptop_list_create'),
    path('api/laptop/<str:id_laptop>/', views.laptop_detail, name='laptop_detail'),
]
