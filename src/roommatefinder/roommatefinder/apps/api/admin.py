from django.contrib import admin
from .models import Profile, Photo, Connection, Message, RoommateQuiz

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ["name", "email", "id"]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
  list_display = ["profile", "image"]

@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
  list_display = ["sender", "receiver"]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
  list_display = ["connection"]

@admin.register(RoommateQuiz)
class RoommateQuizAdmin(admin.ModelAdmin):
  list_display = ["profile"]