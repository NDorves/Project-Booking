# Generated by Django 5.1.2 on 2024-11-11 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(choices=[('Excellent: 9 +', 'Excellent: 9 +'), ('Very good: 8 +', 'Very good: 8 +'), ('Good: 7 +', 'Good: 7 +'), ('Sufficient: 6 +', 'Sufficient: 6 +')]),
        ),
    ]
