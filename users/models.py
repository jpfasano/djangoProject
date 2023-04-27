from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from phonenumber_field.validators import validate_international_phonenumber
import re


# from phonenumber_field.formfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # phone = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{10}$|^\d{3}-\d{3}-\d{4}$')])
    phone = PhoneField(blank=True, E164_only=True, help_text='xxx-xxx-xxxx')

    # def clean(self):
    #     phone_number = self.phone.raw_phone
    #
    #     if re.compile(r'^\d{10}$|^\d{3}-\d{3}-\d{4}$').match(phone_number):
    #         return phone_number
    #     else:
    #         raise ValidationError('The phone number is not valid.')

        # if not validate_international_phonenumber(phone_number):
        #     raise ValidationError('The phone number is not valid.')
        #
        # return phone_number

    def __str__(self):
        if self.phone is None:
            return ''
        else:
            return self.user.first_name + ' ' + self.user.last_name + ' ' + self.phone.base_number_fmt

    def save(self,*args, **kwargs):
        super(Profile, self).save(*args, **kwargs)