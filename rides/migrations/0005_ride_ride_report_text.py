# Generated by Django 4.2 on 2023-05-11 15:55

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0004_alter_ride_options_ride_participants_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='ride_report_text',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]
