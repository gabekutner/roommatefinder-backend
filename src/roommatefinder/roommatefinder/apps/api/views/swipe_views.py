""" roommatefinder/apps/api/views/swipe_views.py """
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.measure import D
from django.db.models import Q
from itertools import chain

from .. import models, serializers



class SwipeModelViewSet(ModelViewSet):
  permission_classes = [IsAuthenticated]

  def list(self, request): 
    """ list home page cards """
    current_profile = request.user
    profiles = models.Profile.objects.all().filter(has_account=True)

    if not current_profile.age:
      return Response(
        {"details": "You need an account to perform this action"},
        status=status.HTTP_401_UNAUTHORIZED,
      )
    
    profiles_serializer = serializers.SwipeProfileSerializer(profiles, many=True)
    print(profiles_serializer)
    return Response(
      {
        "count": len(profiles),
        "profile_count": profiles.count(),
        "results": profiles_serializer.data,
      }
    )