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
  image = serializers.ListField(
    required=True, 
    allow_null=False, 
    max_length=None, 
  )

  class Meta:
    model = models.Photo
    fields = ["id", "image", "profile"]

class ProfileSerializer(serializers.ModelSerializer):
  token = serializers.SerializerMethodField(read_only=True)
  refresh_token = serializers.SerializerMethodField(read_only=True)
  sex = serializers.CharField(
    source="get_sex_display", 
    required=True, 
    allow_null=False
  )

  class Meta:
    model = models.Profile
    exclude = [
      "user_permissions",
      "groups",
      "password",
      "last_login",
      "is_staff",
      "is_active",
      "blocked_profiles",
   ]

  # refresh the token everytime the user is called
  def get_token(self, profile):
    token = RefreshToken.for_user(profile)
    return str(token.access_token)

  def get_refresh_token(self, profile):
    token = RefreshToken.for_user(profile)
    return str(token)
  

class CreateProfileSerializer(serializers.Serializer):
  birthday = serializers.DateField(
    required=True, 
    allow_null=False
  )
  sex = ChoicesField(
    choices=models.Profile.SEX_CHOICES, 
    required=True, 
    allow_null=False
  )
  dorm_building = serializers.CharField(
    required=True, 
    allow_null=False
  )
  interests = fields.MultipleChoiceField(
    choices=POPULAR_CHOICES, 
    required=True, 
    allow_null=False
  )
  thumbnail = fields.ImageField(
    required=True,
    allow_null=False
  )


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
  # sex = ChoicesField(
  #   choices=models.Profile.SEX_CHOICES, 
  #   required=False, 
  #   allow_null=True
  # )
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


class SwipeProfileSerializer(serializers.ModelSerializer):
  sex = serializers.CharField(
    source="get_sex_display", 
    required=True, 
    allow_null=False
  )

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