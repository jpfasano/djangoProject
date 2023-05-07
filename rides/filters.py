from datetime import date

import django_filters
from django.forms import CheckboxSelectMultiple

from .models import Ride


class RideFilter(django_filters.FilterSet):
    RIDE_VIEW_FILTER =(
        ('scheduled', 'Scheduled Rides'),
        ('completed', 'Completed Rides'),
    )
    selection = django_filters.MultipleChoiceFilter(label="Select rides to be displayed", choices=RIDE_VIEW_FILTER,
                                                    method='filter_rides',widget=CheckboxSelectMultiple)
    class Meta:
        model = Ride
        # exclude = '__all__'
        fields = []

    def filter_rides(self, queryset, name, value ):
        today = date.today()
        if 'scheduled' in value and 'completed' in value:
            # Display everything.  Nothing to filter
            pass
        elif 'scheduled' in value:
            # only display those with date >= today
            queryset = queryset.filter(ride_date__gte=today).order_by('ride_date')
        elif 'completed' in value:
            # only display those with date >= today
            queryset = queryset.filter(ride_date__lte=today)
        return queryset
