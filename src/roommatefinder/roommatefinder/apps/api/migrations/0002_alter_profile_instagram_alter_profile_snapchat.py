# Generated by Django 4.1.13 on 2024-04-25 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='instagram',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='snapchat',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
