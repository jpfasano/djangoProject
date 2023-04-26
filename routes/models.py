from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Route(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    distance = models.PositiveSmallIntegerField()
    start_location = models.TextField()
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
