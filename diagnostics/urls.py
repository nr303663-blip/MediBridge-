from django.urls import path
from . import views

app_name = 'diagnostics'

urlpatterns = [
    path('', views.select_symptoms, name='diagnostics_home'),
    path('result/<int:diagnosis_id>/', views.result, name='result'),
    path('history/', views.history, name='history'),
]
