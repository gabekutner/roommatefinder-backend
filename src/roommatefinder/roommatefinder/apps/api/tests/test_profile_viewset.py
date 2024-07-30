# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from roommatefinder.apps.api import models, views


class TestProfileModelViewSet(TestCase):
  """ Test ProfileModelViewSet """
  def setUp(self):
    """ Setup for the tests """
    self.factory = APIRequestFactory()
      # bad naming

    self.unauthed_user = models.Profile.objects.create(identifier="dave", is_superuser=False, otp_verified=True)
    self.authed_user = models.Profile.objects.create(identifier="gabe", is_superuser=True, otp_verified=True)

  # bad naming

  def test_list_unauthed(self):
    """ Test listing profiles without authentication """
    request = self.factory.get("/")
    view = views.profile_views.ProfileViewSet.as_view({'get': 'list'})
    force_authenticate(request, user=self.unauthed_user)
    response = view(request)
    self.assertEqual(response.status_code, 403)
  
  # bad naming
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
    request = self.factory.post('/api/v1/profiles/', {'identifier': 'u1234567'}, format='json')
    view = views.profile_views.ProfileViewSet.as_view({'post': 'create'})
    response = view(request)
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response.data['identifier'], 'u1234567')

  def test_create_identifier_that_already_exists(self):
    """ Test creating a profile with an identifier that already exists. """
    models.Profile.objects.create(identifier="u1234567", otp_verified=True)
    request = self.factory.post('/api/v1/profiles/', {'identifier': 'u1234567'}, format='json')
    view = views.profile_views.ProfileViewSet.as_view({'post': 'create'})
    response = view(request)
    self.assertEqual(response.status_code, 400)

  def test_verify_otp(self):
    profile = models.Profile.objects.create(identifier="u1234567")
    request = self.factory.post('/api/v1/profiles/actions/verify-otp/', {'otp': str(profile.otp)}, format='json')
    view = views.profile_views.ProfileViewSet.as_view({'post': 'verify_otp'})
    force_authenticate(request, user=profile)
    response = view(request)
    self.assertEqual(response.status_code, 200)

  def test_verify_otp_wrong(self):
    profile = models.Profile.objects.create(identifier="123")
    # will 100% be wrong, otp codes are 4-digits
    request = self.factory.post('/api/v1/profiles/actions/verify-otp/', {'otp': '123'}, format='json')
    view = views.profile_views.ProfileViewSet.as_view({'post': 'verify_otp'})
    force_authenticate(request, user=profile)
    response = view(request)
    self.assertEqual(response.status_code, 400)

  def test_create_passwords(self):
    profile = models.Profile.objects.create(identifier="123", otp_verified=True)
    request = self.factory.post(
      '/api/v1/profiles/actions/create-password/', 
      {
        'password': '123',
        'repeated_password': '123'
      }, 
      format='json'
    )
    view = views.profile_views.ProfileViewSet.as_view({'post': 'create_password'})
    force_authenticate(request, user=profile)
    response = view(request)
    self.assertEqual(response.status_code, 200)

  def test_create_passwords_with_two_different_passwords(self):
    profile = models.Profile.objects.create(identifier="123", otp_verified=True)
    request = self.factory.post(
      '/api/v1/profiles/actions/create-password/', 
      {
        'password': '123',
        'repeated_password': '1234'
      }, 
      format='json'
    )
    view = views.profile_views.ProfileViewSet.as_view({'post': 'create_password'})
    force_authenticate(request, user=profile)
    response = view(request)
    self.assertEqual(response.status_code, 400)

  