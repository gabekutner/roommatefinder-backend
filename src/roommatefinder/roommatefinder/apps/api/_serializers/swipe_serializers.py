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
  prompts = extra_serializers.PromptSerializer(source="prompt_set", many=True, read_only=True)
  quotes = extra_serializers.QuoteSerializer(source="quote_set", many=True, read_only=True)
  links = extra_serializers.LinkSerializer(source="link_set", many=True, read_only=True)
  # get status of connection between 
  sent_connections = extra_serializers.ConnectionSerializer(many=True)
  received_connections = extra_serializers.ConnectionSerializer(many=True)

  class Meta:
    model = models.Profile
    fields = [
      "id", "email", "name",
      "birthday", "age", "sex",
      "city", "state", "major",
      "dorm_building", "description", "interests", 
      "thumbnail", "graduation_year", "photos",
      "prompts", "quotes", "links",
      "sent_connections", "received_connections",
    ]