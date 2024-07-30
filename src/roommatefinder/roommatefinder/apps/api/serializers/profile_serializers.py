from rest_framework import serializers, fields
from rest_framework_simplejwt.tokens import RefreshToken

from roommatefinder.apps.api.serializers import photo_serializers
from roommatefinder.apps.api import models
from roommatefinder.apps.api.utils import model_utils
from roommatefinder.settings._base import POPULAR_CHOICES, DORM_CHOICES


class ProfileSerializer(serializers.ModelSerializer):
  token = serializers.SerializerMethodField(read_only=True)
  refresh_token = serializers.SerializerMethodField(read_only=True)
  photos = photo_serializers.PhotoSerializer(source="photo_set", many=True, read_only=True)
  sex = serializers.CharField(source="get_sex_display", required=True, allow_null=False)

  class Meta:
    model = models.Profile
    fields = ['id', 'token', 'refresh_token', 'sex',
              'photos', 'is_superuser', 'created', 'modified',
              'identifier', 'name', 'age',
              'major', 'city', 'state', 'description',
              'dorm_building', 'interests', 'has_account',
              'thumbnail', 'progress', 'graduation_year', 
              'pause_profile', 'otp_verified']
  
  # refresh the token everytime the user is called
  def get_token(self, profile):
    token = RefreshToken.for_user(profile)
    return str(token.access_token)

  def get_refresh_token(self, profile):
    token = RefreshToken.for_user(profile)
    return str(token)  
    

class CreateProfileSerializer(serializers.Serializer):
  # required
  name = serializers.CharField(required=True, allow_null=False)
  age = serializers.IntegerField(required=True, allow_null=False)
  sex = model_utils.ChoicesField(choices=models.Profile.SEX_CHOICES, required=True, allow_null=False)
  dorm_building = serializers.CharField(required=True, allow_null=False)  
  thumbnail = serializers.ImageField(required=True, allow_null=False, max_length=None, use_url=True)

  city = serializers.CharField(required=False, allow_null=True)
  state = serializers.CharField(required=False, allow_null=True)
  graduation_year = serializers.IntegerField(required=False, allow_null=True)
  major = serializers.CharField(required=False, allow_null=True)
  description = serializers.CharField(required=False, allow_null=True)
  interests = fields.MultipleChoiceField(choices=POPULAR_CHOICES, required=False, allow_null=True)


class UpdateProfileSerializer(serializers.Serializer):
  name = serializers.CharField(required=False, allow_null=True)
  city = serializers.CharField(required=False, allow_null=True)
  state = serializers.CharField(required=False, allow_null=True)
  graduation_year = serializers.CharField(required=False, allow_null=True)
  major = serializers.CharField(required=False, allow_null=True)
  description = serializers.CharField(required=False, allow_null=True)
  interests = serializers.MultipleChoiceField(choices=POPULAR_CHOICES, required=False, allow_null=True)
  dorm_building = serializers.ChoiceField(choices=DORM_CHOICES, required=False, allow_null=True)
  thumbnail = serializers.ImageField(required=False, allow_null=True, max_length=None, use_url=True)