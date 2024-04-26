from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
# from .models import ...

# @receiver(post_save, sender=Model)
# def model_save_handler(sender, **kwargs):
#   if settings.DEBUG:
#     print(f"{kwargs["instance"]} saved.")

# @receiver(post_delete, sender=Model)
# def model_delete_handler(sender, **kwargs):
#   if settings.DEBUG:
#     print(f"{kwargs["instance"]} deleted.")