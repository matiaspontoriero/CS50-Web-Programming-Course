# Generated by Django 5.1 on 2024-08-15 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental', '0003_car_is_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='is_crashed',
            field=models.BooleanField(default=False),
        ),
    ]
