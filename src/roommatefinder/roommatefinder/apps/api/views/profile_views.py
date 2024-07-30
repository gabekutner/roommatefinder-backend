# -*- coding: utf-8 -*-
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
    identifier = request.data["identifier"]
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
    otp = request.data['otp']

    try:
      # Necessary query
      ## if you use >>> self.queryset.filter(id=user.id)
      ## an error is raised that there is no attribute profile.otp
      ## because profile_serializers.ProfileSerializer does not have the 
      ## otp related fields other than otp_verified
      profile = models.Profile.objects.get(id=user.id)
    except models.Profile.DoesNotExist:
      return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
    
    if str(profile.otp) == str(otp):
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
  def create_password(self, request):
    """Create the password for a :class:`~roommatefinder.apps.api.models.Profile` instance. 
    
    Returns a :class:`~roommatefinder.apps.api.serializers.ProfileSerializer` object.

    Required parameters:

    :param password: the password
    :param repeated_password: the password, again

    """
    data = request.data
    password = data["password"]
    repeated_password = data["repeated_password"]

    if password != repeated_password:
      return Response({"detail": "Your passwords don't match."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      profile = models.Profile.objects.get(id=request.user.id)
      if not profile.otp_verified:
        return Response(
          {'detail': f'Profile: {profile.id} needs to verify their account via otp before creating passwords.'}, 
          status=status.HTTP_400_BAD_REQUEST
        )
      profile.password = make_password(data["password"])
      profile.save()
      serializer = profile_serializers.ProfileSerializer(profile, many=False)
      return Response(serializer.data, status=status.HTTP_200_OK)
    except:
      return Response(
        {"detail": f"Error creating passwords for Profile: {request.user}."}, 
        status=status.HTTP_400_BAD_REQUEST
      )
          

  def retrieve(self, request, pk=None):
    """Get method for the :class:`~roommatefinder.apps.api.models.Profile` model. 
    
    Returns a :class:`~roommatefinder.apps.api.serializers.ProfileSerializer` object.

    """
    try:
      profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response(
        {"detail": f"Profile: {pk} doesn't exist."}, 
        status=status.HTTP_400_BAD_REQUEST
      )
    serializer = profile_serializers.ProfileSerializer(profile, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
  

  def update(self, request, pk=None):
    """Update method for the :class:`~roommatefinder.apps.api.models.Profile` model. 
    
    Returns a :class:`~roommatefinder.apps.api.serializers.ProfileSerializer` object.

    """
    profile = request.user
    field_serializer = profile_serializers.UpdateProfileSerializer(data=request.data, many=False)
    if field_serializer.is_valid(raise_exception=True):
      try:
        profile = models.Profile.objects.get(pk=pk)
      except ObjectDoesNotExist:
        return Response(
          {"detail": f"Profile: {pk} doesn't exist."}, 
          status=status.HTTP_400_BAD_REQUEST
        )

      if "name" in request.data:
        profile.name = field_serializer.validated_data["name"]
      if "city" in request.data:
        profile.city = field_serializer.validated_data["city"]
      if "state" in request.data:
        profile.state = field_serializer.validated_data["state"]
      if "graduation_year" in request.data:
        profile.graduation_year = field_serializer.validated_data["graduation_year"]
      if "major" in request.data:
        profile.major = field_serializer.validated_data["major"]
      if "description" in request.data:
        profile.description = field_serializer.validated_data["description"]
      if "interests" in request.data:
        profile.interests = field_serializer.validated_data["interests"]
      if "dorm_building" in request.data:
        profile.dorm_building = field_serializer.validated_data["dorm_building"]
      if "thumbnail" in request.data:
        profile.thumbnail = field_serializer.validated_data["thumbnail"]
      profile.save()

    else:
      return Response(
        {'detail': f'Update profile: {profile.id} failed.'}, 
        status=status.HTTP_400_BAD_REQUEST
      )
  
    profile_serializer = profile_serializers.ProfileSerializer(profile, many=False)
    return Response(profile_serializer.data, status=status.HTTP_200_OK)
  

  def destroy(self, request, pk=None):
    """ Delete method for the :class:`~roommatefinder.apps.api.models.Profile` model. """
    try:
      profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response(
        {"detail": f"Profile: {pk} doesn't exist."}, 
        status=status.HTTP_400_BAD_REQUEST
      )
    profile.delete()
    return Response(
      {"detail": f"Profile: {pk} deleted successfully."}, 
      status=status.HTTP_200_OK
    )


  @action(detail=False, methods=["post"], url_path=r"actions/upload-thumbnail")
  def upload_thumbnail(self, request):
    profile = request.user

    fields_serializer = profile_serializers.UploadThumbnailSerializer(data=request.data)
    if fields_serializer.is_valid():
      profile.thumbnail = fields_serializer.validated_data["thumbnail"]
      profile.save()

    profile_serializer = profile_serializers.ProfileSerializer(profile)
    return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
  

  @action(detail=False, methods=["post"], url_path=r"actions/create-profile")
  def create_profile(self, request):
    """Create a profile for AuthNavigator the :class:`~roommatefinder.apps.api.models.Profile` model. 

    Returns a :class:`~roommatefinder.apps.api.serializers.ProfileSerializer` object.

    Required parameters:

    :param name: string, 
    :param age: integer, 
    :param sex: string, either "M" or "F"
    :param thumbnail: file, 
    :param dorm_building: string, as an integer "1". See `~roommatefinder.settings._base.DORM_CHOICES` for options.

    Optional parameters: 

    :param city: string
    :param state: string, as the abbreviation. Ex. "CA", "FL"
    :param graduation_year: integer
    :param major: string
    :param interests: [string], as a list of integers in strings ["1", "2"]. See `~roommatefinder.settings._base.POPULAR_CHOICES` for options.
    :param description: string
    
    """
    profile = request.user
    fields_serializer = profile_serializers.CreateProfileSerializer(data=request.data, many=False)
    fields_serializer.is_valid(raise_exception=True)
  
    profile.name = fields_serializer.validated_data["name"]
    profile.age = fields_serializer.validated_data["age"]
    profile.sex = fields_serializer.validated_data["sex"]
    profile.thumbnail = fields_serializer.validated_data["thumbnail"]
    profile.dorm_building = fields_serializer.validated_data["dorm_building"]

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

    profile.has_account = True
    profile.save()

    profile_serializer = profile_serializers.ProfileSerializer(profile, many=False)
    return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
  

  @action(detail=False, methods=["get"], url_path=r"actions/swipe-profiles")
  def swipe_profiles(self, request):
    """Get a paginated 10 result list of the :class:`~roommatefinder.apps.api.models.Profile` model.
    
    Returns a :class:`~roommatefinder.apps.api.serializers.ProfileSerializer` object.
    
    """
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