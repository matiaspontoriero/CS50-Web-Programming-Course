# Generated by Django 5.0.6 on 2024-08-03 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_listing_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='isStock',
            field=models.BooleanField(default=True),
        ),
    ]
