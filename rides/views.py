from django.shortcuts import render
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

from .forms import CreateRideForm
from .models import Ride
from django.contrib.auth.models import User


class RidesListView(ListView):
    model = Ride
    template_name = 'rides/rides.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'rides'
    # ordering = ['-date_posted']  # Newest to oldest
    paginate_by = 5


class UserRidesListView(ListView):
    model = Ride
    template_name = 'rides/user_rides.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'rides'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Ride.objects.filter(leader=user)
        # return Ride.objects.filter(leader=user).order_by('-date_posted')


class RidesDetailView(DetailView):
    model = Ride
    context_object_name = 'ride'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context["display_more"] = False
    #     context['jptest'] = 'jpfest'
    #     return context


class RidesCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    # fields = ['route', 'ride_date', 'start_time', 'additional_details']
    form_class = CreateRideForm

    def form_valid(self, form):
        form.instance.leader = self.request.user
        return super().form_valid(form)


class RidesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    fields = ['route', 'ride_date', 'start_time', 'additional_details', 'leader']

    # form_class = RideCreateUpdateForm

    # def form_valid(self, form):
    #     form.instance.leader = self.request.user
    #     return super().form_valid(form)

    # Check to make sure user is allowed to update the ride.
    # Only the ride's leader is allowed to update.
    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.leader:
            return True
        else:
            return False



class RidesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ride

    # success_url = '/'
    # Check to make sure user is allowed to delete the ride.
    # Only the ride's leader is allowed to delete.
    def test_func(self):
        ride = self.get_object()
        if self.request.user == ride.leader:
            return True
        else:
            return False

    def get_success_url(self):
        return reverse('rides')



