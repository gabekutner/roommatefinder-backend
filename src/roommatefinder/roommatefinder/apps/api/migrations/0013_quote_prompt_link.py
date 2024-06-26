# Generated by Django 4.1.13 on 2024-06-04 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_roommatequiz'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quote', models.CharField(max_length=250)),
                ('cited', models.CharField(blank=True, max_length=100, null=True)),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question', models.CharField(choices=[('1', 'In one word, my friends would describe me as ...'), ('2', 'My ideal roommate is ...'), ('3', 'Hot take:'), ('4', 'The biggest red flag a roommate could have is ...'), ('5', 'The biggest green flag a roommate could have is ...'), ('6', 'A boundary of mine is ...'), ('7', 'All I ask of you is ...'), ('8', 'My dream career ...'), ('9', "If loving this is wrong, I don't want to be right ..."), ('10', 'My guilty pleasure is ...'), ('11', 'If someone broke into our dorm, my plan would be ...'), ('12', "Uh oh! Roommate's vape charger lit the room on fire, the first thing I'm grabbing is ..."), ('13', 'My parents would kill me if they found out I ...'), ('14', 'What would be the scariest sound to hear in your dorm room?'), ('15', 'The most embarrassing moment of my life was when ...'), ('16', 'My late night drive home along song is ...'), ('17', 'My ideal college day in the life looks like ...'), ('18', "Don't tell the RA ..."), ('19', 'My craziest side quest:'), ('20', 'My strange addiction:'), ('21', "I'm looking for a roommate who ..."), ('22', 'Weird flex:'), ('23', 'If I won the lottery, my first purchase would be ...'), ('24', 'Celebrity crush:'), ('25', "If I'm not in class, catch me ..."), ('26', "If you take my toothpaste I'll ...")], max_length=2)),
                ('answer', models.CharField(max_length=250)),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=250)),
                ('link', models.CharField(max_length=250)),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
