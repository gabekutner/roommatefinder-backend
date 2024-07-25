from django.contrib import admin
from .models import (
  Profile, 
  Photo, 
  Connection, 
  Message, 
  RoommateQuiz,
  # Prompt,
  # Quote,
  # Link
)

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ["name", "identifier", "id"]

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

""" widgets taken out of inital app version """
# @admin.register(Prompt)
# class PromptAdmin(admin.ModelAdmin):
#   list_display = ["profile", "question"]

# @admin.register(Quote)
# class QuoteAdmin(admin.ModelAdmin):
#   list_display = ["profile", "quote"]

# @admin.register(Link)
# class LinkAdmin(admin.ModelAdmin):
#   list_display = ["profile", "title"]