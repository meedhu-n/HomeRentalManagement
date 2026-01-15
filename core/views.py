from django.shortcuts import render

def index(request):
    """
    Renders the public landing page (Home).
    """
    return render(request, 'core/index.html')