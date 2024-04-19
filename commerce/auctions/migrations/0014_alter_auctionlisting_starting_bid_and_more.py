# Generated by Django 5.0.4 on 2024-04-19 18:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auctionlisting_winner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=10),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='winner',
            field=models.ForeignKey(blank=True, default='No winner', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listings_bought', to=settings.AUTH_USER_MODEL),
        ),
    ]
