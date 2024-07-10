from rest_framework import serializers
from .. import models
from ..serializers import photo_serializers


class ChoicesField(serializers.Field):
  """ custom choices field """
  def __init__(self, choices, **kwargs):
    self._choices = choices
    super(ChoicesField, self).__init__(**kwargs)

  def to_representation(self, obj):
    if obj in self._choices:
      return self._choices[obj]
    return obj

  def to_internal_value(self, data):
    if data in self._choices:
      return getattr(self._choices, data)
    raise serializers.ValidationError(["choice not valid"])

# prompts
class PromptSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Prompt
    fields = ["id", "profile", "question", "answer"]

class CreatePromptSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Prompt
    fields = '__all__'

class UpdatePromptSerializer(serializers.Serializer):
  question = serializers.CharField(required=False, allow_null=True)
  answer = serializers.CharField(required=False, allow_null=True)

# quotes
class QuoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Quote
    fields = ["id", "profile", "quote", "cited"]

class CreateQuoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Quote
    fields = '__all__'

class UpdateQuoteSerializer(serializers.Serializer):
  quote = serializers.CharField(required=False, allow_null=True)
  cited = serializers.CharField(required=False, allow_null=True)

# links
class LinkSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Link
    fields = ["id", "profile", "title", "link"]

class CreateLinkSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Link
    fields = '__all__'

class UpdateLinkSerializer(serializers.Serializer):
  title = serializers.CharField(required=False, allow_null=True)
  link = serializers.CharField(required=False, allow_null=True)

# connections
class ConnectionSerializer(serializers.ModelSerializer):
  class Meta:
      model = models.Connection
      fields = ['id', 'sender', 'receiver', 'accepted']

# swipe
class SwipeProfileSerializer(serializers.ModelSerializer):
  sex = serializers.CharField(
    source="get_sex_display", 
    required=True, 
    allow_null=False
  )
  photos = photo_serializers.PhotoSerializer(source="photo_set", many=True, read_only=True)
  prompts = PromptSerializer(source="prompt_set", many=True, read_only=True)
  quotes = QuoteSerializer(source="quote_set", many=True, read_only=True)
  links = LinkSerializer(source="link_set", many=True, read_only=True)
  # get status of connection between 
  sent_connections = ConnectionSerializer(many=True)
  received_connections = ConnectionSerializer(many=True)
  class Meta:
    model = models.Profile
    fields = [
      "id",
      "email",
      "name",
      "birthday",
      "age",
      "sex",
      "city",
      "state",
      "major",
      "dorm_building",
      "description",
      "instagram",
      "snapchat",
      "interests",
      "thumbnail",
      "graduation_year",
      "photos",
      "prompts",
      "quotes",
      "links",
      "sent_connections",
      "received_connections",
    ]

# basic user 
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Profile
		fields = [
      'id',
			'name',
			'thumbnail',
    ]

# search
class SearchSerializer(UserSerializer):
  status = serializers.SerializerMethodField()
  class Meta:
    model = models.Profile
    fields = [
      'id',
      'name',
			'thumbnail',
      'status'
    ]

  def get_status(self, obj):
    if obj.pending_them:
      return 'pending-them'
    elif obj.pending_me:
      return 'pending-me'
    elif obj.connected:
      return 'connected'
    return 'no-connection'
    
# request
class RequestSerializer(serializers.ModelSerializer):
	sender = UserSerializer()
	receiver = UserSerializer()
	class Meta:
		model = models.Connection
		fields = [
			'id',
			'sender',
			'receiver',
			'created',
      'display_match'
		]

# friends
class FriendSerializer(serializers.ModelSerializer):
	friend = serializers.SerializerMethodField()
	preview = serializers.SerializerMethodField()
	updated = serializers.SerializerMethodField()
	class Meta:
		model = models.Connection
		fields = [
			'id',
			'friend',
			'preview',
			'updated',
		]

	def get_friend(self, obj):
		# if i'm the sender
		if self.context['user'] == obj.sender:
			return UserSerializer(obj.receiver).data
		# if i'm the receiver
		elif self.context['user'] == obj.receiver:
			return UserSerializer(obj.sender).data
		else:
			print('Error: No user found in friendserializer')

	def get_preview(self, obj):
		default = 'New connection'
		if not hasattr(obj, 'latest_text'):
			return default
		return obj.latest_text or default

	def get_updated(self, obj):
		if not hasattr(obj, 'latest_created'):
			date = obj.modified
		else:
			date = obj.latest_created or obj.modified
		return date.isoformat()

# message
class MessageSerializer(serializers.ModelSerializer):
	is_me = serializers.SerializerMethodField()
	class Meta:
		model = models.Message
		fields = [
			'id',
			'is_me',
			'text',
			'created',
		]

	def get_is_me(self, obj):
		return self.context['user'] == obj.user