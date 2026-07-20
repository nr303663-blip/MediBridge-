from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/<int:doctor_id>/', views.book_appointment, name='book_appointment'),
    path('mine/', views.my_appointments, name='my_appointments'),
    path('mine/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('doctor/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/<int:appointment_id>/approve/', views.approve_appointment_view, name='approve_appointment'),
    path('doctor/<int:appointment_id>/decline/', views.decline_appointment_view, name='decline_appointment'),
]
