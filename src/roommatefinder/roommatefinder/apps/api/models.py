""" roommatefinder/apps/api/models.py """
import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from multiselectfield import MultiSelectField
from model_utils import Choices
from django.utils import timezone

from roommatefinder.apps.core.models import CreationModificationDateBase
from roommatefinder.apps.api.managers import CustomUserManager
from roommatefinder.settings._base import INTEREST_CHOICES

# Create your models here.
class Profile(AbstractBaseUser, PermissionsMixin, CreationModificationDateBase):
  """ Profile Model """
  SEX_CHOICES = Choices(("M", "Male"),
                        ("F", "Female"),)

  SHOW_ME_CHOICES = Choices(("M", "Men"),
                            ("W", "Women"),)

  interests = MultiSelectField(choices=INTEREST_CHOICES, max_choices=5, max_length=1000)

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  email = models.CharField(max_length=200, unique=True)
  name = models.CharField(max_length=200, null=True)
  password = models.CharField(max_length=200)
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  has_account = models.BooleanField(default=False)
  
  age = models.PositiveIntegerField(null=True)
  graduation_year = models.PositiveIntegerField(null=True)
  description = models.TextField(max_length=500, null=True)

  instagram = models.TextField(max_length=15, null=True)
  snapchat = models.TextField(max_length=15, null=True)
  
  sex = models.CharField(
    choices=SEX_CHOICES,
    # default=SEX_CHOICES.M,
    max_length=1,
    null=False,
    blank=False,
  )

  show_me = models.CharField(
    choices=SHOW_ME_CHOICES,
    # default=SHOW_ME_CHOICES.W,
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


class Photo(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)
  image = models.ImageField(null=True, blank=True)
  created_at = models.DateTimeField(default=timezone.now)

  def delete(self):
    self.image.delete(save=False)
    super().delete()