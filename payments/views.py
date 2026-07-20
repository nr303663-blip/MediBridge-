from django.shortcuts import render


def placeholder(request):
    """
    Temporary placeholder view for the payments app.
    Will be replaced with real views during the relevant build phase.
    """
    return render(request, 'placeholder.html', {'module': 'payments'})
