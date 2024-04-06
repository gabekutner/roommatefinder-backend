""" roommatefinder/apps/api/views/profile_views.py """
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist

from .. import serializers, models
from ..utils import exec


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
  def validate(self, attrs):
    data = super().validate(attrs)
    serializer = serializers.ProfileSerializer(self.user).data
    for key, value in serializer.items():
      data[key] = value
    return data

class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer
  permission_classes = [AllowAny]


class ProfileViewSet(ModelViewSet):
  """ Profile views """
  # https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
  queryset = models.Profile.objects.all()
  serializer_class = serializers.ProfileSerializer
  permission_classes = [IsAuthenticated]

  # admin actions for this model view set
  def get_permissions(self):
    ALLOW_ANY = ["create"]
    if self.action in ALLOW_ANY:
      return [AllowAny()]
    return [permission() for permission in self.permission_classes]

  def list(self, request):
    return Response(
      {"detail": "Not authorized."}, status=status.HTTP_401_UNAUTHORIZED
    )
  
  def create(self, request):
    """ Register / Sign Up for an account.  """
    data = request.data
    password = data["password"]
    repeated_password = data["repeated_password"]

    if password != repeated_password:
      return Response(
        {"detail": "Your password does not match."}, status=status.HTTP_400_BAD_REQUEST
      )
    
    try:
      user = models.Profile.objects.create(
        email=data["email"], password=make_password(data["password"])
      )
      serializer = serializers.ProfileSerializer(user, many=False)
      return Response(serializer.data)
    except:
      return Response(
        {"detail": "User with this email already exist."}, status=status.HTTP_400_BAD_REQUEST
      )
    
  def retrieve(self, request, pk=None):
    """ Get a Profile by id. """
    try:
      profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response(
        {"detail": "Profile does not exist."}, status=status.HTTP_400_BAD_REQUEST
      )

    exec.only_admin_and_user(profile.id, request)
    serializer = serializers.ProfileSerializer(profile, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def update(self, request, pk=None):
    """ Update a Profile. """
    fields_serializer = serializers.UpdateProfileSerializer(data=request.data)
    fields_serializer.is_valid(raise_exception=True)

    try:
      profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response(
        {"Error": "Profile does not exist."}, status=status.HTTP_400_BAD_REQUEST
      )

    exec.only_admin_and_user(profile.id, request)

    if "sex" in request.data:
      profile.sex = fields_serializer.validated_data["sex"]
    if "show_me" in request.data:
      profile.show_me = fields_serializer.validated_data["show_me"]
    if "instagram" in request.data:
      profile.instagram = fields_serializer.validated_data["instagram"]
    if "snapchat" in request.data:
      profile.snapchat = fields_serializer.validated_data["snapchat"]
    if "description" in request.data:
      profile.description = fields_serializer.validated_data["description"]
    if "interests" in request.data:
      profile.interests = fields_serializer.validated_data["interests"]
  
    profile.save()
    profile_serializer = serializers.ProfileSerializer(profile, many=False)
    return Response(profile_serializer.data)
  
  def destroy(self, request, pk=None):
    """ Delete a Profile. """
    try:
      profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response(
          {"Error": "Profile does not exist."}, status=status.HTTP_400_BAD_REQUEST
      )
    exec.only_admin_and_user(profile.id, request)
    profile.delete()
    return Response(
      {"detail": "User deleted successfully."}, status=status.HTTP_200_OK
    )
  
  @action(detail=False, methods=["post"], url_path=r"actions/create-profile")
  def create_profile(self, request):
    """ Create a profile. Must be a registered user. """
    profile = request.user
    fields_serializer = serializers.CreateProfileSerializer(data=request.data)
    fields_serializer.is_valid(raise_exception=True)

    profile.name = fields_serializer.validated_data["name"]
    profile.age = fields_serializer.validated_data["age"]
    profile.sex = fields_serializer.validated_data["sex"]
    profile.show_me = fields_serializer.validated_data["show_me"]

    profile.instagram = fields_serializer.validated_data["instagram"]
    profile.snapchat = fields_serializer.validated_data["snapchat"]
    profile.interests = fields_serializer.validated_data["interests"]
    profile.description = fields_serializer.validated_data["description"]
    
    profile.has_account = True

    profile.save()
    profile_serializer = serializers.ProfileSerializer(profile)
    return Response(profile_serializer.data)

  @action(detail=True, methods=["post"], url_path=r"actions/block-profile")
  def block_profile(self, request, pk=None):
    """ Block a profile. """
    current_profile = request.user
    try:
      blocked_profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response(
        {"Error": "Profile does not exist"}, status=status.HTTP_400_BAD_REQUEST
      )
    current_profile.block_profile(blocked_profile)
    return Response({"detail": f"Successfully blocked {blocked_profile.id}."}, status=status.HTTP_200_OK)
  
  @action(detail=True, methods=["post"], url_path=r"actions/unblock-profile")
  def unblock_profile(self, request, pk=None):
    """ Unblock a profile. """
    profile = request.user
    try:
      blocked_profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response({"Error": "Profile does not exist."})
    profile.blocked_profiles.remove(blocked_profile)
    return Response({"detail": f"Successfully unblocked {blocked_profile.id}."}, status=status.HTTP_200_OK)
  
  @action(detail=False, methods=["get"], url_path=r"actions/get-blocked-profiles")
  def get_blocked_profiles(self, request):
    """ Get all blocked profiles. """
    current_profile = request.user
    blocked_profiles = current_profile.blocked_profiles.all()
    # serializer = serializers.SwipeProfileSerializer(blocked_profiles, many=True)
    return Response({"count": blocked_profiles.count(), "results": blocked_profiles})

  @action(detail=False, methods=["post"], url_path=r"actions/reset-password")
  def reset_password(self, request):
    """ Reset password. """
    current_profile = request.user
    data = request.data
    password = data["password"]
    repeated_password = data["repeated_password"]

    if password == repeated_password:
      current_profile.password = make_password(password)
      current_profile.save()
      return Response(
        {"detail": "You password has been reset."}, status=status.HTTP_200_OK
      )

    return Response(
      {"detail": "Your passwords do not match."}, status=status.HTTP_400_BAD_REQUEST,
    )
  

class PhotoViewSet(ModelViewSet):
  serializer_class = serializers.PhotoSerializer
  permission_classes = [IsAuthenticated]

  def list(self, request):
    profile = request.user
    queryset = models.Photo.objects.filter(profile=profile.id).order_by("created")
    serializer = serializers.PhotoSerializer(queryset, many=True)
    return Response(serializer.data)

  def retrieve(self, request, pk):
    photo = models.Photo.objects.get(pk=pk)
    serializer = serializers.PhotoSerializer(photo, many=False)
    return Response(serializer.data)

  def create(self, request):
    profile = request.user
    profile_photos = models.Photo.objects.filter(profile=profile.id)
    fields_serializer = serializers.PhotoSerializer(data=request.data)
    fields_serializer.is_valid(raise_exception=True)

    if len(profile_photos) >= 5:
      return Response(
        {"detail": "Profile cannot have more than 5 images."}, status=status.HTTP_400_BAD_REQUEST,
      )

    photo = models.Photo.objects.create(
      profile=profile, image=fields_serializer._validated_data["image"]
    )
    serializer = serializers.PhotoSerializer(photo, many=False)
    return Response(serializer.data)

  def update(self, request, pk=None, *args, **kwargs):
    photo = models.Photo.objects.get(pk=pk)
    fields_serializer = serializers.PhotoSerializer(data=request.data, partial=True)
    fields_serializer.is_valid(raise_exception=True)
    photo.image = fields_serializer.validated_data["image"]

    photo.save()
    serializer = serializers.PhotoSerializer(photo, many=False)
    return Response(serializer.data)

  def destroy(self, request, pk):
    photo = models.Photo.objects.get(pk=pk)
    photo.delete()
    return Response({"detail": "Photo deleted."}, status=status.HTTP_200_OK)