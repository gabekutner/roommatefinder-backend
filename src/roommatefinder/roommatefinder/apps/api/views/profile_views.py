from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.parsers import MultiPartParser, FormParser

from .. import serializers, models
from ..utils import exec
from .._serializers import profile_serializers


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
    if not request.user.is_superuser:
      return Response({"detail": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    profiles = models.Profile.objects.all()
    serializer = serializers.ProfileSerializer(profiles, many=True)
    return Response(
      {
        "detail": "hello admin",
        "profile_count": profiles.count(),
        "profiles": serializer.data
      }, status=status.HTTP_200_OK
    )
    
  
  def create(self, request):
    """ register for an account """
    data = request.data
    password = data["password"]
    repeated_password = data["repeated_password"]

    if password != repeated_password:
      return Response({"detail": "your passwords don't match"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      user = models.Profile.objects.create(name=data["name"], email=data["email"], password=make_password(data["password"]))
      serializer = serializers.ProfileSerializer(user, many=False)
      return Response(serializer.data)
    except:
      return Response({"detail": "profile with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    

  def retrieve(self, request, pk=None):
    """ get a profile """
    try:
      profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response({"detail": "profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    exec.only_admin_and_user(profile.id, request)
    serializer = serializers.ProfileSerializer(profile, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)
  

  def update(self, request, pk=None):
    profile = request.user
    field_serializer = profile_serializers.UpdateProfileSerializer(data=request.data)
    if field_serializer.is_valid(raise_exception=True):
      try:
        profile = models.Profile.objects.get(pk=pk)
      except ObjectDoesNotExist:
        return Response({"detail": "Profile doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)

      if "name" in request.data:
        profile.name = field_serializer.validated_data["name"]
      if "city" in request.data:
        profile.city = field_serializer.validated_data["state"]
      if "state" in request.data:
        profile.state = field_serializer.validated_data["state"]
      if "graduation_year" in request.data:
        profile.graduation_year = field_serializer.validated_data["graduation_year"]
      if "major" in request.data:
        profile.major = field_serializer.validated_data["major"]
      if "interests" in request.data:
        profile.interests = field_serializer.validated_data["interests"]
      profile.save()

      # prompts_data = field_serializer.validated_data.get("prompt_set", [])
      # quotes_data = field_serializer.validated_data.get("quote_set", [])
      # links_data = field_serializer.validated_data.get("link_set", [])

      # prompts_serializer = serializers.UpdatePromptSerializer(data=prompts_data, many=True)
      # quotes_serializer = serializers.UpdateQuoteSerializer(data=quotes_data, many=True)
      # links_serializer = serializers.UpdateLinkSerializer(data=links_data, many=True)

      # if not all([prompts_serializer.is_valid(), quotes_serializer.is_valid(), links_serializer.is_valid()]):
      #   return Response({
      #     'prompts_errors': prompts_serializer.errors,
      #     'quotes_errors': quotes_serializer.errors,
      #     'links_errors': links_serializer.errors,
      #   }, status=status.HTTP_400_BAD_REQUEST)

      # prompts_serializer.save(profile=profile)
      # quotes_serializer.save(profile=profile)
      # links_serializer.save(profile=profile)
    else:
      return Response({'detail': 'Update profile failed.'}, status=status.HTTP_400_BAD_REQUEST)
  
    profile_serializer = profile_serializers.ProfileSerializer(profile, many=False)
    return Response(profile_serializer.data)
  

  def destroy(self, request, pk=None):
    """ delete a profile """
    try:
      profile = models.Profile.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response({"detail": "Profile does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    exec.only_admin_and_user(profile.id, request)
    profile.delete()
    return Response({"detail": "profile deleted successfully."}, status=status.HTTP_200_OK)
  

  @action(detail=False, methods=["post"], url_path=r"actions/upload-thumbnail")
  def upload_thumbnail(self, request):
    profile = request.user

    fields_serializer = serializers.UploadThumbnailSerializer(data=request.data)
    if fields_serializer.is_valid():
      profile.thumbnail = fields_serializer.validated_data["thumbnail"]
      profile.save()

    profile_serializer = serializers.ProfileSerializer(profile)
    return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
  

  @action(detail=False, methods=["post"], url_path=r"actions/create-profile")
  def create_profile(self, request):
    # NOTE: This will create everything but thumbnail and photos
    # That will be handled in two separate views: thumbnail in ProfileViewSet 
    # photos in PhotoViewSet. This way I can separate request data as raw json and multipart.
    # Really not sure why I'm having a problem with posting it all as multipart data, but the
    # problem persists and I'd rather make two requests one user's creating profiles than 
    # figuring out why this is. On submitted raw json, the request works (this is without submitting
    # files). Once I try to submit multipart data with nested objects such as the links, quotes, and prompts
    # I get an error telling me the fields of these models must be set although they are.
    # Will separate this into two endpoints now.
    profile = request.user
    fields_serializer = serializers.CreateProfileSerializer(data=request.data)
    fields_serializer.is_valid(raise_exception=True)
  
    # Save profile fields
    profile.birthday = fields_serializer.validated_data["birthday"]
    profile.sex = fields_serializer.validated_data["sex"]
    profile.city = fields_serializer.validated_data["city"]
    profile.state = fields_serializer.validated_data["state"]
    profile.graduation_year = fields_serializer.validated_data["graduation_year"]
    profile.major = fields_serializer.validated_data["major"]
    profile.interests = fields_serializer.validated_data["interests"]
    profile.dorm_building = fields_serializer.validated_data["dorm_building"]
    profile.has_account = True
    profile.save()

    # Save related objects
    prompts_data = fields_serializer.validated_data.get("prompt_set", [])
    quotes_data = fields_serializer.validated_data.get("quote_set", [])
    links_data = fields_serializer.validated_data.get("link_set", [])

    prompts_serializer = serializers.CreatePromptSerializer(data=prompts_data, many=True)
    quotes_serializer = serializers.CreateQuoteSerializer(data=quotes_data, many=True)
    links_serializer = serializers.CreateLinkSerializer(data=links_data, many=True)

    if not all([prompts_serializer.is_valid(), quotes_serializer.is_valid(), links_serializer.is_valid()]):
        return Response({
            'prompts_errors': prompts_serializer.errors,
            'quotes_errors': quotes_serializer.errors,
            'links_errors': links_serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    prompts_serializer.save(profile=profile)
    quotes_serializer.save(profile=profile)
    links_serializer.save(profile=profile)

    profile_serializer = serializers.ProfileSerializer(profile)
    return Response(profile_serializer.data, status=status.HTTP_201_CREATED)


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
  

  @action(detail=False, methods=["get"], url_path=r"actions/get-blocked-profiles")
  def get_blocked_profiles(self, request):
    """ get all blocked profiles """
    current_profile = request.user
    blocked_profiles = current_profile.blocked_profiles.all()
    serializer = serializers.SwipeProfileSerializer(blocked_profiles, many=True)
    return Response({"count": blocked_profiles.count(), "results": serializer.data})

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
  

class PhotoViewSet(ModelViewSet):
  serializer_class = serializers.PhotoSerializer
  permission_classes = [IsAuthenticated]
  parser_classes = (MultiPartParser, FormParser,)

  def get_serializer(self, *args, **kwargs):
    # add many=True if the data is of type list
    if isinstance(kwargs.get("data", {}), list):
      kwargs["many"] = True

    return super(PhotoViewSet, self).get_serializer(*args, **kwargs)

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
    def modify_input_for_multiple_files(image):
      dict = {}
      dict['image'] = image
      return dict

    profile = request.user
    profile_photos = models.Photo.objects.filter(profile=profile.id)

    images = dict((request.data).lists())['image']

    if len(profile_photos) + len(images) > 4:
      return Response({"detail": "Profile cannot have more than 4 images"}, status=status.HTTP_400_BAD_REQUEST)

    for image in images:
      modified_data = modify_input_for_multiple_files(image)
      file_serializer = serializers.CreatePhotoSerializer(data=modified_data)
      if file_serializer.is_valid():
        models.Photo.objects.create(
          profile=profile, image=image
        )

      else:
        return Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'detail': 'Photos upload successfully.'}, status=status.HTTP_201_CREATED)
  


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
    return Response({"detail": "photo deleted"}, status=status.HTTP_200_OK)