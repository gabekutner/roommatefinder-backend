from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

from roommatefinder.apps.api import models
from roommatefinder.apps.api.serializers import photo_serializers


class TestPhotoViewSet(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = models.Profile.objects.create_user(identifier='u1234567', password='testpassword')
    self.client.force_authenticate(user=self.user)

    # Create initial photo
    self.photo = models.Photo.objects.create(
        profile=self.user,
        image=SimpleUploadedFile(name='test_image.jpg', content=b'file_content', content_type='image/jpeg')
    )
    self.photo_url = f'/api/v1/photos/{self.photo.id}/'

  def test_list_photos(self):
    response = self.client.get('/api/v1/photos/')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(len(response.data), 1)
    self.assertEqual(response.data[0]['id'], str(self.photo.id))

  def test_retrieve_photo(self):
    response = self.client.get(self.photo_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['id'], str(self.photo.id))

  def test_delete_photo(self):
    response = self.client.delete(self.photo_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['detail'], 'photo deleted')
    self.assertFalse(models.Photo.objects.filter(id=self.photo.id).exists())