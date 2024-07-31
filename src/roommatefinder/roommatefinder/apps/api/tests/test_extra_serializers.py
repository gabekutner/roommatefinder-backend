from django.test import TestCase

from roommatefinder.apps.api import models
from roommatefinder.apps.api.serializers import extra_serializers


class TestMessageSerializer(TestCase):
  def setUp(self):
    self.user1 = models.Profile.objects.create(identifier='user1', password='password')
    self.user2 = models.Profile.objects.create(identifier='user2', password='password')

    self.connection = models.Connection.objects.create(
      sender=self.user1,
      receiver=self.user2,
      accepted=True
    )

    self.message_by_user1 = models.Message.objects.create(
      user=self.user1,
      text='Hello from user1',
      connection=self.connection
    )
    self.message_by_user2 = models.Message.objects.create(
      user=self.user2,
      text='Hello from user2',
      connection=self.connection
    )

  def test_get_is_me(self):
    serializer = extra_serializers.MessageSerializer(instance=self.message_by_user1, context={'user': self.user1})
    data = serializer.data
    self.assertEqual(data['is_me'], True)

    serializer = extra_serializers.MessageSerializer(instance=self.message_by_user2, context={'user': self.user1})
    data = serializer.data
    self.assertEqual(data['is_me'], False)


class TestFriendSerializer(TestCase):
  def setUp(self):
    self.user1 = models.Profile.objects.create(identifier='user1', password='password')
    self.user2 = models.Profile.objects.create(identifier='user2', password='password')

    self.connection = models.Connection.objects.create(
      sender=self.user1,
      receiver=self.user2,
      accepted=True
    )

  def test_get_friend_as_sender(self):
    serializer = extra_serializers.FriendSerializer(instance=self.connection, context={'user': self.user1})
    data = serializer.data
    expected_friend = extra_serializers.UserSerializer(self.user2).data
    self.assertEqual(data['friend'], expected_friend)

  def test_get_friend_as_receiver(self):
    serializer = extra_serializers.FriendSerializer(instance=self.connection, context={'user': self.user2})
    data = serializer.data
    expected_friend = extra_serializers.UserSerializer(self.user1).data
    self.assertEqual(data['friend'], expected_friend)

  def test_get_preview_with_latest_text(self):
    self.connection.latest_text = 'Hello'
    self.connection.save()
    serializer = extra_serializers.FriendSerializer(self.connection, context={'user': self.user1})
    data = serializer.data

    # Assert the preview is serialized correctly with latest text
    self.assertEqual(data['preview'], 'Hello')
  
  def test_get_preview_without_latest_text(self):
    serializer = extra_serializers.FriendSerializer(self.connection, context={'user': self.user1})
    data = serializer.data

    # Assert the preview is 'New connection' when there's no latest text
    self.assertEqual(data['preview'], 'New connection')

  def test_get_updated_with_latest_created(self):
    from datetime import datetime, timezone
    latest_created = datetime.now(timezone.utc)
    self.connection.latest_created = latest_created
    self.connection.save()
    serializer = extra_serializers.FriendSerializer(self.connection, context={'user': self.user1})
    data = serializer.data

    # Assert the updated field is serialized with latest_created
    self.assertEqual(data['updated'], latest_created.isoformat())