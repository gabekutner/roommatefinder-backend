from django.contrib import admin
from .models import Profile, Photo, Prompt, Connection

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ["name", "email", "id"]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
  list_display = ["profile", "image"]

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
  list_display = ["profile", "prompt", "answer"]


# Chat
@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
  list_display = ["sender", "receiver"]