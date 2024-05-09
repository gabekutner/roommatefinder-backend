import json
import base64
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile

from . import models


class ChatConsumer(WebsocketConsumer):

  def connect(self):
    user = self.scope['user']
    print(user, user.is_authenticated)
    if not user.is_authenticated:
      return
    
    # self.email = user.email
    # async_to_sync(self.channel_layer.group_add)(
		# 	self.email, self.channel_name
		# )
    self.accept()


  def disconnect(self, close_code):
		# Leave room/group
    # async_to_sync(self.channel_layer.group_discard)(
		# 	self.email, self.channel_name
		# )
    pass
		

  # handle requests --------------------------
  # def receive(self, text_data):
  #   # receive message from websocket
  #   data = json.loads(text_data)
  #   data_source = data.get('source')

  #   print('receive ', json.dumps(data, indent=2))

  #   # thumbnail upload
  #   if data_source == 'thumbnail':
  #     self.receive_thumbnail(data)

  # def receive_thumbnail(self, data):
  #   user = self.scope['user']
  #   # Convert base64 data  to django content file
  #   image_str = data.get('base64')
  #   image = ContentFile(base64.b64decode(image_str))
  #   # Update thumbnail field
  #   filename = data.get('filename')
  #   user.thumbnail.save(filename, image, save=True)
  #   # Serialize user
  #   # serialized = UserSerializer(user)
  #   # Send updated user data including new thumbnail 
  #   self.send_group(self.email, 'thumbnail', user)

  
  # # catch websocket broadcasts
  # def send_group(self, group, source, data):
  #   response = {
  #     'type': 'broadcast_group',
  #     'source': source,
  #     'data': data 
  #   }
  #   async_to_sync(self.channel_layer.group_send(
  #     group, response
  #   ))

  # def broadcast_group(self, data):
  #   data.pop('type')
  #   self.send(text_data=json.dumps(data))