# Generated by Django 5.1.2 on 2024-11-11 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='start_date',
            field=models.DateField(),
        ),
    ]