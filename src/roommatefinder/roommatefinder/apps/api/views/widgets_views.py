from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .. import models
from ..serializers import extra_serializers, profile_serializers


class LinkViewSet(ModelViewSet):
  queryset = models.Link.objects.all()
  serializer_class = extra_serializers.LinkSerializer
  permission_classes = [IsAuthenticated]

  def list(self, request):
    pass

  def retrieve(self, request, *args, **kwargs):
    return super().retrieve(request, *args, **kwargs)
  
  def create(self, request, *args, **kwargs):
    return super().create(request, *args, **kwargs)
  
  def update(self, request, *args, **kwargs):
    return super().update(request, *args, **kwargs)
  
  def destroy(self, request, pk=None):
    """ delete link """
    try:
      link = models.Link.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response({"detail": "profile does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    link.delete()
    profile_serializer = profile_serializers.ProfileSerializer(request.user)
    return Response(profile_serializer.data, status=status.HTTP_200_OK)