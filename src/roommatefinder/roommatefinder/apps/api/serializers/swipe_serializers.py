from rest_framework import serializers

from .. import models
from . import photo_serializers, extra_serializers


class SwipeProfileSerializer(serializers.ModelSerializer):
  sex = serializers.CharField(
    source="get_sex_display", 
    required=True, 
    allow_null=False
  )

  photos = photo_serializers.PhotoSerializer(source="photo_set", many=True, read_only=True)
  sent_connections = extra_serializers.ConnectionSerializer(many=True)
  received_connections = extra_serializers.ConnectionSerializer(many=True)

  class Meta:
    model = models.Profile
    fields = [
      "id", "identifier", "name",
      "age", "sex",
      "city", "state", "major",
      "dorm_building", "description", "interests", 
      "thumbnail", "graduation_year", "photos",
      "sent_connections", "received_connections",
    ]