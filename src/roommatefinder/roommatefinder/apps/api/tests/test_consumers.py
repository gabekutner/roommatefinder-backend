from django.test import TestCase
from channels.testing import WebsocketCommunicator
# from roommatefinder.asgi import application
from roommatefinder.apps.api import models
from roommatefinder.apps.api import consumers


class TestAPIConsumer(TestCase):
  """ Test Websocket Consumer """
  def setUp(self):
    """Setup for the tests"""
    self.user = models.Profile.objects.create(identifier="gabe", otp_verified=True)

  async def test_websocket_connect(self):
    # Create a WebSocket communicator
    communicator = WebsocketCommunicator(
      consumers.APIConsumer.as_asgi(),
      'chat/',
    )
    communicator.scope['user'] = self.user
    # Send a connect request and check the response
    connected, subprotocol = await communicator.connect()
    self.assertTrue(connected)