from django.contrib import admin
from .models import Profile, Photo

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ["name", "email", "id"]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
  list_display = ["profile", "image"]