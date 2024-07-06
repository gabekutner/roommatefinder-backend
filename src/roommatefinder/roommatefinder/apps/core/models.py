from django.db import models
from django.utils.translation import gettext_lazy as _


class CreationModificationDateBase(models.Model):
  """ abstract base class with a creation and modification date and time """
  created = models.DateTimeField(
    _("creation date and time"),
    auto_now_add=True 
  )
  modified = models.DateTimeField(
    _("modification date and time"),
    auto_now=True
  )
  
  class Meta:
    abstract=True