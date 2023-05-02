from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, FormView
)

from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin

from .forms import CreateRideForm, UpdateRideForm
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


class RidesDetailView(DetailView): # SingleObjectMixin,FormView):
    model = Ride
    # context_object_name = 'ride'
    # fields = []

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        leader = self.get_object().leader
        participants = self.get_object().participants
        user = self.request.user
        buttons_value = 'None'
        if leader == user:
            buttons_value = 'update_delete'
        elif participants.filter(pk=user.pk).exists():
            buttons_value = 'remove_participation'
        else:
            buttons_value = 'signup'
        context["buttons"] = buttons_value
        return context

    def post(self, request, *args, **kwargs):
        # Get the current pk from the method dictionary
        pk = kwargs.get('pk')

        if request.method == 'POST':
            # # Get the current object
            obj = self.model.objects.get(id=pk)
            # Alter the field Value
            action = request.POST.get('action')
            if action == 'signup':
                pobj = self.get_object().participants
                user = self.request.user
                pobj.add(user)
            elif action == 'remove_participation':
                pobj = self.get_object().participants
                user = self.request.user
                pobj.remove(user)


            # obj.field = some_value
            # # Save the object
            # obj.save()

            # Redirect to you current View after update
            return redirect('ride-detail', pk=pk)
            # reverse('rides')
    #
    # def form_valid(self, form):
    #     review = form.instance
    #     review.user = self.request.user
    #     review.expert = self.object
    #     form.save()
    #     return super().form_valid(form)

class RidesCreateView(LoginRequiredMixin, CreateView):
    model = Ride
    # fields = ['route', 'ride_date', 'start_time', 'additional_details']
    form_class = CreateRideForm

    def form_valid(self, form):
        form.instance.leader = self.request.user
        return super().form_valid(form)


class RidesUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    # fields = ['route', 'ride_date', 'start_time', 'additional_details', 'leader']
    form_class = UpdateRideForm

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



