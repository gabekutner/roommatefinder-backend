# -*- coding: utf-8 -*-
from django.contrib import admin
from roommatefinder.apps.api import models

# Register your models here.
@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ["name", "identifier", "id"]

@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
  list_display = ["profile", "image"]

@admin.register(models.Connection)
class ConnectionAdmin(admin.ModelAdmin):
  list_display = ["sender", "receiver"]

@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin):
  list_display = ["connection"]

@admin.register(models.RoommateQuiz)
class RoommateQuizAdmin(admin.ModelAdmin):
  list_display = ["profile"]