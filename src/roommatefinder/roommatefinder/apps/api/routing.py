from django.urls import path
from . import consumers

websocket_urlpatterns = [
  path('chat/', consumers.APIConsumer.as_asgi()),
]