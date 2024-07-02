""" roommatefinder/apps/api/models.py """
import uuid
import datetime

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField
from model_utils import Choices

from roommatefinder.apps.core.models import CreationModificationDateBase
from roommatefinder.apps.api.managers import CustomUserManager
from roommatefinder.settings._base import POPULAR_CHOICES, PROMPTS


def upload_thumbnail(instance, filename):
	path = f'thumbnails/{instance.id}'
	extension = filename.split('.')[-1]
	if extension:
		path = path + '.' + extension
	return path

# Create your models here.
class Profile(AbstractBaseUser, PermissionsMixin, CreationModificationDateBase):
  """ Profile Model 
  create: (del later)
    birthday: new Date(),
    sex: "",
    hometown: "",
    graduation_year: "",
    major: "",
    interests: [],
    prompts: [],
    quotes: [],
    links: [],
    photos: [],
  """
  SEX_CHOICES = Choices(("M", "Male"),
                        ("F", "Female"),)
  
  DORM_CHOICES = Choices(('1', 'Chapel Glen'), 
                         ('2', 'Gateway Heights'),
                         ('3' ,'Impact and Prosperity Epicenter'),
                         ('4', 'Kahlert Village'),
                         ('5', 'Lassonde Studios'),
                         ('6', 'Officers Circle'),
                         ('7', 'Sage Point'),
                         ('8', 'Marriott Honors Community'),
                         ('9', 'Guest House'),
                         ('10', "I don't know"), )
  
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  email = models.CharField(max_length=200, unique=True)
  name = models.CharField(max_length=200, null=True)
  password = models.CharField(max_length=200)

  birthday = models.DateField(null=True)
  
  instagram = models.CharField(max_length=15, null=True, blank=True)
  snapchat = models.CharField(max_length=15, null=True, blank=True)
  major = models.CharField(max_length=25, null=True, default="Undecided")
  city = models.CharField(max_length=25, null=True, blank=True)
  state = models.CharField(max_length=25, null=True, blank=True)
  description = models.TextField(max_length=500, null=True, blank=True)
  dorm_building = models.CharField(choices=DORM_CHOICES, max_length=2, null=True)
  interests = MultiSelectField(choices=POPULAR_CHOICES, max_choices=5, max_length=1000)
  graduation_year = models.PositiveIntegerField(null=True, blank=True)

  # background
  is_staff = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  has_account = models.BooleanField(default=False)
  
  sex = models.CharField(
    choices=SEX_CHOICES,
    max_length=1,
    null=False,
    blank=False,
  )

  thumbnail = models.ImageField(
		upload_to=upload_thumbnail,
		null=True,
		blank=True
	)

  blocked_profiles = models.ManyToManyField(
    "self", symmetrical=False, related_name="blocked_by", blank=True
  )

  USERNAME_FIELD = "email"
  # required for creating user
  REQUIRED_FIELDS = []

  objects = CustomUserManager()

  @property
  def age(self):
    if self.birthday:
      return int((datetime.date.today() - self.birthday).days / 365.25)
  
  @property
  def progress(self):
    attrs = self.__dict__
    attrs_to_delete = (
      '_state', 
      'last_login',
      'is_superuser',
      'created',
      'modified',
      'id',
      'password',
      'is_staff',
      'is_active',
      'has_account',
    )
    for attr in attrs_to_delete:
      attrs.pop(attr, None)

    progress = 0
    count = attrs.keys().__len__()
    for key in attrs.keys():
      if attrs[key] == None:
        progress += 1

    return 100 - int((progress / count) * 100)

  def block_profile(self, blocked_profile):
    """ block a profile """
    # try:
    #   connection = Connection.objects.get(
    #     Q(sender=self.id, receiver=blocked_profile.id) | Q(sender=blocked_profile.id, receiver=self.id),
    #     accepted=True,
    #   )
    #   print(connection)
    #   messages = Message.objects.get(connection=connection)
    #   print(messages)
    # except Connection.DoesNotExist:
    #   print({"detail": f"no connection between {self.id} and {blocked_profile.id}"})
    
    # connection.delete()

    # try:
    #   print(connection)
      

    # except Message.DoesNotExist:
    #   print({"detail": f"no messages between {self.id} and {blocked_profile.id}"})

    self.blocked_profiles.add(blocked_profile)

  def delete(self):
    """ delete profile """
    super().delete()


class Photo(CreationModificationDateBase):
  """ Photo Model """    
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)
  image = models.ImageField(null=True, blank=True)

  def delete(self):
    self.image.delete(save=False)
    super().delete()


class Prompt(CreationModificationDateBase):
  """ Prompts Model """
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)
  question = models.CharField(
    choices=PROMPTS,
    max_length=2,
    null=False,
    blank=False
  )
  answer = models.CharField(max_length=250, null=False, blank=False)

class Quote(CreationModificationDateBase):
  """ Quotes Model """
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)
  quote = models.CharField(max_length=250, null=False, blank=False)
  cited = models.CharField(max_length=100, null=True, blank=True)

class Link(CreationModificationDateBase):
  """ Links Model """
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)
  title = models.CharField(max_length=250, null=False, blank=False)
  link = models.CharField(max_length=250, null=False, blank=False)


class RoommateQuiz(CreationModificationDateBase):
  """ Roommate Matching Quiz Model """
  profile = models.OneToOneField(
    Profile,
    on_delete=models.CASCADE,
    primary_key=True,
  )
  social_battery = models.IntegerField(
    null=False, 
    blank=False,
    validators=[
      MinValueValidator(0),
      MaxValueValidator(20)
    ],
    default=10
  )
  clean_room = models.CharField(max_length=100, null=False, blank=True, default="")
  noise_level = models.IntegerField(
    null=False, 
    blank=False,
    validators=[
      MinValueValidator(0),
      MaxValueValidator(20)
    ],
    default=10
  )
  guest_policy = models.CharField(max_length=100, null=False, blank=True, default="")
  in_room = models.IntegerField(
    null=False, 
    blank=False,
    validators=[
      MinValueValidator(0),
      MaxValueValidator(20)
    ],
    default=10
  )
  hot_cold = models.IntegerField(
    null=False, 
    blank=False,
    validators=[
      MinValueValidator(0),
      MaxValueValidator(20)
    ],
    default=10
  )
  bed_time = models.CharField(max_length=100, null=False, blank=True, default="")
  wake_up_time = models.CharField(max_length=100, null=False, blank=True, default="")
  sharing_policy = models.CharField(max_length=100, null=False, blank=True, default="")
  


class Connection(models.Model): 
  sender = models.ForeignKey(
    Profile,
    related_name='sent_connections',
    on_delete=models.CASCADE
  )
  receiver = models.ForeignKey(
    Profile,
    related_name='received_connections',
    on_delete=models.CASCADE
  )
  accepted = models.BooleanField(default=False)
  # new data point - display_match:bool , default = false
  # if model is being updated than display_match=True
  display_match = models.BooleanField(default=False)

  # deprecated, can replace with CreationModificationBase
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
	  return str(self.sender.id) + ' -> ' + str(self.receiver.id)


class Message(models.Model):
	connection = models.ForeignKey(
		Connection,
		related_name='messages',
		on_delete=models.CASCADE
	)
	user = models.ForeignKey(
		Profile,
		related_name='my_messages',
		on_delete=models.CASCADE
	)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.user.id) + ': ' + self.text