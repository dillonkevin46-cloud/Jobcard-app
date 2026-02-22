from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path('create/', views.client_create, name='client_create'),
    path('edit/<int:pk>/', views.client_edit, name='client_edit'),
    path('delete/<int:pk>/', views.client_delete, name='client_delete'),
]
