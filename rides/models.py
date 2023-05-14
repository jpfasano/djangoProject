from datetime import datetime

from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from routes.models import Route


class Ride(models.Model):
    leader = models.ForeignKey(User, blank=False, null=True, on_delete=models.SET_NULL)
    route = models.ForeignKey(Route, blank=False, null=True, on_delete=models.SET_NULL)
    additional_details = RichTextField(blank=True, null=True)
    ride_date = models.DateField()
    start_time = models.TimeField()
    participants = models.ManyToManyField(User, related_name='ride_participants')
    # ride_report_text = RichTextUploadingField(blank=False, null=False)
    ride_report_text = RichTextField(blank=False, null=False)

    # Route also a foreign key.
    # Date
    #

    def __str__(self):
        rn = ''
        ld = ''
        rd = ''
        if self.route is not None:
            rn = self.route.route_name
        if self.leader is not None:
            ld = self.leader
        if self.ride_date is not None:
            rd = str(self.ride_date)
        ret_val = ''
        ret_val += rn
        ret_val += ' on ' + rd
        ret_val += ' lead by ' + ld.first_name + " " + ld.last_name
        return ret_val

    def get_absolute_url(self):
        return reverse('ride-detail', kwargs={'pk': self.pk})

    @property
    def event_status(self):
        status = None

        present = datetime.now()
        ride_occurred = (present >= self.ride_date)

        if ride_occurred:
            status = 'Finished'
        else:
            status = 'Ongoing'

        return status

    class Meta:
        ordering = ['-ride_date']
