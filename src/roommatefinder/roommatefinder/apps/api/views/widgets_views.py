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
  
  def create(self, request):
    """ create a link """
    profile = request.user
    field_serializer = extra_serializers.CreateLinkSerializer(data=request.data)
    if not field_serializer.is_valid():
      return Response({ 'links_errors': field_serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
    
    field_serializer.save(profile=profile)
    profile_serializer = profile_serializers.ProfileSerializer(profile)
    return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
  
  def destroy(self, request, pk=None):
    """ delete link """
    try:
      link = models.Link.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response({"detail": "link does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    link.delete()
    profile_serializer = profile_serializers.ProfileSerializer(request.user)
    return Response(profile_serializer.data, status=status.HTTP_200_OK)
  

class PromptViewSet(ModelViewSet):
  queryset = models.Prompt.objects.all()
  serializer_class = extra_serializers.PromptSerializer
  permission_classes = [IsAuthenticated]
  
  def create(self, request):
    """ create a prompt """
    profile = request.user
    field_serializer = extra_serializers.CreatePromptSerializer(data=request.data)
    if not field_serializer.is_valid():
      return Response({ 'prompts_errors': field_serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
    
    field_serializer.save(profile=profile)
    profile_serializer = profile_serializers.ProfileSerializer(profile)
    return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
  
  def destroy(self, request, pk=None):
    """ delete prompt """
    try:
      prompt = models.Prompt.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response({"detail": "prompt does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    prompt.delete()
    profile_serializer = profile_serializers.ProfileSerializer(request.user)
    return Response(profile_serializer.data, status=status.HTTP_200_OK)
  

class QuoteViewSet(ModelViewSet):
  queryset = models.Quote.objects.all()
  serializer_class = extra_serializers.QuoteSerializer
  permission_classes = [IsAuthenticated]
  
  def create(self, request):
    """ create a quote """
    profile = request.user
    field_serializer = extra_serializers.CreateQuoteSerializer(data=request.data)
    if not field_serializer.is_valid():
      return Response({ 'quotes_errors': field_serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
    
    field_serializer.save(profile=profile)
    profile_serializer = profile_serializers.ProfileSerializer(profile)
    return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
  
  def destroy(self, request, pk=None):
    """ delete quote """
    try:
      quote = models.Quote.objects.get(pk=pk)
    except ObjectDoesNotExist:
      return Response({"detail": "quote does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    quote.delete()
    profile_serializer = profile_serializers.ProfileSerializer(request.user)
    return Response(profile_serializer.data, status=status.HTTP_200_OK)