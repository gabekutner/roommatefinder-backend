from rest_framework import serializers, fields
from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers import (
  PhotoSerializer,
  PromptSerializer,
  QuoteSerializer,
  LinkSerializer,
  CreatePromptSerializer,
  CreateQuoteSerializer,
  CreateLinkSerializer,
)
from .. import models
from ..utils import model_utils
from roommatefinder.settings._base import POPULAR_CHOICES


class ProfileSerializer(serializers.ModelSerializer):
  token = serializers.SerializerMethodField(read_only=True)
  refresh_token = serializers.SerializerMethodField(read_only=True)

  photos = PhotoSerializer(source="photo_set", many=True, read_only=True)
  prompts = PromptSerializer(source="prompt_set", many=True, read_only=True)
  quotes = QuoteSerializer(source="quote_set", many=True, read_only=True)
  links = LinkSerializer(source="link_set", many=True, read_only=True)
  sex = serializers.CharField(source="get_sex_display", required=True, allow_null=False)

  class Meta:
    model = models.Profile
    fields = ['id', 'token', 'refresh_token', 'sex',
              'photos', 'prompts', 'quotes', 'links',
              'is_superuser', 'created', 'modified',
              'email', 'name', 'birthday', 'age',
              'major', 'city', 'state', 'description',
              'dorm_building', 'interests', 'has_account',
              'thumbnail', 'progress', 'graduation_year']
  
  # refresh the token everytime the user is called
  def get_token(self, profile):
    token = RefreshToken.for_user(profile)
    return str(token.access_token)

  def get_refresh_token(self, profile):
    token = RefreshToken.for_user(profile)
    return str(token)  
    

class CreateProfileSerializer(serializers.Serializer):
  birthday = serializers.DateField(required=True, allow_null=False)
  sex = model_utils.ChoicesField(choices=models.Profile.SEX_CHOICES, required=True, allow_null=False)
  city = serializers.CharField(required=True, allow_null=False)
  state = serializers.CharField(required=True, allow_null=False)
  graduation_year = serializers.IntegerField(required=True, allow_null=False)
  major = serializers.CharField(required=True, allow_null=False)
  interests = fields.MultipleChoiceField(choices=POPULAR_CHOICES, required=True, allow_null=False)
  dorm_building = serializers.CharField(required=True, allow_null=False)  
  prompts = CreatePromptSerializer(source='prompt_set', many=True, required=True)
  quotes = CreateQuoteSerializer(source='quote_set', many=True, required=True)
  links = CreateLinkSerializer(source='link_set', many=True, required=True)


class UpdateProfileSerializer(serializers.Serializer):
  name = serializers.CharField(required=False, allow_null=True)
  city = serializers.CharField(required=False, allow_null=True)
  state = serializers.CharField(required=False, allow_null=True)
  graduation_year = serializers.CharField(required=False, allow_null=True)
  major = serializers.CharField(required=False, allow_null=True)
  interests = serializers.MultipleChoiceField(choices=POPULAR_CHOICES, required=False, allow_null=True)

# Extras
class UploadThumbnailSerializer(serializers.Serializer):
  thumbnail = serializers.ImageField(
    required=True, allow_null=False, max_length=None, use_url=True
  )