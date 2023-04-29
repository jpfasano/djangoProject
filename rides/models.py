from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from routes.models import Route


class Ride(models.Model):
    leader = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    route = models.ForeignKey(Route, blank=True, null=True, on_delete=models.SET_NULL)
    additional_details = RichTextField(blank=True, null=True)
    ride_date = models.DateField()
    start_time = models.TimeField()
    # Route also a foreign key.
    # Date
    #

    def __str__(self):
        return self.route.route_name

    def get_absolute_url(self):
        return reverse('ride-detail', kwargs={'pk':self.pk})