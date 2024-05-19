from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from .. import models, serializers
from ..handlers.rank import rank_profiles
from ..pagination import StandardResultsSetPagination


class SwipeModelViewSet(ListAPIView):
  # permission_classes = [IsAuthenticated]
  queryset = models.Profile.objects.all()
  pagination_class = StandardResultsSetPagination
  serializer_class = serializers.SwipeProfileSerializer

  # def list(self, request): 
  #   """ list swipe cards """
  #   current_profile = request.user
  #   profiles = models.Profile.objects.all().filter(has_account=True).exclude(id=current_profile.id)

  #   if not current_profile.age:
  #     return Response(
  #       {"details": "You need an account to perform this action"},
  #       status=status.HTTP_401_UNAUTHORIZED,
  #     )
    
  #   # filters go here
  #   # show_profiles = rank_profiles(current_profile, profiles)

  #   profiles_serializer = serializers.SwipeProfileSerializer(profiles, many=True)
  #   return Response(
  #     {
  #       "count": len(profiles),
  #       "profile_count": profiles.count(),
  #       "results": profiles_serializer.data,
  #     }
  #   )
  
  # def retrieve(self, request, pk=None):
  #   profile = models.Profile.objects.get(pk=pk)
  #   serializer = serializers.SwipeProfileSerializer(profile, many=False)
  #   return Response(serializer.data, status=status.HTTP_200_OK)