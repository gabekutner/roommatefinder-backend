from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from roommatefinder.apps.api import models, views


class TestProfileModelViewSet(TestCase):
    """ Test ProfileModelViewSet """
    def setUp(self):
      """ Setup for the tests """
      self.factory = APIRequestFactory()
      self.unauthed_user = models.Profile.objects.create(identifier="dave", is_superuser=False, otp_verified=True)
      self.authed_user = models.Profile.objects.create(identifier="gabe", is_superuser=True, otp_verified=True)

    def test_list_unauthed(self):
      """ Test listing profiles without authentication """
      request = self.factory.get("/")
      view = views.profile_views.ProfileViewSet.as_view({'get': 'list'})
      force_authenticate(request, user=self.unauthed_user)
      response = view(request)
      self.assertEqual(response.status_code, 401)
    
    def test_list_authed(self):
      """ Test listing profiles with authentication """
      request = self.factory.get("/")
      view = views.profile_views.ProfileViewSet.as_view({'get': 'list'})
      force_authenticate(request, user=self.authed_user)
      response = view(request)
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.data['profile_count'], 2)

    def test_create(self):
      """ Test creating a profile """
      request = self.factory.post('/api/v1/profiles/', {'identifier': '123'}, format='json')
      view = views.profile_views.ProfileViewSet.as_view({'post': 'create'})
      response = view(request)
      self.assertEqual(response.status_code, 201)
      self.assertEqual(response.data['identifier'], '123')

    def test_create_identifier_that_already_exists(self):
      """ Test creating a profile with an identifier that already exists. """
      models.Profile.objects.create(identifier="123", otp_verified=True)
      request = self.factory.post('/api/v1/profiles/', {'identifier': '123'}, format='json')
      view = views.profile_views.ProfileViewSet.as_view({'post': 'create'})
      response = view(request)
      self.assertEqual(response.status_code, 400)

    