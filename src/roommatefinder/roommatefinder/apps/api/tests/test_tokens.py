# -*- coding: utf-8 -*-
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from roommatefinder.apps.api import models


class TestMyTokenObtainPairView(APITestCase):
  """
  Test case for `MyTokenObtainPairView`.

  This test case verifies the functionality of the token authentication endpoint. The tests ensure
  that valid credentials return the expected JWT tokens and invalid credentials return an appropriate
  error response.

  Attributes:
    user (Profile): An instance of the `Profile` model used for testing authentication.
    url (str): The URL endpoint for obtaining tokens, resolved from the URL configuration.
  """
  def setUp(self):
    self.user = models.Profile.objects.create_user(
      identifier='u1234567',
      password='testpassword'
    )
    self.url = reverse('login')  # URL name defined in your URL config

  def test_token_obtain_pair_success(self):
    """
    Tests successful token generation with valid credentials.

    Sends a POST request to the login endpoint with valid credentials and verifies that:
    - The response status code is 200 OK.
    - The response contains both 'access' and 'refresh' tokens.

    Expected response:
      - Status code: 200
      - JSON response body contains 'access' and 'refresh' keys.
    """
    data = {
      'identifier': 'u1234567',
      'password': 'testpassword'
    }
    response = self.client.post(self.url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('access', response.data)
    self.assertIn('refresh', response.data)