from django.test import TestCase
from rest_framework.test import APIRequestFactory
from . import models, views

class TestProfileModelViewSet(TestCase):
    """Test ProfileModelViewSet"""

    def setUp(self):
        """Setup for the tests"""
        self.factory = APIRequestFactory()
        self.profile = models.Profile.objects.create(identifier="gabe")

    def test_list_unauthed(self):
        """Test listing profiles without authentication"""
        response = views.ProfileViewSet.as_view({'get': 'list'})
        self.assertEqual(response.status_code, 200)
        # Add more assertions as needed