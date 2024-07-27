import string
import random

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password

from .. import models
from ..serializers import profile_serializers


@api_view(["get"])
@permission_classes([IsAdminUser])
def list_profiles(request):
  """ List all profiles. """
  profiles = models.Profile.objects.all()
  serializer = profile_serializers.ProfileSerializer(profiles, many=True)
  return Response(
    {
      "count": len(serializer.data), 
      "results": serializer.data
    }, 
    status=status.HTTP_200_OK,
  )

@api_view(["post"])
@permission_classes([IsAdminUser])
def fake_create_profiles(request):
  """Create a 5 fake profiles. """
  N = 7
  PASSWORD = make_password("123")
  SEX = "M"
  AGE = 19

  for i in range(5):
    profile = {
      "identifier": "".join(random.choices(string.ascii_uppercase + string.digits, k=N)),
      "password": PASSWORD,
      "name": "".join(random.choices(string.ascii_uppercase + string.digits, k=N)),
      "sex": SEX,
      "age": AGE,
      "dorm_building": str(random.randint(1, 10)),
    }  
    models.Profile.objects.create(
      identifier=profile["identifier"],
      password=profile["password"],
      name=profile["name"],
      sex=profile["sex"],
      age=profile["age"],
      dorm_building=profile["dorm_building"],
      has_account=True,
      otp_verified=True
    )

  return Response({"detail": "great success"}, status=status.HTTP_201_CREATED)


@api_view(["post"])
@permission_classes([IsAdminUser])
def delete_profile(request, pk):
  """ Delete a profile by id. """
  try:
    profile = models.Profile.objects.get(pk=pk)
  except ObjectDoesNotExist:
    return Response(
      {"detail": f"Profile: {pk} doesn't exist."}, status=status.HTTP_400_BAD_REQUEST
    )
  profile.delete()
  return Response(
    {"detail": "success"}, 
    status=status.HTTP_200_OK
  )

