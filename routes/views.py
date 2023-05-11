from ckeditor.widgets import CKEditorWidget
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import Route
from django.contrib.auth.models import User
from django import forms


def routes(request):
    context = {
        'routes': Route.objects.all(),
        'route_name': 'Routes'
    }
    return render(request, 'routes/routes.html', context)


class RoutesListView(ListView):
    model = Route
    template_name = 'routes/routes.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'routes'
    ordering = ['-date_posted']  # Newest to oldest
    paginate_by = 5


class UserRoutesListView(ListView):
    model = Route
    template_name = 'routes/user_routes.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'routes'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Route.objects.filter(author=user).order_by('-date_posted')


class RoutesDetailView(DetailView):
    model = Route


class RoutesCreateView(LoginRequiredMixin, CreateView):
    model = Route
    fields = ['route_name', 'description', 'distance', 'start_location']
    # form_class = RouteCreateUpdateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RoutesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Route
    fields = ['route_name', 'description', 'distance', 'start_location']

    # form_class = RouteCreateUpdateForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # Check to make sure user is allowed to update the route.
    # Only the route's author is allowed to update.
    def test_func(self):
        route = self.get_object()
        if self.request.user == route.author:
            return True
        else:
            return False


class RoutesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Route

    # success_url = '/'
    # Check to make sure user is allowed to delete the route.
    # Only the route's author is allowed to delete.
    def test_func(self):
        route = self.get_object()
        if self.request.user == route.author:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('routes')

