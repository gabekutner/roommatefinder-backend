# Generated by Django 4.1.13 on 2024-07-02 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_remove_roommatequiz_preferred_noise_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='connection',
            name='display_match',
            field=models.BooleanField(default=False),
        ),
    ]