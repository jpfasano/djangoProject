from datetime import date

from django.contrib import messages
from django.http import HttpResponseRedirect
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
from django_filters.views import FilterView

from .filters import RideFilter

from .forms import CreateRideForm, UpdateRideForm, UpdateRideReportForm
from .models import Ride
from django.contrib.auth.models import User


def about(request):
    return render(request, 'rides/about.html', {'title': 'About Routes'})


def home(request):
    return render(request, 'rides/home.html', {'title': 'ADKEzRiders Home Page'})


class ScheduledRides(ListView):
    model = Ride
    template_name = 'rides/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'rides'
    ordering = ['ride_date']  # Newest to oldest

    # filterset_class = RideFilter
    # paginate_by = 5

    def get_queryset(self):
        today = date.today()
        queryset = super().get_queryset()
        queryset = queryset.filter(ride_date__gte=today)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RideFilter(self.request.GET, queryset=self.get_queryset())
        return context


class CompletedRides(ListView):
    model = Ride
    template_name = 'rides/completed_rides.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'rides'
    ordering = ['-ride_date']  # Newest to oldest
    # filterset_class = RideFilter
    paginate_by = 5

    def get_queryset(self):
        today = date.today()
        queryset = super().get_queryset()
        queryset = queryset.filter(ride_date__lte=today)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RideFilter(self.request.GET, queryset=self.get_queryset())
        return context


class RidesListView(FilterView):
    model = Ride
    template_name = 'rides/rides.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'rides'
    ordering = ['-ride_date']  # Newest to oldest
    filterset_class = RideFilter
    paginate_by = 5

    # def get_queryset(self):
    #     today = date.today()
    #     queryset = super().get_queryset()
    #     queryset = queryset.filter(ride_date__gte=today)
    #     return queryset

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['filter'] = RideFilter(self.request.GET, queryset=self.get_queryset() )
    #     return context


class UserRidesListView(ListView):
    model = Ride
    template_name = 'rides/user_rides.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'rides'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Ride.objects.filter(leader=user)
        # return Ride.objects.filter(leader=user).order_by('-date_posted')


class RidesDetailView(LoginRequiredMixin, DetailView):  # SingleObjectMixin,FormView):
    model = Ride

    # context_object_name = 'ride'
    # fields = []

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        leader = self.get_object().leader
        participants = self.get_object().participants
        buttons_value = 'None'
        if self.request.user.is_authenticated:
            user = self.request.user
            buttons_value = ''
            today = date.today()
            ride_date = self.get_object().ride_date

            # Check for buttons available pre-ride
            if today <= ride_date:
                if leader == user:
                    buttons_value = 'update_delete'
                elif participants.filter(pk=user.pk).exists():
                    buttons_value = 'remove_participation'
                else:
                    buttons_value = 'signup'

            # Check for buttons available post-ride
            if today >= ride_date:
                context['ride_report'] = True
                # Did user participate in the ride?
                if participants.filter(pk=user.pk).exists():
                    # User participated so can create trip report
                    buttons_value += ' update_trip_report'

        context["buttons"] = buttons_value

        # # Is there a ride report?
        # ride_report_text = self.get_object().ride_report_text
        # if ride_report_text.strip() != '':
        #     context['ride_report'] = True

        return context

    def post(self, request, *args, **kwargs):
        # Get the current pk from the method dictionary
        pk = kwargs.get('pk')

        if request.method == 'POST':
            # # Get the current object
            obj = self.model.objects.get(id=pk)
            ride_as_string = str(obj)
            # Alter the field Value
            action = request.POST.get('action')
            if action == 'signup':
                pobj = self.get_object().participants
                user = self.request.user
                pobj.add(user)
                messages.success(request, f'You are signed up for {ride_as_string}')
            elif action == 'remove_participation':
                pobj = self.get_object().participants
                user = self.request.user
                pobj.remove(user)
                messages.success(request, f'You are no longer signed up for {ride_as_string}')
            elif action == 'update_trip_report':
                return redirect('ride-report-update', pk=pk)

            # obj.field = some_value
            # # Save the object
            # obj.save()

        # Redirect to you current View after update
        return redirect('ride-detail', pk=pk)
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
        # Current signed in user is the ride leader and a ride participant
        form.save()
        form.instance.leader = self.request.user
        form.instance.participants.add(self.request.user)
        return super().form_valid(form)


class RidesReportUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ride
    template_name = 'rides/report_update.html'
    # fields = ['route', 'ride_date', 'start_time', 'additional_details', 'leader']
    form_class = UpdateRideReportForm

    # def form_valid(self, form):
    #     form.instance.leader = self.request.user
    #     return super().form_valid(form)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['create'] = True
    #     return context

    # Check to make sure user is allowed to create the ride report.
    # Only the ride participants are allowed to create.
    def test_func(self):
        ride = self.get_object()
        if self.request.user in ride.participants.all():
            # if ride.participants.filter(pk=self.request.user).exists():
            return True
        else:
            return False

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        if form.has_changed():
            success_message = None
            # Do something to update database
            if self.request.POST['action'] == 'update':
                success_message = 'Ride report updated.'
            elif self.request.POST['action'] == 'update_and_email':
                for changed in form.changed_data:
                    print(changed)
                participants = self.get_object().participants.all()
                for p in participants:
                    print("Ride report updated. Send email to inform " + p.email)
                success_message = 'Ride report updated'
                if len(participants) > 0:
                    success_message += ' and email sent to sign-up list'
            if success_message is not None:
                messages.success(self.request, success_message)
        else:
            messages.warning(self.request, 'No changes detected. Ride report not updated')
            pass
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

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # form.send_email()
        if form.has_changed():
            success_message = None
            if self.request.POST['action'] == 'update':
                success_message = 'Ride data has been updated.'
            elif self.request.POST['action'] == 'update_and_email':
                for changed in form.changed_data:
                    print(changed)
                participants = self.get_object().participants.all()
                for p in participants:
                    print("Ride updated. Send email to inform " + p.email)
                success_message = 'Ride updated'
                if len(participants) > 0:
                    success_message += ' and email sent to sign-up list'
            if success_message is not None:
                messages.success(self.request, success_message)
        else:
            messages.warning(self.request, 'No changes detected. Ride not updated')
        return super().form_valid(form)


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
        return reverse('home')

    def form_valid(self, form):
        action = self.request.POST['action']
        if action == 'delete':
            participants = self.get_object().participants.all()
            for p in participants:
                print("Ride canceled. Send email to inform " + p.email)

            pk = self.kwargs.get('pk')
            obj = self.model.objects.get(id=pk)
            ride_as_string = str(obj)
            messages.success(self.request, "The ride '" + ride_as_string + "' has been canceled")
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     # Get the current pk from the method dictionary
    #     pk = kwargs.get('pk')
    #     obj = self.model.objects.get(id=pk)
    #     ride_as_string = str(obj)
    #
    #     if request.method == 'POST':
    #
    #         action = request.POST.get('action')
    #         if action == 'delete':
    #             for p in self.get_object().participants.all():
    #                 print("Ride canceled. Send email to inform " + p.email)
    #
    #             # Redirect to all rides view after delete
    #             Ride.objects.get(id=pk).delete()
    #             messages.success(request, f'"{ride_as_string}" deleted and signed-up users notified.')
    #     return redirect('rides')
    #     # reverse('rides')
