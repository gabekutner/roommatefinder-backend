# -*- coding: utf-8 -*-
from django.test import TestCase
from channels.testing import WebsocketCommunicator
from roommatefinder.apps.api import models
from roommatefinder.apps.api import consumers


class TestAPIConsumer(TestCase):
  """
  Test case for the WebSocket API consumer.

  This test class uses Django's TestCase to test the WebSocket consumer's functionality. 
  """
  def setUp(self):
    self.user = models.Profile.objects.create(identifier="sender", otp_verified=True)
    
  async def test_websocket_connect(self):
    """
    Tests the WebSocket connection establishment.

    This asynchronous test method:
    - Creates a WebSocket communicator for the `APIConsumer`.
    - Sets the scope to include the test user.
    - Sends a WebSocket connection request.
    - Asserts that the connection is successful.

    Raises:
      AssertionError: If the WebSocket connection is not established successfully.
    """
    communicator = WebsocketCommunicator(
      consumers.APIConsumer.as_asgi(),
      'chat/',
    )
    communicator.scope['user'] = self.user
    # Send a connect request and check the response
    connected, _ = await communicator.connect()
    self.assertTrue(connected)