# Generated by Django 4.1.13 on 2024-07-25 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_remove_connection_updated_connection_modified_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='email',
            new_name='identifier',
        ),
    ]