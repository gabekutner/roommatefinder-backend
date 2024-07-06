# Generated by Django 4.1.13 on 2024-07-06 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_connection_display_match'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='snapchat',
        ),
        migrations.AddField(
            model_name='profile',
            name='pause_profile',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='link',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation date and time'),
        ),
        migrations.AlterField(
            model_name='link',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modification date and time'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation date and time'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modification date and time'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation date and time'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modification date and time'),
        ),
        migrations.AlterField(
            model_name='prompt',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation date and time'),
        ),
        migrations.AlterField(
            model_name='prompt',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modification date and time'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation date and time'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modification date and time'),
        ),
        migrations.AlterField(
            model_name='roommatequiz',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation date and time'),
        ),
        migrations.AlterField(
            model_name='roommatequiz',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='modification date and time'),
        ),
    ]