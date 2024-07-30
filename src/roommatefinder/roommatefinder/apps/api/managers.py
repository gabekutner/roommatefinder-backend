from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
  """ custom user model manager """
  def create_user(self, identifier, password, **extra_fields):
    """ create and save a profile """
    if not identifier:
      raise ValueError(_("The Identifier must be set"))
    user = self.model(identifier=identifier, **extra_fields)
    user.set_password(password)
    user.save()
    return user
  
  def create_superuser(self, identifier, password, **extra_fields):
    """ create and save a superuser """
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    extra_fields.setdefault("is_active", True)

    if extra_fields.get("is_staff") is not True:
      raise ValueError(_("superuser must have is_staff=True"))
    if extra_fields.get("is_superuser") is not True:
      raise ValueError(_("superuser must have is_superuser=True"))
    return self.create_user(identifier, password, **extra_fields)