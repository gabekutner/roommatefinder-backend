""" roommatefinder/apps/api/internal/internal_profiles.py """
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .. import serializers, models


@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_profiles(request):
  """ List all profiles. """
  profiles = models.Profile.objects.all()
  serializer = serializers.ProfileSerializer(profiles, many=True)
  return Response(
    {"count": len(serializer.data), "results": serializer.data}, status=status.HTTP_200_OK,
  )

@api_view(["POST"])
@permission_classes([IsAdminUser])
def delete_profile(request, pk):
  """ Delete a profile by id. """
  try:
    profile = models.Profile.objects.get(pk=pk)
  except ObjectDoesNotExist:
    return Response(
      {"detail": f"Profile with id {pk} does not exist."}, status=status.HTTP_400_BAD_REQUEST
    )
  profile.delete()
  return Response(
    {"detail": "success"}, status=status.HTTP_200_OK
  )