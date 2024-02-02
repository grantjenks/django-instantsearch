from django.shortcuts import render


def index(request):
    """
    View function for the index page.
    """
    return render(request, 'index.html')
