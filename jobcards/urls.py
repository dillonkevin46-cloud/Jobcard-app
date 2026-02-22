from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('jobcards/', views.jobcard_list, name='jobcard_list'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('builder/', views.template_builder, name='template_builder'),
]
