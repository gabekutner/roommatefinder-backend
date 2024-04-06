""" roommatefinder/apps/api/serializers.py """
from rest_framework import serializers, fields
from rest_framework_simplejwt.tokens import RefreshToken

from . import models
from roommatefinder.settings._base import INTEREST_CHOICES


class ChoicesField(serializers.Field):
  """ Custom Choices Field """
  def __init__(self, choices, **kwargs):
    self._choices = choices
    super(ChoicesField, self).__init__(**kwargs)

  def to_representation(self, obj):
    if obj in self._choices:
      return self._choices[obj]
    return obj

  def to_internal_value(self, data):
    if data in self._choices:
      return getattr(self._choices, data)
    raise serializers.ValidationError(["choice not valid"])
  

class PhotoSerializer(serializers.ModelSerializer):
  """ models.Photo Serializer """
  image = serializers.ImageField(
    required=True, allow_null=False, max_length=None, use_url=True
  )

  class Meta:
    model = models.Photo
    fields = ["id", "image", "profile"]


class ProfileSerializer(serializers.ModelSerializer):
  """ Profile Serializer """
  token = serializers.SerializerMethodField(read_only=True)
  refresh_token = serializers.SerializerMethodField(read_only=True)

  # transform the sex and show me into text "Male"
  sex = serializers.CharField(
    source="get_sex_display", required=True, allow_null=False
  )
  show_me = serializers.CharField(
    source="get_show_me_display", required=True, allow_null=False
  )

  photos = PhotoSerializer(source="photo_set", many=True, read_only=True)

  class Meta:
    model = models.Profile
    exclude = [
      "user_permissions",
      "groups",
      "password",
      "last_login",
      "is_staff",
      "is_active",
      "blocked_profiles",
   ]

  # refresh the token everytime the user is called
  def get_token(self, profile):
    token = RefreshToken.for_user(profile)
    return str(token.access_token)

  def get_refresh_token(self, profile):
    token = RefreshToken.for_user(profile)
    return str(token)
  

class CreateProfileSerializer(serializers.Serializer):
  name = serializers.CharField(required=True, allow_null=False)
  age = serializers.IntegerField(required=True, allow_null=False)
  instagram = serializers.CharField(required=False, allow_null=True, allow_blank=True)
  snapchat = serializers.CharField(required=False, allow_null=True, allow_blank=True)
  description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
  sex = ChoicesField(
    choices=models.Profile.SEX_CHOICES,
    required=True,
    allow_null=False,
  )
  show_me = ChoicesField(
    choices=models.Profile.SHOW_ME_CHOICES,
    required=False,
    allow_null=True,
  )
  interests = fields.MultipleChoiceField(
    choices=INTEREST_CHOICES,
    required=False,
    allow_null=True,
  )


class UpdateProfileSerializer(serializers.Serializer):
  instagram = serializers.CharField(required=False, allow_null=True)
  snapchat = serializers.CharField(required=False, allow_null=True)
  description = serializers.CharField(required=False, allow_null=True, allow_blank=True)
  sex = ChoicesField(
    choices=models.Profile.SEX_CHOICES,
    required=False,
    allow_null=True,
  )
  show_me = ChoicesField(
    choices=models.Profile.SHOW_ME_CHOICES,
    required=False,
    allow_null=True,
  )
  interests = fields.MultipleChoiceField(
    choices=INTEREST_CHOICES,
    required=False,
    allow_null=True,
  )