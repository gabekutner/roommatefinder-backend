from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes


from .. import models, serializers
from ..handlers.rank import rank_profiles
from ..pagination import StandardResultsSetPagination


class SwipeModelViewSet(ListAPIView):
  # queryset = models.Profile.objects.all()
  pagination_class = StandardResultsSetPagination
  serializer_class = serializers.SwipeProfileSerializer

  def get_queryset(self):
    return models.Profile.objects.all().exclude(id=self.request.user.id)

@api_view(["get"])
@permission_classes([IsAuthenticated])
def get_swipe_profile(request, pk):
  """ get one swipe profile """
  profile = models.Profile.objects.get(pk=pk)
  serializer = serializers.SwipeProfileSerializer(profile, many=False)
  return Response(serializer.data, status=status.HTTP_200_OK)