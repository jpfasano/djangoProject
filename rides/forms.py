from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.utils import ErrorList



from routes.models import Route
from .models import Ride


class DateInput(forms.DateInput):
    input_type = 'date'
class TimeInput(forms.TimeInput):
    input_type = 'time'


class CreateRideForm(ModelForm):


    # leader = forms.ModelChoiceField(queryset=User.objects.all)
    route = forms.ModelChoiceField(queryset=Route.objects.all())
    additional_details = forms.CharField(widget=CKEditorWidget())
    ride_date = forms.DateField(widget=DateInput())
    start_time = forms.TimeField(widget=TimeInput())

    class Meta:
        model = Ride
        fields = ['route', 'ride_date', 'start_time', 'additional_details']
        # widgets = {'ride_date': DateInput(), 'start_time': TimeInput()}
