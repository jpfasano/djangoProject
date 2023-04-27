from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Route(models.Model):
    route_name = models.CharField(max_length=100)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    distance = models.PositiveSmallIntegerField()
    start_location = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.route_name

    def get_absolute_url(self):
        return reverse('route-detail', kwargs={'pk':self.pk})
