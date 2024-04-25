""" roommatefinder/apps/api/views/swipe_views.py """
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .. import models, serializers
from ..handlers.rank import rank_profiles


class SwipeModelViewSet(ModelViewSet):
  permission_classes = [IsAuthenticated]

  def list(self, request): 
    """ list home page cards """
    current_profile = request.user
    profiles = models.Profile.objects.all().filter(has_account=True).exclude(id=current_profile.id)

    if not current_profile.age:
      return Response(
        {"details": "You need an account to perform this action"},
        status=status.HTTP_401_UNAUTHORIZED,
      )
    
    # filters go here
    show_profiles = rank_profiles(current_profile, profiles)

    profiles_serializer = serializers.SwipeProfileSerializer(show_profiles, many=True)
    return Response(
      {
        "count": len(show_profiles),
        "profile_count": show_profiles.count(),
        "results": profiles_serializer.data,
      }
    )
  
  def retrieve(self, request, pk=None):
    profile = models.Profile.objects.get(pk=pk)
    serializer = serializers.SwipeProfileSerializer(profile, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)