# Generated by Django 5.1 on 2024-08-14 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0002_remove_booking_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
