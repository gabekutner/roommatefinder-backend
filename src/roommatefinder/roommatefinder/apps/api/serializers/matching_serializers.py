from rest_framework import serializers
from .. import models


class RoommateQuizSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.RoommateQuiz
    fields = '__all__'


class CreateRoommateQuizSerializer(serializers.Serializer):
  social_battery = serializers.IntegerField(required=True, allow_null=False)
  clean_room = serializers.CharField(required=True, allow_null=False)
  noise_level = serializers.IntegerField(required=True, allow_null=False)
  guest_policy = serializers.CharField(required=True, allow_null=False)
  in_room = serializers.CharField(required=True, allow_null=False)
  hot_cold = serializers.IntegerField(required=True, allow_null=False)
  bed_time = serializers.CharField(required=True, allow_null=False)
  wake_up_time = serializers.CharField(required=True, allow_null=False)
  sharing_policy = serializers.CharField(required=True, allow_null=False)


class UpdateRoommateQuiz(serializers.Serializer):
  social_battery = serializers.IntegerField(required=False, allow_null=True)
  clean_room = serializers.CharField(required=False, allow_null=True)
  noise_level = serializers.IntegerField(required=False, allow_null=True)
  guest_policy = serializers.CharField(required=False, allow_null=True)
  in_room = serializers.IntegerField(required=False, allow_null=True)
  hot_cold = serializers.IntegerField(required=False, allow_null=True)
  bed_time = serializers.CharField(required=False, allow_null=True)
  wake_up_time = serializers.CharField(required=False, allow_null=True)
  sharing_policy = serializers.CharField(required=False, allow_null=True)