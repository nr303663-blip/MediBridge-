from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('', views.home, name='hospital_home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
