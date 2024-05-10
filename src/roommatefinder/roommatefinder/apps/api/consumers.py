import json
import uuid
import base64
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from django.db.models import Q, Exists, OuterRef

from . import models
from . import serializers


class APIConsumer(WebsocketConsumer):

  def connect(self):
    user = self.scope['user']
    # print(user, user.is_authenticated)
    if not user.is_authenticated:
      return

    self.id, self._id = str(user.id), user.id
    # Join this user to a group by their email
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
    # Receive message from websocket
    data = json.loads(text_data)
    data_source = data.get('source')

    print('receive ', json.dumps(data, indent=2))

    # Search / filter users
    if data_source == 'search':
      self.receive_search(data)

    # Get friend list
    elif data_source == 'friend.list':
      self.receive_friend_list(data)
    
    elif data_source == 'message.list':
      self.receive_message_list(data)

		# Message has been sent
    elif data_source == 'message.send':
      self.receive_message_send(data)

		# User is typing message
    elif data_source == 'message.type':
      self.receive_message_type(data)

    # Make friend request
    elif data_source == 'request.connect':
      self.receive_request_connect(data)

    # Accept friend request
    elif data_source == 'request.accept':
      self.receive_request_accept(data)

    # Get request list
    elif data_source == 'request.list':
      self.receive_request_list(data)

    # Upload thumbnail
    elif data_source == 'thumbnail':
      self.receive_thumbnail(data)


  def receive_message_list(self, data):
    user = self.scope['user']
    connectionId = data.get('connectionId')
    page = data.get('page')
    page_size = 15
    try:
      connection = models.Connection.objects.get(id=connectionId)
    except models.Connection.DoesNotExist:
      print("Error: couldn't find connection")
      return
    # Get messages
    messages = models.Message.objects.filter(
      connection=connection
    ).order_by('-created')[page * page_size:(page + 1) * page_size]
    # Serialized message
    serialized_messages = serializers.MessageSerializer(
      messages,
      context={ 
        'user': user 
      }, 
      many=True
    )
    # Get recipient friend
    recipient = connection.sender
    if connection.sender == user:
      recipient = connection.receiver

    # Serialize friend
    serialized_friend = serializers.UserSerializer(recipient)

    # Count the total number of messages for this connection
    messages_count = models.Message.objects.filter(
      connection=connection
    ).count()

    next_page = page + 1 if messages_count > (page + 1 ) * page_size else None

    data = {
      'messages': serialized_messages.data,
      'next': next_page,
      'friend': serialized_friend.data
    }
    # Send back to the requestor
    self.send_group(str(user.id), 'message.list', data)


  def receive_message_send(self, data):
    user = self.scope['user']
    connectionId = data.get('connectionId')
    message_text = data.get('message')
    try:
      connection = models.Connection.objects.get(id=connectionId)
    except models.Connection.DoesNotExist:
      print('Error: couldnt find connection')
      return

    message = models.Message.objects.create(
      connection=connection,
      user=user,
      text=message_text
    )

    # Get recipient friend
    recipient = connection.sender
    if connection.sender == user:
      recipient = connection.receiver

    # Send new message back to sender
    serialized_message = serializers.MessageSerializer(
      message,
      context={
        'user': user
      }
    )
    serialized_friend = serializers.UserSerializer(recipient)
    data = {
      'message': serialized_message.data,
      'friend': serialized_friend.data
    }
    self.send_group(str(user.id), 'message.send', data)

    # Send new message to receiver
    serialized_message = serializers.MessageSerializer(
      message,
      context={
        'user': recipient
      }
    )
    serialized_friend = serializers.UserSerializer(user)
    data = {
      'message': serialized_message.data,
      'friend': serialized_friend.data
    }
    self.send_group(str(recipient.id), 'message.send', data)


  def receive_message_type(self, data):
    user = self.scope['user']
    recipient_id = data.get('id')
    data = {
      'id': str(recipient_id)
    }
    self.send_group(str(recipient_id), 'message.type', data)


  def receive_friend_list(self, data):
    user = self.scope['user']
    # Get connections for user
    connections = models.Connection.objects.filter(
      Q(sender=user) | Q(receiver=user),
      accepted=True,
    )
    serialized = serializers.FriendSerializer(connections, context={ 'user': user}, many=True)
    # Send data back to user
    self.send_group(str(user.id), 'friend.list', serialized.data)


  def receive_request_accept(self, data):
    id = data.get('id')
    print(f'data: {data}')
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
    self.send_group(str(connection.sender.id), 'request.accept', serialized.data)
    # Send accepted request to receiver
    self.send_group(str(connection.receiver.id), 'request.accept', serialized.data)

  
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
    # Send results back to sender
    self.send_group(str(connection.sender.id), 'request.connect', serialized.data)
    # Send results back to receiver
    self.send_group(str(connection.receiver.id), 'request.connect', serialized.data)


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
    # Serialized results
    serialized = serializers.SearchSerializer(profiles, many=True)
     # Send results back to user
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