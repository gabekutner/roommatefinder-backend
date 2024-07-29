from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from .. import models, views

class TestProfileModelViewSet(TestCase):
    """Test ProfileModelViewSet"""

    def setUp(self):
        """Setup for the tests"""
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