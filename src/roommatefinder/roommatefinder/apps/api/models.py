# -*- coding: utf-8 -*-
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField
from model_utils import Choices

from roommatefinder.apps.core.models import CreationModificationDateBase
from roommatefinder.apps.api.managers import CustomUserManager
from roommatefinder.settings._base import POPULAR_CHOICES, DORM_CHOICES


def upload_thumbnail(instance, filename):
  """ Defines where to upload a thumbnail. """
  path = f'thumbnails/{instance.id}'
  extension = filename.split('.')[-1]
  if extension:
    path = path + '.' + extension
  return path


# Create your models here.
class Profile(AbstractBaseUser, PermissionsMixin, CreationModificationDateBase):
  SEX_CHOICES = Choices(("M", "Male"), ("F", "Female"))
  
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  identifier = models.CharField(max_length=200, unique=True)
  name = models.CharField(max_length=200, null=True)
  password = models.CharField(max_length=200)
  age = models.PositiveIntegerField(default=0)

  major = models.CharField(max_length=25, null=True, default="Undecided")
  city = models.CharField(max_length=25, null=True, blank=True)
  state = models.CharField(max_length=25, null=True, blank=True)
  description = models.TextField(max_length=500, null=True, blank=True)
  dorm_building = models.CharField(choices=DORM_CHOICES, max_length=2, null=True)
  interests = MultiSelectField(choices=POPULAR_CHOICES, max_choices=5, max_length=1000)
  graduation_year = models.PositiveIntegerField(null=True, blank=True)

  otp = models.CharField(max_length=6, null=True, blank=True)
  otp_expiry = models.DateTimeField(blank=True, null=True)
  max_otp_try = models.CharField(max_length=2, default=3)
  otp_max_out = models.DateTimeField(blank=True, null=True)
  otp_verified = models.BooleanField(default=False)

  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  has_account = models.BooleanField(default=False)
  pause_profile = models.BooleanField(default=False)
  
  sex = models.CharField(
    choices=SEX_CHOICES,
    max_length=1,
    null=False,
    blank=False,
  )

  thumbnail = models.ImageField(
		upload_to=upload_thumbnail,
		null=True,
		blank=True
	)

  blocked_profiles = models.ManyToManyField(
    "self", symmetrical=False, related_name="blocked_by", blank=True
  )

  USERNAME_FIELD = "identifier"
  # required for creating user
  REQUIRED_FIELDS = []
  # custom profile creation + swiping algorithm 
  objects = CustomUserManager()

  def delete(self):
    super().delete()


class Photo(CreationModificationDateBase):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)
  image = models.ImageField(null=True, blank=True)

  def delete(self):
    self.image.delete(save=False)
    super().delete()


class RoommateQuiz(CreationModificationDateBase):
  profile = models.OneToOneField(
    Profile,
    on_delete=models.CASCADE,
    primary_key=True,
  )
  social_battery = models.IntegerField(
    null=False, 
    blank=False,
    validators=[
      MinValueValidator(0),
      MaxValueValidator(20)
    ],
    default=10
  )
  clean_room = models.CharField(max_length=100, null=False, blank=True, default="")
  noise_level = models.IntegerField(
    null=False, 
    blank=False,
    validators=[
      MinValueValidator(0),
      MaxValueValidator(20)
    ],
    default=10
  )
  guest_policy = models.CharField(max_length=100, null=False, blank=True, default="")
  in_room = models.IntegerField(
    null=False, 
    blank=False,
    validators=[
      MinValueValidator(0),
      MaxValueValidator(20)
    ],
    default=10
  )
  hot_cold = models.IntegerField(
    null=False, 
    blank=False,
    validators=[
      MinValueValidator(0),
      MaxValueValidator(20)
    ],
    default=10
  )
  bed_time = models.CharField(max_length=100, null=False, blank=True, default="")
  wake_up_time = models.CharField(max_length=100, null=False, blank=True, default="")
  sharing_policy = models.CharField(max_length=100, null=False, blank=True, default="")


class Connection(CreationModificationDateBase): 
  sender = models.ForeignKey(
    Profile,
    related_name='sent_connections',
    on_delete=models.CASCADE
  )
  receiver = models.ForeignKey(
    Profile,
    related_name='received_connections',
    on_delete=models.CASCADE
  )
  accepted = models.BooleanField(default=False)
  
  def __str__(self):
	  return str(self.sender.id) + ' -> ' + str(self.receiver.id)


class Message(CreationModificationDateBase):
  connection = models.ForeignKey(
		Connection,
		related_name='messages',
		on_delete=models.CASCADE
	)
  user = models.ForeignKey(
		Profile,
		related_name='my_messages',
		on_delete=models.CASCADE
	)
  text = models.TextField()

  def __str__(self):
    return str(self.user.id) + ': ' + self.text