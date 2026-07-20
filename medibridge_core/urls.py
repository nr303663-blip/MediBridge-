"""
MediBridge URL Configuration.
Wires up every module from the roadmap (Section 2: Core Modules).
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core site pages (home, about, departments, etc. - Hospital Info Module)
    path('', include('hospital.urls')),

    # Authentication Module
    path('accounts/', include('accounts.urls')),

    # Doctor Module
    path('doctors/', include('doctors.urls')),

    # Patient dashboard
    path('patients/', include('patients.urls')),

    # Appointment + Approval + Notification Modules
    path('appointments/', include('appointments.urls')),

    # Payment Module
    path('payments/', include('payments.urls')),

    # ML-Based Self Diagnostic Module
    path('diagnostics/', include('diagnostics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
