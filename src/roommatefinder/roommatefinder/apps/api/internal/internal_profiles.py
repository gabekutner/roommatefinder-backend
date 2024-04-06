""" Admin actions - profile """
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

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