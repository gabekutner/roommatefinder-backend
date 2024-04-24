""" roommatefinder/apps/api/models.py """
import uuid
import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from multiselectfield import MultiSelectField
from model_utils import Choices
# from django.utils import timezone

from roommatefinder.apps.core.models import CreationModificationDateBase
from roommatefinder.apps.api.managers import CustomUserManager
from roommatefinder.settings._base import INTEREST_CHOICES, CHOICES, POPULAR_CHOICES

# Create your models here.
class Profile(AbstractBaseUser, PermissionsMixin, CreationModificationDateBase):
  """ Profile Model """
  SEX_CHOICES = Choices(("M", "Male"),
                        ("F", "Female"),)
  
  DORM_CHOICES = Choices(('1', 'Chapel Glen'), 
                ('2', 'Gateway Heights'),
                ('3' ,'Impact and Prosperity Epicenter'),
                ('4', 'Kahlert Village'),
                ('5', 'Lassonde Studios'),
                ('6', 'Officers Circle'),
                ('7', 'Sage Point'),
                ('8', 'Marriott Honors Community'),
                ('9', 'Guest House'),
                ('10', "I don't know"), )

  # base
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  email = models.CharField(max_length=200, unique=True)
  name = models.CharField(max_length=200, null=True)
  password = models.CharField(max_length=200)

  birthday = models.DateField(null=True)
  # age = models.PositiveIntegerField(null=True)
  description = models.TextField(max_length=500, null=True)
  instagram = models.TextField(max_length=15, null=True)
  snapchat = models.TextField(max_length=15, null=True)

  # extra
  city = models.CharField(max_length=25, null=True)
  state = models.CharField(max_length=25, null=True)
  major = models.CharField(max_length=50, null=True, default="Undecided")
  minor = models.CharField(max_length=50, null=True)
  graduation_year = models.PositiveIntegerField(null=True)
  dorm_building = models.CharField(choices=DORM_CHOICES, max_length=2, null=True)
  interests = MultiSelectField(choices=POPULAR_CHOICES, max_choices=5, max_length=1000)

  # background
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  has_account = models.BooleanField(default=False)
  
  sex = models.CharField(
    choices=SEX_CHOICES,
    max_length=1,
    null=False,
    blank=False,
  )

  blocked_profiles = models.ManyToManyField(
    "self", symmetrical=False, related_name="blocked_by", blank=True
  )

  USERNAME_FIELD = "email"
  # requred for creating user
  REQUIRED_FIELDS = []

  objects = CustomUserManager()

  @property
  def age(self):
    if self.birthday:
      return int((datetime.date.today() - self.birthday).days / 365.25)

  def block_profile(self, blocked_profile):
    """ Block a profile. """
    # remove likes
    # remove match
    # remove conversation
    self.blocked_profiles.add(blocked_profile)

  def delete(self):
    """ Delete your profile. """
    # delete conversations
    super().delete()


class Photo(CreationModificationDateBase):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)
  image = models.ImageField(null=True, blank=True)

  def delete(self):
    self.image.delete(save=False)
    super().delete()