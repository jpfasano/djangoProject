# Generated by Django 4.2 on 2023-04-27 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='route',
            old_name='title',
            new_name='route_name',
        ),
    ]
