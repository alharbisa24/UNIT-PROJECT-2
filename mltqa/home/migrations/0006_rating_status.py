# Generated by Django 4.2.23 on 2025-07-27 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_rename_starts_rating_stars'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
