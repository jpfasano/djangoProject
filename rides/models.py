from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Ride(models.Model):
    leader = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    additional_details = RichTextField(blank=True, null=True)
    # Route also a foreign key.
    # Date
    #

    def __str__(self):
        return self.additional_details

    def get_absolute_url(self):
        return reverse('ride-detail', kwargs={'pk':self.pk})