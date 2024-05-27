import json
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
    if not user.is_authenticated:
      self.close()
      return

    # self.id, self._id = str(user.id), user.id
    self._id = str(user.id)
    # join this user to a group by their id
    async_to_sync(self.channel_layer.group_add)(
			self._id, self.channel_name
		)
    self.accept()

  def disconnect(self, close_code):
		# leave room/group
    async_to_sync(self.channel_layer.group_discard)(
			self._id, self.channel_name
		)
		

  #----------------------
	#   Handle Requests
	#----------------------
  def receive(self, text_data):
    # receive message from websocket
    data = json.loads(text_data)
    data_source = data.get('source')

    # gearch / filter users
    if data_source == 'search':
      self.receive_search(data)

    # get friend list
    elif data_source == 'friend.list':
      self.receive_friend_list(data)
    
    # get message list
    elif data_source == 'message.list':
      self.receive_message_list(data)

		# message has been sent
    elif data_source == 'message.send':
      self.receive_message_send(data)

		# user is typing message
    elif data_source == 'message.type':
      self.receive_message_type(data)

    # make friend request
    elif data_source == 'request.connect':
      self.receive_request_connect(data)

    # accept friend request
    elif data_source == 'request.accept':
      self.receive_request_accept(data)

    # get request list
    elif data_source == 'request.list':
      self.receive_request_list(data)

    # upload thumbnail
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
      print({"detail": "couldn't find connection"})
      return
    
    # get messages
    messages = models.Message.objects.filter(
      connection=connection
    ).order_by('-created')[page * page_size:(page + 1) * page_size]
    # serialized message
    serialized_messages = serializers.MessageSerializer(
      messages,
      context={'user': user}, 
      many=True
    )
    # get recipient friend
    recipient = connection.sender
    if connection.sender == user:
      recipient = connection.receiver

    # serialize friend
    serialized_friend = serializers.UserSerializer(recipient)

    # count the total number of messages for this connection
    messages_count = models.Message.objects.filter(
      connection=connection
    ).count()

    next_page = page + 1 if messages_count > (page + 1 ) * page_size else None

    data = {
      'messages': serialized_messages.data,
      'next': next_page,
      'friend': serialized_friend.data
    }
    # send back to the requestor
    self.send_group(str(user.id), 'message.list', data)


  def receive_message_send(self, data):
    user = self.scope['user']
    connectionId = data.get('connectionId')
    message_text = data.get('message')
    try:
      connection = models.Connection.objects.get(id=connectionId)
    except models.Connection.DoesNotExist:
      print({"detail": "couldn't find connection"})
      return

    message = models.Message.objects.create(
      connection=connection,
      user=user,
      text=message_text
    )

    # get recipient friend
    recipient = connection.sender
    if connection.sender == user:
      recipient = connection.receiver

    # send new message back to sender
    serialized_message = serializers.MessageSerializer(
      message,
      context={'user': user}
    )
    serialized_friend = serializers.UserSerializer(recipient)
    data = {
      'message': serialized_message.data,
      'friend': serialized_friend.data
    }
    self.send_group(str(user.id), 'message.send', data)

    # send new message to receiver
    serialized_message = serializers.MessageSerializer(
      message,
      context={'user': recipient}
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
    data = {'id': str(recipient_id)}
    self.send_group(str(recipient_id), 'message.type', data)


  def receive_friend_list(self, data):
    user = self.scope['user']
    # get connections for user
    connections = models.Connection.objects.filter(
      Q(sender=user) | Q(receiver=user),
      accepted=True,
    )
    serialized = serializers.FriendSerializer(connections, context={ 'user': user}, many=True)
    # send data back to user
    self.send_group(str(user.id), 'friend.list', serialized.data)


  def receive_request_accept(self, data):
    id = data.get('id')
    # fetch connection object
    try:
      connection = models.Connection.objects.get(
        sender__id=id,
        receiver=self.scope['user']
      )
    except models.Connection.DoesNotExist:
      print({"detail": "connection does not exist"})
      return
    # update connection
    connection.accepted = True
    connection.save()

    serialized = serializers.RequestSerializer(connection)
    # send accepted request to sender
    self.send_group(str(connection.sender.id), 'request.accept', serialized.data)
    # send accepted request to receiver
    self.send_group(str(connection.receiver.id), 'request.accept', serialized.data)

  
  def receive_request_list(self, data):
    user = self.scope['user']
    # get connections made to this user
    connections = models.Connection.objects.filter(
      receiver=user,
      accepted=False,
    )
    serialized = serializers.RequestSerializer(connections, many=True)
    # send request list back to user
    return self.send_group(str(user.id), 'request.list', serialized.data)


  def receive_request_connect(self, data):
    id = data.get('id')
    # attempt to fetch the receiving user
    try:
      receiver = models.Profile.objects.get(id=id)
    except models.Profile.DoesNotExist:
      print({'detail': 'user not found'})
      return
 
    # create connection
    connection, _ = models.Connection.objects.get_or_create(
      sender=self.scope['user'],
      receiver=receiver,
    )
    # serialized connection
    serialized = serializers.RequestSerializer(connection)
    # send results back to sender
    self.send_group(str(connection.sender.id), 'request.connect', serialized.data)
    # send results back to receiver
    self.send_group(str(connection.receiver.id), 'request.connect', serialized.data)


  def receive_search(self, data):
    query = data.get('query')
    # get profiles from query search term
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
    # serialized results
    serialized = serializers.SearchSerializer(profiles, many=True)
     # send results back to user
    self.send_group(self._id, 'search', serialized.data) 


  def receive_thumbnail(self, data):
    user = self.scope['user']
    # convert base64 data  to django content file
    image_str = data.get('base64')
    image = ContentFile(base64.b64decode(image_str))
    # update thumbnail field
    filename = data.get('filename')
    user.thumbnail.save(filename, image, save=True)
    # serialize user
    serialized = serializers.UserSerializer(user)
    # send updated user data including new thumbnail 
    self.send_group(self._id, 'thumbnail', serialized.data)

  
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