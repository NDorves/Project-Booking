# Generated by Django 5.1.2 on 2024-11-12 10:54

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_alter_review_rating'),
        ('user', '0002_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-updated_at']},
        ),
        migrations.AddField(
            model_name='review',
            name='rating_designation',
            field=models.CharField(choices=[('Excellent', 'Excellent'), ('Very good', 'Very good'), ('Good', 'Good'), ('Sufficient', 'Sufficient')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='user.user'),
        ),
    ]