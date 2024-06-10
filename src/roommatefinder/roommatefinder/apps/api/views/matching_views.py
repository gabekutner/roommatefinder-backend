from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .. import models
from .._serializers.matching_serializers import RoommateQuizSerializer, CreateRoommateQuizSerializer


class RoommateQuizViewSet(ModelViewSet):
  queryset = models.RoommateQuiz.objects.all()
  serializer_class = RoommateQuizSerializer

  def list(self, request):
    serializer = RoommateQuizSerializer(self.queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def retrieve(self, request, pk=None):
    quiz = self.queryset.filter(profile=pk)
    serializer = RoommateQuizSerializer(quiz, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
  def create(self, request):
    profile = request.user
    fields_serializer = CreateRoommateQuizSerializer(data=request.data)
    if fields_serializer.is_valid():
      quiz = models.RoommateQuiz.objects.create(
        profile=profile, **fields_serializer.validated_data
      )
    else:
      return Response({'detail': 'Create roommate matching quiz failed.'}, status=status.HTTP_400_BAD_REQUEST)
    
    matching_serializer = RoommateQuizSerializer(quiz)
    return Response(matching_serializer.data, status=status.HTTP_201_CREATED)

  def update(self, request, pk=None):
    pass

  def destory(self, request):
    pass