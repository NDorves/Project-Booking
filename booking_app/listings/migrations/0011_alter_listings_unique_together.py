# Generated by Django 5.1.2 on 2024-11-25 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0010_alter_listings_owner'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='listings',
            unique_together={('title',)},
        ),
    ]
