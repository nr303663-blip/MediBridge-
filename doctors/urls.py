from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_dashboard, name='doctors_home'),
    path('search/', views.doctor_search, name='doctor_search'),
    path('<int:doctor_id>/', views.doctor_detail, name='doctor_detail'),
]
