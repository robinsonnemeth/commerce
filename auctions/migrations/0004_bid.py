# Generated by Django 3.2.9 on 2021-12-28 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211227_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_bid', models.DateTimeField(auto_now=True)),
                ('bid', models.DecimalField(decimal_places=2, max_digits=6)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.listing')),
                ('user_bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_bid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
