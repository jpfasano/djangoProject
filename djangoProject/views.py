from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    # return HttpResponse('<h1>Website Homepage</h1>')
    return render(request,'home.html', {'title': 'ADKEzRiders'})


