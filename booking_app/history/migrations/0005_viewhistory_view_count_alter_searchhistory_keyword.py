# Generated by Django 5.1.2 on 2024-11-11 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_remove_searchhistory_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewhistory',
            name='view_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='searchhistory',
            name='keyword',
            field=models.CharField(max_length=255),
        ),
    ]