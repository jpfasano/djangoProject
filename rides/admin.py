from django.contrib import admin
from .models import Ride, Picture


class PictureInLine(admin.TabularInline):
    model = Picture


class RideAdmin(admin.ModelAdmin):
    inlines = [PictureInLine]


admin.site.register(Ride, RideAdmin)
