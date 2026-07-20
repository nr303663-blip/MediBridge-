from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class PatientSignUpForm(UserCreationForm):
    """Signup form for patients — creates a User(role='patient') + a linked Patient profile."""
    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@example.com',
            'autofocus': True,
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'})
    )
    first_name = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    phone_number = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number (optional)'})
    )
    age = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=120,
        widget=forms.NumberInput(attrs={'placeholder': 'Age'})
    )
    gender = forms.ChoiceField(
        required=False,
        choices=[('', '-- Select --'), ('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'phone_number', 'age', 'gender', 'password1', 'password2'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = User.Role.PATIENT
        user.phone_number = self.cleaned_data.get('phone_number', '')
        if commit:
            user.save()
        return user


class DoctorSignUpForm(UserCreationForm):
    """
    Signup form for doctors — creates a User(role='doctor') + a linked Doctor
    profile with approval_status='pending' (Approval Module, Section 2).
    A pending doctor cannot log in and receive bookings until an admin
    approves them.
    """
    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'placeholder': 'email@example.com',
            'autofocus': True,
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'})
    )
    first_name = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'})
    )
    phone_number = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number (optional)'})
    )
    qualification = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Qualification'}),
    )
    experience_years = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'placeholder': 'Years of experience'})
    )

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email',
            'phone_number', 'password1', 'password2'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = User.Role.DOCTOR
        user.phone_number = self.cleaned_data.get('phone_number', '')
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    """
    Login form. Roadmap's User table keys on email, but Django's auth
    system natively works with `username`; USERNAME_FIELD='email' on our
    custom User model handles that mapping, so this form just relabels
    the field for the template.
    """
    username = forms.CharField(label="Email", widget=forms.TextInput(attrs={'autofocus': True}))
