# Generated by Django 4.1.13 on 2024-07-25 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_remove_prompt_profile_remove_quote_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
