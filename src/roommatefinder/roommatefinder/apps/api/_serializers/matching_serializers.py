from rest_framework import serializers

from .. import models


class RoommateQuizSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.RoommateQuiz
    fields = '__all__'

class CreateRoommateQuizSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.RoommateQuiz
    exclude = ['profile']

# class UpdateRoommateQuiz