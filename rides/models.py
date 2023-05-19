import os
from datetime import datetime
# from io import BytesIO

from ckeditor.fields import RichTextField
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string
from PIL import Image

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


# ----------------------------------

def get_up_load_path(instance, filename):
    pass
    path = 'pictures/'
    ride_date = instance.ride.ride_date.strftime('%Y-%m-%d')
    path += ride_date + '/'
    path += filename
    upload_path = path
    while default_storage.exists(upload_path):
        last_dot_index = upload_path.rfind('.')
        pre_extension = upload_path[:last_dot_index]
        extension = upload_path[last_dot_index:]
        random_string = get_random_string(length=4)
        upload_path = pre_extension + '_' + random_string + extension
    return upload_path


class Picture(models.Model):
    picture = models.ImageField(upload_to=get_up_load_path)
    # picture = models.ImageField(upload_to='pictures/')
    caption = models.CharField(max_length=512)
    ride = models.ForeignKey('Ride',on_delete=models.CASCADE,related_name='report_pictures')

    # blog_entry = BlogEntry.objects.get(pk=1)  # Assuming you have a specific BlogEntry instance
    # # Retrieve all associated pictures for the given BlogEntry
    # associated_pictures = blog_entry.report_pictures.all()

    def delete(self, *args, **kwargs):
        # Delete the picture file from the media directory
        if self.picture:
            default_storage.delete(self.picture.name)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs) # Open the image file
        img = Image.open(self.picture.path)

        # if format isn't jpg, then save to change to be jpg
        save_picture = img.format != 'JPEG'

        max_dim = 512
        if img.height > max_dim or img.width > max_dim:
            # Resize the image
            max_size = (max_dim, max_dim)
            img.thumbnail(max_size)
            save_picture = True

            # Save the resized image, overwriting the original file
        if save_picture:
            img.save(self.picture.path, format='JPEG', quality=75)

