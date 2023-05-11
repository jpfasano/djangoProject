from datetime import datetime, date, timedelta

from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from routes.models import Route
from .models import Ride


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


def default_ride_date():
    # One week from today
    return datetime.today() + timedelta(days=7)


def default_ride_start_time():
    # ten in the morning
    return default_ride_date().replace(hour=10, minute=00, second=00)


class CreateRideForm(ModelForm):
    # leader = forms.ModelChoiceField(queryset=User.objects.all)
    route = forms.ModelChoiceField(queryset=Route.objects.all())
    additional_details = forms.CharField(widget=CKEditorWidget(), required=False)
    # ride_date = forms.DateField(widget=DateInput(attrs={'width': 200}), initial=default_ride_date)
    # ride_date = forms.DateField(widget=DateInput(), initial=default_ride_date)
    ride_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'min': datetime.now().date()}),
                                initial=default_ride_date)
    start_time = forms.TimeField(widget=TimeInput(), initial=default_ride_start_time)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['start_time'].initial = models.TimeField('10:00am')

    def clean_ride_date(self):
        ride_date = self.cleaned_data['ride_date']
        if ride_date < date.today():
            raise forms.ValidationError("The date cannot be in the past")
        return ride_date

    class Meta:
        model = Ride
        fields = ['route', 'ride_date', 'start_time', 'additional_details']
        # widgets = {'ride_date': DateInput(), 'start_time': TimeInput()}


class CreateRideReportForm(ModelForm):
    ride_report_text = forms.CharField(widget=CKEditorWidget(), required=True)

    def clean_ride_report_text(self):
        # Not sure if this method is really needed.
        ride_report_text = self.cleaned_data['ride_report_text']
        if ride_report_text.strip() == "":
            raise forms.ValidationError("Ride report textual description is required")
        return ride_report_text

    class Meta:
        model = Ride
        fields = ['ride_report_text']
        # widgets = {'ride_date': DateInput(), 'start_time': TimeInput()}


class UpdateRideForm(ModelForm):
    leader = forms.ModelChoiceField(User.objects.all(),
                                    help_text='Caution: If the ride leader is changed, then only the new leader will be able to edit this ride.')
    route = forms.ModelChoiceField(queryset=Route.objects.all())
    additional_details = forms.CharField(widget=CKEditorWidget(), required=False)
    # ride_date = forms.DateField(widget=DateInput(attrs={'width': 200}), initial=default_ride_date)
    ride_date = forms.DateField(widget=DateInput(), initial=default_ride_date)
    start_time = forms.TimeField(widget=TimeInput(), initial=default_ride_start_time)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     self.fields['start_time'].initial = models.TimeField('10:00am')

    def clean_ride_date(self):
        ride_date = self.cleaned_data['ride_date']
        if ride_date < date.today():
            raise forms.ValidationError("The date cannot be in the past")
        return ride_date

    class Meta:
        model = Ride
        fields = ['route', 'ride_date', 'start_time', 'additional_details', 'leader']
        # widgets = {'ride_date': DateInput(), 'start_time': TimeInput()}
