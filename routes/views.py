from django.shortcuts import render
from .models import Route

def routes(request):
    context = {
        'routes': Route.objects.all(),
        'title': 'Routes'
    }
    return render(request,'routes/routes.html', context)


def about(request):
    return render(request,'routes/about.html', {'title': 'About Routes'})

def home(request):
    return render(request,'routes/home.html', {'title': 'ADKEzRiders Home Page'})