from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.signup_choice, name='accounts_home'),
    path('signup/', views.signup_choice, name='signup_choice'),
    path('signup/patient/', views.patient_signup, name='patient_signup'),
    path('signup/doctor/', views.doctor_signup, name='doctor_signup'),
    path('login/', views.MediBridgeLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard-redirect/', views.dashboard_redirect, name='dashboard_redirect'),
]
