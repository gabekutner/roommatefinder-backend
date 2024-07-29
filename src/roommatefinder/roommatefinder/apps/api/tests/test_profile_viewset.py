import unittest
from rest_framework.test import APIRequestFactory, force_authenticate
from .. import models, views


class TestProfileModelViewSet(unittest.TestCase):
  """ Test ProfileModelViewSet """
  def __init__(self, *args, **kwargs):
    super(TestProfileModelViewSet, self).__init__(*args, **kwargs)
    self.factory = APIRequestFactory()
    # self.authed_user = models.Profile.objects.get(identifier="gabekutner")
    # self.unauthed_user = models.Profile.objects.get(identifier="4153213")

  def test_list_unauthed(self):
    profile = models.Profile(identifier="gabe")
    profile.save()
    # view = views.profile_views.ProfileViewSet.as_view({'get': 'list'})
    # request = self.factory.get("/")
    # force_authenticate(request, user=profile)
    # response = view(request)
    # assert response.status_code == 401

  # def test_list_authed(self):
  #   view = views.profile_views.ProfileViewSet.as_view({'get': 'list'})
  #   request = self.factory.get("/")
  #   force_authenticate(request, user=self.authed_user)
  #   response = view(request)
  #   assert response.status_code == 200