from django.shortcuts import render

routeList = [
    {
        'author': 'JP Fasano',
        'title': 'Title 1',
        'content': 'Content of first post',
        'date_posted': 'Today',
        'distance': 15,
        'start_location': "Stewart's"
    },
    {
        'author': 'Ken G',
        'title': 'Title 2',
        'content': 'Content of second post',
        'date_posted': 'April 22, 2023',
        'distance': 25,
        'start_location': 'The Hub, Brant Lake'
    }
]

def routes(request):
    context = {
        'routes': routeList,
        'title': 'Routes'
    }
    return render(request,'routes/routes.html', context)


def about(request):
    return render(request,'routes/about.html', {'title': 'About Routes'})

def home(request):
    return render(request,'routes/home.html', {'title': 'ADKEzRiders Home Page'})