# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from roommatefinder.apps.api import models
from roommatefinder.apps.api.serializers import photo_serializers, profile_serializers


class PhotoViewSet(ModelViewSet):
  serializer_class = photo_serializers.PhotoSerializer
  permission_classes = [IsAuthenticated]
  parser_classes = (MultiPartParser, FormParser,)

  def get_serializer(self, *args, **kwargs):
    # add many=True if the data is of type list
    if isinstance(kwargs.get("data", {}), list):
      kwargs["many"] = True
    return super(PhotoViewSet, self).get_serializer(*args, **kwargs)


  def list(self, request):
    """ list photos """
    profile = request.user
    queryset = models.Photo.objects.filter(profile=profile.id).order_by("created")
    serializer = photo_serializers.PhotoSerializer(queryset, many=True)
    return Response(serializer.data)


  def retrieve(self, request, pk):
    """ get a photo """
    photo = models.Photo.objects.get(pk=pk)
    serializer = photo_serializers.PhotoSerializer(photo, many=False)
    return Response(serializer.data)


  def create(self, request):
    """ create photo(s) """
    def modify_input_for_multiple_files(image):
      dict = {}
      dict['image'] = image
      return dict

    profile = request.user
    profile_photos = models.Photo.objects.filter(profile=profile.id)
    images = dict((request.data).lists())['image']

    if len(profile_photos) + len(images) > 5:
      return Response({"detail": "profile cannot have more than 5 images"}, status=status.HTTP_400_BAD_REQUEST)

    for image in images:
      modified_data = modify_input_for_multiple_files(image)
      file_serializer = photo_serializers.CreatePhotoSerializer(data=modified_data)
      if file_serializer.is_valid():
        models.Photo.objects.create(
          profile=profile, image=image
        )
      else:
        return Response({"detail": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)
      
    # return as profile serializer
    profile_serializer = profile_serializers.ProfileSerializer(profile, many=False)
    return Response(profile_serializer.data, status=status.HTTP_201_CREATED)


  def update(self, request, pk=None, *args, **kwargs):
    """ update photo """
    photo = models.Photo.objects.get(pk=pk)
    fields_serializer = photo_serializers.PhotoSerializer(data=request.data, partial=True)
    fields_serializer.is_valid(raise_exception=True)
    photo.image = fields_serializer.validated_data["image"]

    photo.save()
    serializer = photo_serializers.PhotoSerializer(photo, many=False)
    return Response(serializer.data)


  def destroy(self, request, pk):
    """ delete photo """
    photo = models.Photo.objects.get(pk=pk)
    photo.delete()
    return Response({"detail": "photo deleted"}, status=status.HTTP_200_OK)