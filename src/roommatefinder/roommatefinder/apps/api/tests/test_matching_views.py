from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from roommatefinder.apps.api import models, views


class TestMatchingViews(TestCase):
  """ Test ProfileModelViewSet """
  def setUp(self):
    """ Setup for the tests """
    self.factory = APIRequestFactory()
    self.user = models.Profile.objects.create(identifier="dave", is_superuser=False, otp_verified=True)
    self.superuser = models.Profile.objects.create(identifier="gabe", is_superuser=True, otp_verified=True)
  
  def test_list_auth(self):
    request = self.factory.get("/")
    view = views.matching_views.RoommateQuizViewSet.as_view({'get': 'list'})
    force_authenticate(request, user=self.superuser)
    response = view(request)
    self.assertEqual(response.status_code, 200)
  
  def test_list_unauth(self):
    request = self.factory.get("/")
    view = views.matching_views.RoommateQuizViewSet.as_view({'get': 'list'})
    response = view(request)
    self.assertEqual(response.status_code, 401)

  def test_create_auth(self):
    request = self.factory.post(
      "/",
      {
        "social_battery": 15,
        "clean_room": "1",
        "noise_level": 15,
        "guest_policy": "2",
        "in_room": 14,
        "hot_cold": 14,
        "bed_time": "4",
        "wake_up_time": "4",
        "sharing_policy": "4"
      },
      format="json",
    )
    view = views.matching_views.RoommateQuizViewSet.as_view({'post': 'create'})
    force_authenticate(request, user=self.superuser)
    response = view(request)
    self.assertEqual(response.status_code, 201)
  
  def test_create_unauth(self):
    request = self.factory.post(
      "/",
      {
        "social_battery": 15,
        "clean_room": "1",
        "noise_level": 15,
        "guest_policy": "2",
        "in_room": 14,
        "hot_cold": 14,
        "bed_time": "4",
        "wake_up_time": "4",
        "sharing_policy": "4"
      },
      format="json",
    )
    view = views.matching_views.RoommateQuizViewSet.as_view({'post': 'create'})
    response = view(request)
    self.assertEqual(response.status_code, 401)

  def test_create_missing_values(self):
    request = self.factory.post(
      "/",
      {
        "social_battery": 15,
      },
      format="json",
    )
    view = views.matching_views.RoommateQuizViewSet.as_view({'post': 'create'})
    force_authenticate(request, user=self.superuser)
    response = view(request)
    self.assertEqual(response.status_code, 400)