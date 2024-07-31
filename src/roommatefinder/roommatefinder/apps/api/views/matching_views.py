# -*- coding: utf-8 -*-
from typing import Optional

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.request import Request

from roommatefinder.apps.api import models
from roommatefinder.apps.api.serializers import matching_serializers


class RoommateQuizViewSet(ModelViewSet):
  """
  ViewSet for managing matching quizs.

  Inherits from:
    ModelViewSet (rest_framework.viewsets)

  Attributes:
    queryset (QuerySet): A RoommateQuiz queryset.
    serializer_class (Type[matching_serializers.RoomateQuizSerializer])
    permission_classes (list): List of permission classes for access control.
  """
  queryset = models.RoommateQuiz.objects.all()
  serializer_class = matching_serializers.RoommateQuizSerializer
  permission_classes = [IsAuthenticated]


  def list(self, request: Request) -> Response:
    """
    List all matching quizs. Only accessible by superusers.

    Parameters:
      request (Request): The incoming HTTP request.

    Returns:
      Response: A Response object containing the profile data or an unauthorized error message.
    """
     # Check if the user is a superuser
    if not request.user.is_superuser:
      return Response({"detail": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = matching_serializers.RoommateQuizSerializer(self.queryset, many=True)
    # Prepare the response data
    response_data = {
      "message": "Hello admin.",
      "profile_count": self.queryset.count(),
      "profiles": serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)


  def retrieve(self, request: Request, pk: Optional[int] = None) -> Response:
    """
    Retrieve a matching quiz by the id of the profile who associated with it.

    This method attempts to fetch a matching quiz based on the provided primary key (pk). 
    If the quiz is not found, it returns a 400 Bad Request response with an error message.

    Parameters:
      request (Request): The HTTP request object that triggered this action.
      pk (Optional[int]): The primary key of the quiz to retrieve. Defaults to None.

    Returns:
      Response: 
        - On success: Returns the quiz data serialized with a 200 OK status.
        - On failure: Returns an error message with a 400 Bad Request status if the quiz does not exist.
    """
    try:
      quiz = self.queryset.get(profile=pk)
    except ObjectDoesNotExist:
      return Response(
        {
          "detail": f"Quiz: {pk} doesn't exist."
        }, 
        status=status.HTTP_400_BAD_REQUEST
      )
    # Serialize result
    serializer = matching_serializers.RoommateQuizSerializer(quiz, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

  def create(self, request: Request) -> Response:
    """
    Create a new quiz for the authenticated user.

    Parameters:
      request (Request): The incoming HTTP request containing profile data.

    Returns:
      Response: A Response object indicating the result of the profile creation.
        - On success: Returns the serialized quiz data and a 201 Created status.
        - On failure: Returns an error message indicating that the quiz creation failed. 
    """
    profile = request.user
    # Init serializer
    field_serializer = matching_serializers.CreateRoommateQuizSerializer(data=request.data, many=False)
    if field_serializer.is_valid(raise_exception=True):
      # Create profile fields with validated data
      quiz = models.RoommateQuiz.objects.create(profile=profile, **field_serializer.validated_data)
    else:
      return Response(
        {'detail': f'Create matching quiz for Profile: {profile.id} failed.'}, 
        status=status.HTTP_400_BAD_REQUEST
      )
    # Serialize and return
    matching_serializer = matching_serializers.RoommateQuizSerializer(quiz)
    return Response(matching_serializer.data, status=status.HTTP_201_CREATED)


  def update(self, request: Request, pk=None) -> Response:
    """
    Update a quiz for the authenticated user.

    Parameters:
      request (Request): The incoming HTTP request containing profile data.

    Returns:
      Response: A Response object indicating the result of the profile creation.
        - On success: Returns the serialized profile data and a 201 Created status.
        - On failure: Returns an error message indicating that a profile with the given identifier already exists, with a 400 Bad Request status.
    """
    field_serializer = matching_serializers.UpdateRoommateQuiz(data=request.data)
    if field_serializer.is_valid(raise_exception=True):
      try:
        quiz = self.queryset.get(pk=pk)
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
  
    quiz_serializer = matching_serializers.RoommateQuizSerializer(quiz)
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