# Generated by Django 5.0.4 on 2024-04-18 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auctionlisting_current_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='current_bid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
