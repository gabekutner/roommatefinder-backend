from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes

from .. import models, serializers
from ..handlers import swipe_filters
# from ..handlers.rank import as
# from api.handlers.swipe_filters
from ..pagination import StandardResultsSetPagination


class SwipeModelViewSet(ListAPIView):
  """ get swipe profiles """
  pagination_class = StandardResultsSetPagination
  serializer_class = serializers.SwipeProfileSerializer

  def get_queryset(self):
    """ get swipe queryset - exclude self, connections & rank """
    profiles = models.Profile.objects.filter(has_account=True)
    blocked_profiles = self.request.user.blocked_profiles.all()
    connections = models.Connection.objects.filter(
      Q(sender=self.request.user.id) | Q(receiver=self.request.user.id),
      accepted=True
    )

    excluded_ids = connections.values_list('sender', 'receiver')
    blocked_ids = blocked_profiles.values_list('id')

    excluded_ids = set([id for sublist in excluded_ids for id in sublist])
    blocked_ids = set([id for sublist in blocked_ids for id in sublist])

    excluded_ids = excluded_ids.union(blocked_ids)

    if not bool(excluded_ids):
      excluded_ids = set([self.request.user.id])

    profiles = profiles.exclude(
      id__in=excluded_ids
    )
    return profiles

class SwipeDetailView(RetrieveAPIView):
  queryset = models.Profile.objects.all()
  serializer_class = serializers.SwipeProfileSerializer