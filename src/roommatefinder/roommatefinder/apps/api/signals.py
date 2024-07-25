import random
import datetime

from rest_framework import status
from rest_framework.response import Response

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from . import models


@receiver(post_save, sender=models.Profile)
def send_otp(sender, instance, **kwargs):
  """ send otp on Profile init """  
  if int(instance.max_otp_try) == 0 and instance.otp_max_out and timezone.now() < instance.otp_max_out:
    return Response(
    "Max OTP try reached, try after an hour",
    status=status.HTTP_400_BAD_REQUEST,
  )

  otp = random.randint(1000, 9999)
  otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
  max_otp_try = int(instance.max_otp_try) - 1

  instance.otp = otp
  instance.otp_expiry = otp_expiry
  instance.max_otp_try = max_otp_try

  if max_otp_try == 0:
    instance.otp_max_out = timezone.now() + datetime.timedelta(hours=1)
  elif max_otp_try == -1:
    instance.max_otp_try = 3
  else:
    instance.otp_max_out = None
    instance.max_otp_try = max_otp_try
  
  instance.save()

  print(instance.otp, 'OTP', instance.identifier)
  # send otp here
  return Response("Successfully generated OTP", status=status.HTTP_200_OK)