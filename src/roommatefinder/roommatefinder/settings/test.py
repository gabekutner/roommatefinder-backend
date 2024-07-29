import os
from ._base import *

if os.environ.get('GITHUB_WORKFLOW'):
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql',
      'NAME': 'github_actions',
      'USER': 'postgres',
      'PASSWORD': 'postgres',
      'HOST': '127.0.0.1',
      'PORT': '5432',
    }
  }