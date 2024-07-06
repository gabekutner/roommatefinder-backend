from rest_framework import serializers
from .. import models


class PhotoSerializer(serializers.ModelSerializer):
  image = serializers.ImageField(
    required=True, allow_null=False, max_length=None, use_url=True
  )
  class Meta:
    model = models.Photo
    fields = ["id", "image", "profile"]

class CreatePhotoSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Photo
    fields = ['image']