# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from .. import models
from ..serializers.matching_serializers import RoommateQuizSerializer, CreateRoommateQuizSerializer, UpdateRoommateQuiz


class RoommateQuizViewSet(ModelViewSet):
  queryset = models.RoommateQuiz.objects.all()
  serializer_class = RoommateQuizSerializer
  permission_classes = [IsAuthenticated]

  def list(self, request):
    """ Get all matching quizes. """
    serializer = RoommateQuizSerializer(self.queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


  def retrieve(self, request, pk=None):
    """Get method for the :class:`~roommatefinder.apps.api.models.RoommateQuiz` model. 
    
    Returns a :class:`~roommatefinder.apps.api.serializers.matching_serializers.RoommateQuizSerializer` object.

    """
    quiz = self.queryset.filter(profile=pk)
    serializer = RoommateQuizSerializer(quiz, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

  def create(self, request):
    """Create method for the :class:`~roommatefinder.apps.api.models.Profile` model. 
    
    Returns a :class:`~roommatefinder.apps.api.serializers.profile_serializers.ProfileSerializer` object.

    Required parameters:

      :param social_battery: integer
      :param clean_room: string
      :param noise_level: integer
      :param guest_policy: string
      :param in_room: integer
      :param hot_cold: integer
      :param bed_time: string
      :param wake_up_time: string
      :param sharing_policy: string

    """
    profile = request.user
    field_serializer = CreateRoommateQuizSerializer(data=request.data, many=False)
    if field_serializer.is_valid(raise_exception=True):
      quiz = models.RoommateQuiz.objects.create(profile=profile, **field_serializer.validated_data)
    else:
      return Response(
        {'detail': f'Create matching quiz for Profile: {profile.id} failed.'}, 
        status=status.HTTP_400_BAD_REQUEST
      )
    
    matching_serializer = RoommateQuizSerializer(quiz)
    return Response(matching_serializer.data, status=status.HTTP_201_CREATED)


  def update(self, request, pk=None):
    """Update method for the :class:`~roommatefinder.apps.api.models.RoommateQuiz` model. 

    Returns a :class:`~roommatefinder.apps.api.serializers.matching_serializers.RoommateQuizSerializer` object.

    """
    field_serializer = UpdateRoommateQuiz(data=request.data)
    if field_serializer.is_valid(raise_exception=True):
      try:
        quiz = models.RoommateQuiz.objects.get(pk=pk)
      except ObjectDoesNotExist:
        return Response({"detail": f"Profile: {pk} doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
      
      if "social_battery" in request.data:
        quiz.social_battery = field_serializer.validated_data["social_battery"]
      if "clean_room" in request.data:
        quiz.clean_room = field_serializer.validated_data["clean_room"]
      if "noise_level" in request.data:
        quiz.noise_level = field_serializer.validated_data["noise_level"]
      if "guest_policy" in request.data:
        quiz.guest_policy = field_serializer.validated_data["guest_policy"]
      if "in_room" in request.data:
        quiz.in_room = field_serializer.validated_data["in_room"]
      if "hot_cold" in request.data:
        quiz.hot_cold = field_serializer.validated_data["hot_cold"]
      if "bed_time" in request.data:
        quiz.bed_time = field_serializer.validated_data["bed_time"]
      if "wake_up_time" in request.data:
        quiz.wake_up_time = field_serializer.validated_data["wake_up_time"]
      if "sharing_policy" in request.data:
        quiz.sharing_policy = field_serializer.validated_data["sharing_policy"]
      quiz.save()
    else:
      return Response(
        {'detail': f'Update matching quiz: {pk} failed.'}, 
        status=status.HTTP_400_BAD_REQUEST
      )
  
    quiz_serializer = RoommateQuizSerializer(quiz)
    return Response(quiz_serializer.data, status=status.HTTP_200_OK)


  def destroy(self, request, pk=None):
    """ Delete matching quiz. """
    try:
      quiz = models.RoommateQuiz.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response(
        {"detail": f"Profile: {pk} doesn't exist."}, 
        status=status.HTTP_400_BAD_REQUEST
      )

    quiz.delete()
    return Response(
      {"detail": f"Matching Quiz: {pk} deleted successfully."}, 
      status=status.HTTP_200_OKs
    )