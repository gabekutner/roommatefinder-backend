# Generated by Django 4.1.13 on 2024-07-31 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connection',
            name='display_match',
        ),
    ]