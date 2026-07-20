from functools import wraps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*roles):
    """
    Restrict a view to users whose `role` is in `roles`.
    Usage: @role_required('doctor')  or  @role_required('doctor', 'admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            if request.user.role not in roles:
                raise PermissionDenied("You don't have access to this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def approved_doctor_required(view_func):
    """
    Restrict a view to doctors whose Doctor.approval_status == 'approved'
    (Approval Module, Section 2). Pending/declined doctors are redirected
    back with a message instead of reaching the dashboard.
    """
    @wraps(view_func)
    @role_required('doctor')
    def _wrapped(request, *args, **kwargs):
        doctor_profile = getattr(request.user, 'doctor_profile', None)
        if not doctor_profile or not doctor_profile.is_approved:
            messages.warning(
                request,
                "Your doctor account is still pending admin approval. "
                "You'll be notified once it's approved."
            )
            return redirect('accounts:accounts_home')
        return view_func(request, *args, **kwargs)
    return _wrapped
