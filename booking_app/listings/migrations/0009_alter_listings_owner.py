# Generated by Django 5.1.2 on 2024-11-12 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_alter_listings_rating'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_listings', to='user.user'),
        ),
    ]