# Generated by Django 4.1.13 on 2024-06-05 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_quote_prompt_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='key',
        ),
    ]
