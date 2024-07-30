# -*- coding: utf-8 -*-
import json
import base64
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from django.db.models import Q, Exists, OuterRef

from roommatefinder.apps.api import models
from roommatefinder.apps.api.serializers import extra_serializers


class APIConsumer(WebsocketConsumer):
  """
  WebSocket Consumer for handling WebSocket connections.

  This consumer manages WebSocket connections for authenticated users. It allows 
  users to search, message other users, and send friend requests and accept them.

  Methods:
    connect():
      Handles WebSocket connection requests. Checks user authentication and
      adds the user to a group if authenticated.

    disconnect(close_code):
      Handles WebSocket disconnection requests. Removes the user from the group
      upon disconnection.

  Attributes:
    _id (str): The unique identifier of the user, set during the connection process.
  """
  def connect(self):
    """
    Handles the WebSocket connection request.

    This method is triggered when a WebSocket connection request is made. It performs
    the following actions:
    - Checks if the user is authenticated.
    - If authenticated, adds the user to a group identified by their user ID.
    - Accepts the WebSocket connection.

    If the user is not authenticated, the connection is closed.
    """
    user = self.scope['user']
    # Close connection attempt if user isn't authenticated
    if not user.is_authenticated:
      self.close()
      return
    # Use the users UUID .id attr for connections
    self._id = str(user.id)
    async_to_sync(self.channel_layer.group_add)(
			self._id, self.channel_name
		)
    self.accept()


  def disconnect(self, close_code):
    """
    Handles the WebSocket disconnection request.

    This method is triggered when a WebSocket disconnection request is made. It performs
    the following actions:
    - Removes the user from the group identified by their user ID.

    Args:
      close_code (int): The code representing the reason for disconnection.
    """
    async_to_sync(self.channel_layer.group_discard)(
			self._id, self.channel_name
		)


  def receive(self, text_data):
    """
    Handles incoming messages from the WebSocket.

    This method processes messages over the WebSocket connection. It routes the 
    message to the appropriate handler based on the 'source' field in the received data.

    Args:
      text_data (str): The JSON-encoded message received from the WebSocket.

    Returns:
        None

    The method handles the following types of messages based on the 'source' field:
        - 'search': Processes search-related messages by calling `receive_search`.
        - 'friend.list': Retrieves the friend list by calling `receive_friend_list`.
        - 'message.list': Retrieves the message list by calling `receive_message_list`.
        - 'message.send': Handles sending messages by calling `receive_message_send`.
        - 'message.type': Updates typing status by calling `receive_message_type`.
        - 'request.connect': Handles friend connection requests by calling `receive_request_connect`.
        - 'request.accept': Accepts friend requests by calling `receive_request_accept`.
        - 'request.list': Retrieves the list of friend requests by calling `receive_request_list`.
        ### Possibly deprecated in first version
        - 'thumbnail': Processes thumbnail uploads by calling `receive_thumbnail`.

    Raises:
      JSONDecodeError: If the `text_data` is not valid JSON.
      KeyError: If the 'source' field is missing in the `text_data`.
    """
    try:
      # Receive message from websocket
      data = json.loads(text_data)
      data_source = data.get('source')

      # Route the message based on the 'source' field
      if data_source == 'search':
        self.receive_search(data)

      elif data_source == 'friend.list':
        self.receive_friend_list(data)
      
      elif data_source == 'message.list':
        self.receive_message_list(data)

      elif data_source == 'message.send':
        self.receive_message_send(data)

      elif data_source == 'message.type':
        self.receive_message_type(data)

      elif data_source == 'request.connect':
        self.receive_request_connect(data)

      elif data_source == 'request.accept':
        self.receive_request_accept(data)

      elif data_source == 'request.list':
        self.receive_request_list(data)

      elif data_source == 'thumbnail':
        self.receive_thumbnail(data)
      
      else:
        self.send(text_data=json.dumps({'error': 'Unknown source'}))

    except json.JSONDecodeError:
      self.send(text_data=json.dumps({'error': 'Invalid JSON data'}))


  def receive_message_list(self, data: dict) -> None:
    """
    Handles incoming WebSocket messages requesting a list of messages for a specific connection.

    This method processes the `message.list` event by retrieving and serializing messages 
    for a given connection. It paginates the messages, serializes them, and sends the paginated 
    result along with the recipient's information back to the requester.

    Parameters:
      data (dict): A dictionary containing:
        - 'connectionId': The ID of the connection for which to retrieve messages.
        - 'page': The current page number for pagination.

    Notes:
      - If the specified connection does not exist, a log message is printed, and no data is sent.
      - Messages are retrieved with pagination. The page size is fixed at 15 messages per page.
      - The recipient of the messages is determined based on the connection details.
      - The response includes serialized messages, the recipient's information, and the pagination status.
    """
    user = self.scope['user']
    connectionId = data.get('connectionId')
    # Retrieve the page number from the incoming data, defaulting to 0
    page = data.get('page', 0)
    # The number of messages per page
    page_size = 15

    try:
      connection = models.Connection.objects.get(id=connectionId)
    except models.Connection.DoesNotExist:
      print({"detail": "Couldn't find connection."})
      return
    
    # Retrieve and paginate messages for the connection
    messages = models.Message.objects.filter(
      connection=connection
    ).order_by('-created')[page * page_size:(page + 1) * page_size]

    # Serialize the messages
    serialized_messages = extra_serializers.MessageSerializer(
      messages,
      context={'user': user}, 
      many=True
    )
    # Determine the recipient of the messages
    recipient = connection.sender
    if connection.sender == user:
      recipient = connection.receiver

    # Serialize the recipient's information
    serialized_friend = extra_serializers.UserSerializer(recipient)

    # Count the total number of messages for the connection
    messages_count = models.Message.objects.filter(
      connection=connection
    ).count()
    # Determine if there is a next page of messages
    next_page = page + 1 if messages_count > (page + 1 ) * page_size else None
    # Response data
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
    serialized_message = extra_serializers.MessageSerializer(
      message,
      context={'user': user}
    )
    serialized_friend = extra_serializers.UserSerializer(recipient)
    data = {
      'message': serialized_message.data,
      'friend': serialized_friend.data
    }
    self.send_group(str(user.id), 'message.send', data)

    # send new message to receiver
    serialized_message = extra_serializers.MessageSerializer(
      message,
      context={'user': recipient}
    )
    serialized_friend = extra_serializers.UserSerializer(user)
    data = {
      'message': serialized_message.data,
      'friend': serialized_friend.data
    }
    self.send_group(str(recipient.id), 'message.send', data)


  def receive_message_type(self, data: dict) -> None:
    """
    Handles incoming WebSocket messages indicating that a user is typing.

    This method processes the `message.type` event, which is sent when a user is 
    typing a message. It extracts the recipient's ID from the incoming data and sends a 
    notification to the group corresponding to the recipient's ID.

    Parameters:
      data (dict): A dictionary containing the incoming message data. It should 
      include an `'id'` key representing the recipient's user ID.

    Notes:
      - The `self.scope['user']` is used to identify the current user, but it is not directly used in this method.
      - The `data` dictionary is transformed to only include the `'id'` key before sending the message to the recipient.
      - The `send_group` method is responsible for sending the notification to the appropriate group.
    """
    # user = self.scope['user']
    recipient_id = data.get('id')
    data = {'id': str(recipient_id)}
    self.send_group(str(recipient_id), 'message.type', data)


  def receive_friend_list(self, data: dict):
    user = self.scope['user']
    # Get connections for user
    connections = models.Connection.objects.filter(
      Q(sender=user) | Q(receiver=user),
      accepted=True,
    )
    serialized = extra_serializers.FriendSerializer(connections, context={'user': user}, many=True)
    # Send data back to user
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

    serialized = extra_serializers.RequestSerializer(connection)
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
    serialized = extra_serializers.RequestSerializer(connections, many=True)
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

    # test if an unaccepted connection exists between the two users already
    # this would mean receiver and sender are switched in this possible connection
    try:
      possible_connection = models.Connection.objects.get(
        receiver=self.scope['user'], sender=receiver
      )
    except models.Connection.DoesNotExist:
      possible_connection = None
    # if there already exists a connection, update the possible_connection as accepted
    if possible_connection is not None:
      possible_connection.accepted = True
      possible_connection.display_match = True
      possible_connection.save()
      connection = possible_connection
    else:
      # create connection 
      connection, _ = models.Connection.objects.get_or_create(
        sender=self.scope['user'],
        receiver=receiver,
      )
    # serialized connection
    serialized = extra_serializers.RequestSerializer(connection)
    # send results back to sender
    self.send_group(str(connection.sender.id), 'request.connect', serialized.data)
    # send results back to receiver
    self.send_group(str(connection.receiver.id), 'request.connect', serialized.data)


  def receive_search(self, data):
    query = data.get('query')
    # get profiles from query search term
    profiles = models.Profile.objects.filter(
      Q(name__istartswith=query) |
      Q(identifier__istartswith=query)
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
    serialized = extra_serializers.SearchSerializer(profiles, many=True)
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
    serialized = extra_serializers.UserSerializer(user)
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