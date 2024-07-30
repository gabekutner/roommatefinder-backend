# -*- coding: utf-8 -*-
import re
from typing import List, Optional

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from .. import models, pagination
from ..serializers import profile_serializers, swipe_serializers


class ProfileViewSet(ModelViewSet):
  """
  ViewSet for managing user profiles.

  Inherits from:
    ModelViewSet (rest_framework.viewsets)

  Attributes:
    queryset (QuerySet): The queryset to be used for this viewset.
    serializer_class (Type[profile_serializers.ProfileSerializer]): The serializer class to be used.
    permission_classes (list): List of permission classes for access control.
  """
  queryset = models.Profile.objects.all()
  serializer_class = profile_serializers.ProfileSerializer
  permission_classes = [IsAuthenticated]

  def get_permissions(self):
    """
    Determines the permissions required based on the action being performed.

    Returns:
      list: A list of permission instances based on the action.
    """
    ALLOW_ANY = ["create"]
    if self.action in ALLOW_ANY:
      return [AllowAny()]
    return [permission() for permission in self.permission_classes]
  

  def list(self, request: Request) -> Response:
    """
    List all profiles. Only accessible by superusers.

    Parameters:
      request (Request): The incoming HTTP request.

    Returns:
      Response: A Response object containing the profile data or an unauthorized error message.
    """
    # Check if the user is a superuser
    if not request.user.is_superuser:
      return Response({"detail": "Unauthorizd access"}, status=status.HTTP_403_FORBIDDEN)

    serializer = profile_serializers.ProfileSerializer(self.queryset, many=True)
    # Prepare the response data
    response_data = {
      "message": "Hello admin.",
      "profile_count": self.queryset.count(),
      "profiles": serializer.data
    }
    return Response(response_data, status=status.HTTP_200_OK)
    

  def create(self, request: Request) -> Response:
    """
    Create a new profile with given identifier.

    Parameters:
      request (Request): The incoming HTTP request containing profile data.

    Returns:
      Response: A Response object indicating the result of the profile creation.
        - On success: Returns the serialized profile data and a 201 Created status.
        - On failure: Returns an error message indicating that a profile with the given identifier already exists, with a 400 Bad Request status.
    """
    try:
      # Ensure an otp code was sent
      identifier = request.data['identifier']
      # Ensure identifier is of type string
      assert type(identifier) == str
      # Ensure identifier is either an email, phone number, or UID
      patterns = [
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', 
        r'^\+?[\d\s.-]{7,15}$',
        r'^u\d{7}$'
      ]
      def match(id: str, patterns: List[str]) -> bool:
        for pattern in patterns:
          if re.match(pattern, id):
            return True
        return False
      # Test identifier matches one of the patterns
      assert match(identifier, patterns)
    except Exception:
      return Response(
        {
          "detail": "Please provide an identifier as a string. Identifier's can be an email address, a phone number, or a UID.",
          "example_request_email": {
            "identifier": "example@gmail.com"
          },
          "example_request_phone": {
            "identifier": "123 123 1234"
          },
          "example_request_uid": {
            "identifier": "u1234567"
          },
        }, 
        status=status.HTTP_404_NOT_FOUND
      )

    try:
      # Attempt to create a new profile with the provided identifier
      profile = models.Profile.objects.create(identifier=identifier)
      serializer = profile_serializers.ProfileSerializer(profile, many=False)
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
      # Return an error response if a profile with the given identifier already exists
      return Response({"detail": "A profile with this identifier already exists."}, status=status.HTTP_400_BAD_REQUEST)
    

  @action(detail=False, methods=["post"], url_path=r"actions/verify-otp", url_name="otp-verify")
  def verify_otp(self, request: Request) -> Response:
    """
    Verify the OTP provided by the user.

    This action checks if the provided OTP matches the one stored in the user's profile. 
    If the OTP is correct, it clears the OTP fields in the profile and marks the OTP as verified.
    Otherwise, it returns an error indicating an incorrect OTP.

    Parameters:
      request (Request): The incoming HTTP request containing the OTP.

    Returns:
      Response: A Response object indicating the result of the OTP verification.
        - On success: Returns the updated profile data and a 200 OK status.
        - On failure: Returns an error message with a 400 Bad Request status.
    """
    user = request.user

    try:
      # Ensure an otp code was sent
      otp = request.data['otp']
      # Ensure it was of type string
      assert type(otp) == str
      # Ensure it was 4 digits
      assert len(otp) == 4
    except Exception:
      return Response(
        {
          'detail': 'Please provide a 4-digit otp code as a string.',
          'example_request': {
            'otp': '1234'
          }
        }, 
        status=status.HTTP_400_BAD_REQUEST
      )

    try:
      # Necessary query
      ## if you use >>> self.queryset.filter(id=user.id)
      ## an error is raised that there is no attribute profile.otp
      ## because profile_serializers.ProfileSerializer does not have the 
      ## otp related fields other than otp_verified
      profile = models.Profile.objects.get(id=user.id)
    except models.Profile.DoesNotExist:
      return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if profile.otp == otp:
      # OTP is correct, update the profile
      profile.otp = None
      profile.otp_expiry = None
      profile.max_otp_try = 3
      profile.otp_max_out = None
      profile.otp_verified = True
      profile.save()
      # Serialize the updated profile
      serializer = profile_serializers.ProfileSerializer(profile, many=False)
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      # OTP is incorrect
      return Response(
        {"detail": f"Not the correct verification code for the profile: {profile.id}."}, 
        status=status.HTTP_400_BAD_REQUEST
      )
    

  @action(detail=False, methods=["post"], url_path=r"actions/create-password", url_name="create-password")
  def create_password(self, request: Request) -> Response:
    """
    Create a password for the user's profile.

    This action allows users to set their password, provided they have verified their account via OTP.
    It checks that the password and repeated password match before updating the profile.

    Parameters:
      request (Request): The incoming HTTP request containing the password details.

    Returns:
      Response: A Response object indicating the result of the password creation/update.
        - On success: Returns the updated profile data with a 200 OK status.
        - On failure: Returns an error message with a 400 Bad Request status.
    """
    user = request.user
    try:
      # Ensure both passwords were sent
      password = request.data["password"]
      repeated_password = request.data["repeated_password"]
      # Ensure both passwords match
      assert password == repeated_password
    except Exception:
      return Response(
        {
          "detail": "Either both passwords were not sent or passwords don't match.",
          "example_request": {
            "password": "123",
            "repeated_password": "123"
          },
        }, 
        status=status.HTTP_400_BAD_REQUEST
      )

    try:
      # Get profile out of the queryset
      ## This works because otp_verified is included in ProfileSerializer
      profile = self.queryset.get(id=user.id)
      # Ensure user is otp verified before creating their password.
      if not profile.otp_verified:
        return Response(
          {'detail': f'Profile: {profile.id} needs to verify their account via otp before creating passwords.'}, 
          status=status.HTTP_400_BAD_REQUEST
        )
      # Create the password
      profile.password = make_password(request.data["password"])
      profile.save()
      # Serialize
      serializer = profile_serializers.ProfileSerializer(profile, many=False)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
      return Response(
        {
          "detail": f"Error creating passwords for Profile: {request.user}.",
          "error": str(e)
        }, 
        status=status.HTTP_400_BAD_REQUEST
      )
          

  def retrieve(self, request: Request, pk: Optional[int] = None) -> Response:
    """
    Retrieve a profile by its primary key (pk).

    This method attempts to fetch a profile based on the provided primary key (pk). 
    If the profile is not found, it returns a 400 Bad Request response with an error message.

    Parameters:
      request (Request): The HTTP request object that triggered this action.
      pk (Optional[int]): The primary key of the profile to retrieve. Defaults to None.

    Returns:
      Response: 
        - On success: Returns the profile data serialized with a 200 OK status.
        - On failure: Returns an error message with a 400 Bad Request status if the profile does not exist.
    """
    try:
      profile = self.queryset.get(pk=pk)
    except ObjectDoesNotExist:
      return Response(
        {"detail": f"Profile: {pk} doesn't exist."}, 
        status=status.HTTP_400_BAD_REQUEST
      )
    # Serialize result
    serializer = profile_serializers.ProfileSerializer(profile, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
  

  def update(self, request: Request, pk: Optional[int] = None) -> Response:
    """
    Update a user's profile with the provided data.

    This method updates specific fields of a user's profile based on the provided primary key (pk). 
    It checks if the profile exists and whether the update data is valid before applying the changes.

    Parameters:
      request (Request): The HTTP request object containing the update data.
      pk (Optional[int]): The primary key of the profile to be updated. Defaults to None.

    Returns:
      Response:
        - On success: Returns the updated profile data with a 200 OK status.
        - On failure: Returns an error message with a 400 Bad Request status if the profile does not exist or if the update fails.
    """
    profile = request.user
    # Init serializer
    field_serializer = profile_serializers.UpdateProfileSerializer(data=request.data, many=False)
    if field_serializer.is_valid(raise_exception=True):
      try:
        profile = self.queryset.get(pk=pk)
      except ObjectDoesNotExist:
        return Response({"detail": f"Profile: {pk} doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
      # Update fields if they are present in the request data
      for field in ['name', 'city', 'state', 'graduation_year', 'major', 'description', 'interests', 'dorm_building', 'thumbnail']:
        if field in request.data:
          setattr(profile, field, field_serializer.validated_data[field])
      # Save profile
      profile.save()
    # Serialize and return 
    profile_serializer = profile_serializers.ProfileSerializer(profile, many=False)
    return Response(profile_serializer.data, status=status.HTTP_200_OK)
  

  def destroy(self, request: Request, pk: Optional[int] = None) -> Response:
    """
    Delete a profile by its primary key (pk).

    This method attempts to delete a profile based on the provided primary key (pk). 
    If the profile does not exist, it returns a 400 Bad Request response with an error message. 
    If the deletion is successful, it returns a confirmation message with a 200 OK status.

    Parameters:
      request (Request): The HTTP request object that triggered this action.
      pk (Optional[int]): The primary key of the profile to be deleted. Defaults to None.

    Returns:
      Response:
        - On success: Returns a confirmation message with a 200 OK status.
        - On failure: Returns an error message with a 400 Bad Request status if the profile does not exist.
    """
    try:
      profile = self.queryset.get(pk=pk)
    except ObjectDoesNotExist:
      return Response({"detail": f"Profile: {pk} doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
    # Delete the retrieved profile
    profile.delete()
    return Response({"detail": f"Profile: {pk} deleted successfully."}, status=status.HTTP_200_OK)
  

  @action(detail=False, methods=["post"], url_path=r"actions/create-profile", url_name="create-profile")
  def create_profile(self, request):
    """
    Create or update the profile for the currently authenticated user.

    This method allows an authenticated user to create or update their profile with the provided data. 
    It ensures that all required fields are validated before applying changes.

    Parameters:
      request (Request): The HTTP request object containing the profile data to be created or updated.

    Returns:
      Response:
        - On success: Returns the updated profile data with a 201 Created status.
        - On failure: Returns an error message with a 400 Bad Request status if the data is invalid.
    """
    profile = request.user
    # Init serializer
    fields_serializer = profile_serializers.CreateProfileSerializer(data=request.data, many=False)
    if fields_serializer.is_valid(raise_exception=True):
      # Update profile fields with validated data
      profile.name = fields_serializer.validated_data["name"]
      profile.age = fields_serializer.validated_data["age"]
      profile.sex = fields_serializer.validated_data["sex"]
      profile.thumbnail = fields_serializer.validated_data["thumbnail"]
      profile.dorm_building = fields_serializer.validated_data["dorm_building"]
      # Optionally update additional fields if they are present in the validated data
      if "city" in fields_serializer.validated_data: 
        profile.city = fields_serializer.validated_data["city"]
      if "state" in fields_serializer.validated_data:
        profile.state = fields_serializer.validated_data["state"]
      if "graduation_year" in fields_serializer.validated_data:
        profile.graduation_year = fields_serializer.validated_data["graduation_year"]
      if "major" in fields_serializer.validated_data:
        profile.major = fields_serializer.validated_data["major"]
      if "interests" in fields_serializer.validated_data:
        profile.interests = fields_serializer.validated_data["interests"]
      if "description" in fields_serializer.validated_data:
        profile.description = fields_serializer.validated_data["description"]
      # Mark the profile as having an account
      profile.has_account = True
      # Save profile
      profile.save()
    # Serialize and return
    profile_serializer = profile_serializers.ProfileSerializer(profile, many=False)
    return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
  

  @action(detail=False, methods=["get"], url_path=r"actions/swipe-profiles")
  def swipe_profiles(self, request):
    # @! convert over to an algorithm in a separate file
    # get the ModelViewSet queryset
    profiles = self.get_queryset()
    profiles = profiles.filter(has_account=True)
    
    connections = models.Connection.objects.filter(
      Q(sender=request.user.id) | Q(receiver=request.user.id),
      accepted=True
    )
    # remove connections from a result
    excluded_ids = connections.values_list('sender', 'receiver')
    excluded_ids = set([id for sublist in excluded_ids for id in sublist])
    
    # remove current user for result by default
    if not bool(excluded_ids):
      excluded_ids = set([request.user.id])

    profiles = profiles.exclude(id__in=excluded_ids)

    # Apply pagination
    paginator = pagination.StandardResultsSetPagination()
    paginated_profiles = paginator.paginate_queryset(profiles, request, view=self)
    
    # Serialize the paginated profiles
    serializer = swipe_serializers.SwipeProfileSerializer(paginated_profiles, many=True)
    return paginator.get_paginated_response(serializer.data)

  
  @action(detail=True, methods=["get"], url_path=r"actions/swipe-profile")
  def swipe_profile(self, request, pk=None):
    """Get a single :class:`~roommatefinder.apps.api.models.Profile` instance as a class:`~roommatefinder.apps.api.serialiers.profile_serializers.SwipeProfileSerializer` object.
    
    Returns a :class:`~roommatefinder.apps.api.serializers.profile_serializers.ProfileSerializer` object.

    Required parameters:

    :param pk: The id of the profile to get

    """
    # /api/v1/profiles/{pk}/actions/swipe-profile/
    try:
      profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response(
        {"detail": f"Profile: {pk} doesn't exist."}, 
        status=status.HTTP_400_BAD_REQUEST
      )

    serializer = swipe_serializers.SwipeProfileSerializer(profile, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


  #! @not in v 1.0.0
  @action(detail=True, methods=["post"], url_path=r"actions/block-profile")
  def block_profile(self, request, pk=None):
    """ block a profile """
    current_profile = request.user
    try:
      blocked_profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response({"detail": "profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    current_profile.block_profile(blocked_profile)
    return Response({"detail": f"successfully blocked {blocked_profile.id}"}, status=status.HTTP_200_OK)
  
  #! @not in v 1.0.0
  @action(detail=True, methods=["post"], url_path=r"actions/unblock-profile")
  def unblock_profile(self, request, pk=None):
    """ unblock a profile """
    profile = request.user
    try:
      blocked_profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response({"detail": "profile does not exist"}, status=status.HTTP_404_NOT_FOUND)
    profile.blocked_profiles.remove(blocked_profile)
    return Response({"detail": f"successfully unblocked {blocked_profile.id}"}, status=status.HTTP_200_OK)
  
  #! @not in v 1.0.0
  @action(detail=False, methods=["get"], url_path=r"actions/get-blocked-profiles")
  def get_blocked_profiles(self, request):
    """ get all blocked profiles """
    current_profile = request.user
    blocked_profiles = current_profile.blocked_profiles.all()
    serializer = swipe_serializers.SwipeProfileSerializer(blocked_profiles, many=True)
    return Response({"count": blocked_profiles.count(), "results": serializer.data})

  #! @not in v 1.0.0
  @action(detail=False, methods=["post"], url_path=r"actions/reset-password")
  def reset_password(self, request):
    """ reset password """
    current_profile = request.user
    data = request.data
    password = data["password"]
    repeated_password = data["repeated_password"]

    if password == repeated_password:
      current_profile.password = make_password(password)
      current_profile.save()
      return Response({"detail": "your password has been reset"}, status=status.HTTP_200_OK)

    return Response({"detail": "your passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)
  

  @action(detail=False, methods=["post"], url_path=r"actions/pause-profile")
  def pause_profile(self, request):
    """Pause profile for an account.

    @! Deprecated on closing of `https://github.com/gabekutner/roommatefinder-backend/issues/5`
    
    """
    current_profile = request.user
    pause_profile_status = current_profile.pause_profile
    current_profile.pause_profile = not pause_profile_status
    current_profile.save()
    serializer = profile_serializers.ProfileSerializer(current_profile, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)