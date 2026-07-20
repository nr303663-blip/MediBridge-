from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import transaction

from .forms import PatientSignUpForm, DoctorSignUpForm, EmailAuthenticationForm
from .models import User
from patients.models import Patient
from doctors.models import Doctor


def signup_choice(request):
    """Landing page: 'Sign up as a Patient' vs 'Sign up as a Doctor'."""
    return render(request, 'accounts/signup_choice.html')


@transaction.atomic
def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Patient.objects.create(
                user=user,
                age=form.cleaned_data.get('age'),
                gender=form.cleaned_data.get('gender', ''),
                contact_number=form.cleaned_data.get('phone_number', ''),
            )
            login(request, user)
            messages.success(request, "Welcome to MediBridge! Your account has been created.")
            return redirect('patients:patients_home')
    else:
        form = PatientSignUpForm()
    return render(request, 'accounts/patient_signup.html', {'form': form})


@transaction.atomic
def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Doctor.objects.create(
                user=user,
                qualification=form.cleaned_data.get('qualification', ''),
                experience_years=form.cleaned_data.get('experience_years') or 0,
                approval_status=Doctor.ApprovalStatus.PENDING,
            )
            login(request, user)
            messages.info(
                request,
                "Your doctor account was created and is pending admin approval. "
                "You'll be notified once approved."
            )
            return redirect('accounts:accounts_home')
    else:
        form = DoctorSignUpForm()
    return render(request, 'accounts/doctor_signup.html', {'form': form})


class MediBridgeLoginView(LoginView):
    """
    Single login page for all roles (patient/doctor/admin). After
    authenticating, the user is redirected to their role-specific
    dashboard by `dashboard_redirect` below.
    """
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:dashboard_redirect')


def logout_view(request):
    logout(request)
    messages.info(request, "You've been logged out.")
    return redirect('hospital:hospital_home')


def dashboard_redirect(request):
    """
    Central role router used right after login. Sends:
      patient -> patient dashboard
      doctor  -> doctor dashboard
      admin   -> Django admin panel (Admin Module dashboard, Section 2)
    """
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.role == User.Role.PATIENT:
        return redirect('patients:patients_home')
    if request.user.role == User.Role.DOCTOR:
        return redirect('doctors:doctors_home')
    if request.user.role == User.Role.ADMIN:
        return redirect('/admin/')

    return redirect('hospital:hospital_home')


def placeholder(request):
    return render(request, 'placeholder.html', {'module': 'accounts'})
