import json
import uuid
import base64
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from django.db.models import Q, Exists, OuterRef

from . import models
from . import serializers


class ChatConsumer(WebsocketConsumer):

  def connect(self):
    user = self.scope['user']
    print(user, user.is_authenticated)
    if not user.is_authenticated:
      return

    self._id = user.id
    self.id = str(user.email).split('@')[0]
    # join this user to a group by their email
    async_to_sync(self.channel_layer.group_add)(
			self.id, self.channel_name
		)
    self.accept()


  def disconnect(self, close_code):
		# Leave room/group
    async_to_sync(self.channel_layer.group_discard)(
			self.id, self.channel_name
		)
		

  #----------------------
	#   Handle Requests
	#----------------------
  def receive(self, text_data):
    # receive message from websocket
    data = json.loads(text_data)
    data_source = data.get('source')

    print('receive ', json.dumps(data, indent=2))

    # Search / filter users
    if data_source == 'search':
      self.receive_search(data)

    # Make friend request
    elif data_source == 'request.connect':
      self.receive_request_connect(data)

    # Accept friend request
    elif data_source == 'request.accept':
      self.receive_request_accept(data)

    # Get request list
    elif data_source == 'request.list':
      self.receive_request_list(data)

    # thumbnail upload
    elif data_source == 'thumbnail':
      self.receive_thumbnail(data)


  def receive_request_accept(self, data):
    id = data.get('id')
    # Fetch connection object
    try:
      connection = models.Connection.objects.get(
        sender__id=id,
        receiver=self.scope['user']
      )
    except models.Connection.DoesNotExist:
      print('Error: connection does not exist')
      return
    # Update connection
    connection.accepted = True
    connection.save()

    serialized = serializers.RequestSerializer(connection)
    # Send accepted request to sender
    self.send_group(connection.sender.id, 'request.accept', serialized.data)
    # Send accepted request to receiver
    self.send_group(connection.receiver.id, 'request.accept', serialized.data)

  
  def receive_request_list(self, data):
    user = self.scope['user']
    # Get connections made to this user
    connections = models.Connection.objects.filter(
      receiver=user,
      accepted=False,
    )
    serialized = serializers.RequestSerializer(connections, many=True)
    # Send request list back to user
    return self.send_group(self.id, 'request.list', serialized.data)


  def receive_request_connect(self, data):
    id = data.get('id')
    # Attempt to fetch the receiving user
    try:
      receiver = models.Profile.objects.get(id=id)
    except models.Profile.DoesNotExist:
      print('Error: User not found')
      return
 
    # Create connection
    connection, _ = models.Connection.objects.get_or_create(
      sender=self.scope['user'],
      receiver=receiver,
    )
    # Serialized connection
    serialized = serializers.RequestSerializer(connection)
    # Send results back
    self.send_group(self.id, 'request.connect', serialized.data)
    # Send results back to receiver
    self.send_group(self.id, 'request.connect', serialized.data)


  def receive_search(self, data):
    query = data.get('query')
    # Get profiles from query search term
    profiles = models.Profile.objects.filter(
      Q(name__istartswith=query) |
      Q(email__istartswith=query)
    ).exclude(
      id=self._id
    ).annotate(
      pending_them=Exists(
				models.Connection.objects.filter(
					sender=self.scope['user'],
					receiver=OuterRef('id'),
					accepted=False
				)
			),
			pending_me=Exists(
				models.Connection.objects.filter(
					sender=OuterRef('id'),
					receiver=self.scope['user'],
					accepted=False
				)
			),
			connected=Exists(
				models.Connection.objects.filter(
					Q(sender=self.scope['user'], receiver=OuterRef('id')) |
					Q(receiver=self.scope['user'], sender=OuterRef('id')),
					accepted=True
				)
			),
    )
    # serializer results
    serialized = serializers.SearchSerializer(profiles, many=True)
    # send results back to user
    self.send_group(self.id, 'search', serialized.data) 


  def receive_thumbnail(self, data):
    user = self.scope['user']
    # Convert base64 data  to django content file
    image_str = data.get('base64')
    image = ContentFile(base64.b64decode(image_str))
    # Update thumbnail field
    filename = data.get('filename')
    user.thumbnail.save(filename, image, save=True)
    # Serialize user
    serialized = serializers.UserSerializer(user)
    # Send updated user data including new thumbnail 
    self.send_group(self.id, 'thumbnail', serialized.data)

  
  #--------------------------------------------
	#   Catch/all broadcast to client helpers
	#--------------------------------------------
  def send_group(self, group, source, data):
    response = {
      'type': 'broadcast_group',
      'source': source,
      'data': data
    }
    async_to_sync(self.channel_layer.group_send)(
      group, response
    )

  def broadcast_group(self, data):
    '''
    data:
      - type: 'broadcast_group'
      - source: where it originated from
      - data: what ever you want to send as a dict
    '''
    data.pop('type')
    '''
    return data:
      - source: where it originated from
      - data: what ever you want to send as a dict
    '''
    self.send(text_data=json.dumps(data))