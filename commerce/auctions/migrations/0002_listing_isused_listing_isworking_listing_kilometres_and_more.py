# Generated by Django 5.0.6 on 2024-08-03 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='isUsed',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='isWorking',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='kilometres',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, max_digits=30),
        ),
    ]
