# -*- coding: utf-8 -*-
from rest_framework import serializers
from roommatefinder.apps.api import models


class ConnectionSerializer(serializers.ModelSerializer):
	"""
	Serializer Class for the Connection model
	"""
	class Meta:
		model = models.Connection
		fields = ['id', 'sender', 'receiver', 'accepted']


class UserSerializer(serializers.ModelSerializer):
	"""
	Serializer Class for the Profile model, used for socket connection 
	"""
	class Meta:
		model = models.Profile
		fields = [
      'id',
			'name',
			'thumbnail',
    ]


class SearchSerializer(UserSerializer):
	"""
	Serializer class for Search items 
	"""
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
	"""
	Serializer class for the Request model
	"""
	sender = UserSerializer()
	receiver = UserSerializer()
	class Meta:
		model = models.Connection
		fields = [
			'id',
			'sender',
			'receiver',
			'created',
		]


class FriendSerializer(serializers.ModelSerializer):
	"""
	Serializer class for an accepted connection
	"""
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
			# @! create more specific error
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


class MessageSerializer(serializers.ModelSerializer):
	"""
	Serializer class for the Message model
	"""
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