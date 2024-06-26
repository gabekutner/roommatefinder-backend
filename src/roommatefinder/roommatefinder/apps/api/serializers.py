from rest_framework import serializers, fields
from rest_framework_simplejwt.tokens import RefreshToken

from . import models
from roommatefinder.settings._base import POPULAR_CHOICES


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
  
class PhotoSerializer(serializers.ModelSerializer):
  image = serializers.ImageField(
    required=True, allow_null=False, max_length=None, use_url=True
  )
  class Meta:
    model = models.Photo
    fields = ["id", "image", "profile"]

class CreatePhotoSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Photo
    fields = ['image']

class UploadThumbnailSerializer(serializers.Serializer):
  thumbnail = serializers.ImageField(
    required=True, allow_null=False, max_length=None, use_url=True
  )

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

class QuoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Quote
    fields = ["id", "profile", "quote", "cited"]

class CreateQuoteSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Quote
    fields = '__all__'

class UpdateQuoteSerializer(serializers.ModelSerializer):
  quote = serializers.CharField(required=False, allow_null=True)
  cited = serializers.CharField(required=False, allow_null=True)

class LinkSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Link
    fields = ["id", "profile", "title", "link"]

class CreateLinkSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Link
    fields = '__all__'

class UpdateLinkSerializer(serializers.ModelSerializer):
  title = serializers.CharField(required=False, allow_null=True)
  link = serializers.CharField(required=False, allow_null=True)

class ProfileSerializer(serializers.ModelSerializer):
  token = serializers.SerializerMethodField(read_only=True)
  refresh_token = serializers.SerializerMethodField(read_only=True)

  sex = serializers.CharField(
    source="get_sex_display", 
    required=True, 
    allow_null=False
  )
  
  photos = PhotoSerializer(source="photo_set", many=True, read_only=True)
  prompts = PromptSerializer(source="prompt_set", many=True, read_only=True)
  quotes = QuoteSerializer(source="quote_set", many=True, read_only=True)
  links = LinkSerializer(source="link_set", many=True, read_only=True)

  class Meta:
    model = models.Profile
    fields = [
      "id",
      "token",
      "refresh_token",
      "sex",
      "photos",
      "prompts",
      "quotes",
      "links",
      "is_superuser",
      "created",
      "modified",
      "email",
      "name",
      "birthday", 
      "age",
      "instagram",
      "snapchat",
      "major",
      "city",
      "state",
      "description",
      "dorm_building",
      "interests",
      "has_account",
      "thumbnail",
      "progress",
      "graduation_year"
    ]

  # refresh the token everytime the user is called
  def get_token(self, profile):
    token = RefreshToken.for_user(profile)
    return str(token.access_token)

  def get_refresh_token(self, profile):
    token = RefreshToken.for_user(profile)
    return str(token)  



class CreateProfileSerializer(serializers.Serializer):
  birthday = serializers.DateField(required=True, allow_null=False)
  sex = ChoicesField(choices=models.Profile.SEX_CHOICES, required=True, allow_null=False)
  city = serializers.CharField(required=True, allow_null=False)
  state = serializers.CharField(required=True, allow_null=False)
  graduation_year = serializers.IntegerField(required=True, allow_null=False)
  major = serializers.CharField(required=True, allow_null=False)
  interests = fields.MultipleChoiceField(choices=POPULAR_CHOICES, required=True, allow_null=False)
  dorm_building = serializers.CharField(required=True, allow_null=False)  

  prompts = CreatePromptSerializer(source='prompt_set', many=True, required=True)
  quotes = CreateQuoteSerializer(source='quote_set', many=True, required=True)
  links = CreateLinkSerializer(source='link_set', many=True, required=True)

  

class UpdateProfileSerializer(serializers.Serializer):
  name = serializers.CharField(
    required=False,
    allow_null=True
  )
  instagram = serializers.CharField(
    required=False,
    allow_null=True
  )
  snapchat = serializers.CharField(
    required=False, 
    allow_null=True
  )
  major = serializers.CharField(
    required=False,
    allow_null=True
  )
  city = serializers.CharField(
    required=False, 
    allow_null=True
  )
  state = serializers.CharField(
    required=False, 
    allow_null=True
  )
  description = serializers.CharField(
    required=False, 
    allow_null=True, 
    allow_blank=True
  )
  dorm_building = ChoicesField(
    choices=models.Profile.DORM_CHOICES, 
    required=False, 
    allow_null=True
  )
  interests = fields.MultipleChoiceField(
    choices=POPULAR_CHOICES, 
    required=False, 
    allow_null=True
  )
  graduation_year = fields.CharField(
    required=False,
    allow_null=True
  )

class ConnectionSerializer(serializers.ModelSerializer):
  class Meta:
      model = models.Connection
      fields = ['id', 'sender', 'receiver', 'accepted']

class SwipeProfileSerializer(serializers.ModelSerializer):
  sex = serializers.CharField(
    source="get_sex_display", 
    required=True, 
    allow_null=False
  )

  photos = PhotoSerializer(source="photo_set", many=True, read_only=True)
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


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Profile
		fields = [
      'id',
			'name',
			'thumbnail',
    ]

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
    
  
class RequestSerializer(serializers.ModelSerializer):
	sender = UserSerializer()
	receiver = UserSerializer()

	class Meta:
		model = models.Connection
		fields = [
			'id',
			'sender',
			'receiver',
			'created'
		]

      
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
		# if I'm the sender
		if self.context['user'] == obj.sender:
			return UserSerializer(obj.receiver).data
		# if I'm the receiver
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
			date = obj.updated
		else:
			date = obj.latest_created or obj.updated
		return date.isoformat()


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