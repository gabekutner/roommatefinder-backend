"""
Django settings for roommatefinder project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
# how to run local postgres instance in docker
# https://www.sqlshack.com/getting-started-with-postgresql-on-docker/

import os
import sys
import json
from dotenv import load_dotenv
from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from roommatefinder.apps.core.versioning import get_git_changeset_timestamp

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path=env_path)

EXTERNAL_BASE = os.path.join(BASE_DIR, "externals")
EXTERNAL_LIBS_PATH = os.path.join(EXTERNAL_BASE, "libs")
EXTERNAL_APPS_PATH = os.path.join(EXTERNAL_BASE, "apps")
sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH] + sys.path


with open(os.path.join(os.path.dirname(__file__), 'sample_secrets.json'), 'r') as f:
  secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
  """Get the secret variable or return explicit exception."""
  try:
    return secrets[setting]
  except KeyError:
    error_msg = f'Set the {setting} secret variable'
    raise ImproperlyConfigured(error_msg)
  
# Utility function to parse boolean environment variables
def str_to_bool(value):
    if value.lower() in ('true', '1'):
        return True
    elif value.lower() in ('false', '0'):
        return False
    raise ValueError(f"Invalid boolean value: {value}")
  
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
  
# cors headers
CORS_ALLOW_CREDENTIALS = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

CORS_ALLOWED_ORIGINS = [
  # deprecated: from react, not needed for native
  "http://127.0.0.1:3000"
]

# SECURITY WARNING: keep the secret key used in production secret!
if str_to_bool(os.getenv('USE_SECRETS', 'true')):
  SECRET_KEY = get_secret('SECRET_KEY')
else:
  SECRET_KEY = os.getenv('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = [
  "*", # all for now
  "127.0.0.1", # local testing
]

AUTH_USER_MODEL = "api.Profile"
CORS_ORIGIN_ALLOW_ALL = True

# Application definition
INSTALLED_APPS = [
  'daphne',
  # contributed
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  # third-party
  "rest_framework",
  "corsheaders",
  "rest_framework_simplejwt",
  "rest_framework_simplejwt.token_blacklist",
  "multiselectfield",
  "django_extensions",
  # local
  "roommatefinder.apps.api"
]

REST_FRAMEWORK = {
  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
  'PAGE_SIZE': 10,
  "DATE_INPUT_FORMATS": ["%m-%d-%Y"],
  "DEFAULT_PERMISSION_CLASSES": [
    "rest_framework.permissions.AllowAny",
  ],
  "DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
  ],
}

# redis channels here ...
CHANNEL_LAYERS = {
  'default': {
    'BACKEND': 'channels_redis.core.RedisChannelLayer',
    'CONFIG': {
      # runs locally, port 6379
      'hosts': [('127.0.0.1', 6379)]
    }
  }
}

# SIMPLE JWT TO CREATE JSON ACCESS TOKENS
SIMPLE_JWT = {
  # change the expiration of the token
  "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
  "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
  "ROTATE_REFRESH_TOKENS": True,
  "BLACKLIST_AFTER_ROTATION": True,  
  "UPDATE_LAST_LOGIN": False,
  "ALGORITHM": "HS256",
  "SIGNING_KEY": SECRET_KEY,
  "VERIFYING_KEY": None,
  "AUDIENCE": None,
  "ISSUER": None,
  "JWK_URL": None,
  "LEEWAY": 0,
  "AUTH_HEADER_TYPES": ("Bearer",),
  "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
  "USER_ID_FIELD": "id",
  "USER_ID_CLAIM": "user_id",
  "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
  "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
  "TOKEN_TYPE_CLAIM": "token_type",
  "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
  "JTI_CLAIM": "jti",
  "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
  "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
  "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}


MIDDLEWARE = [
  # defaults
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  # imported
  "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'roommatefinder.urls'

# remove in production, will need replacement for admin page
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

WSGI_APPLICATION = 'roommatefinder.wsgi.application'
# daphne
ASGI_APPLICATION = "roommatefinder.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if str_to_bool(os.getenv('USE_SECRETS', 'true')):
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': get_secret('DATABASE_NAME'),
      'USER': get_secret('DATABASE_USER'),
      'PASSWORD': get_secret('DATABASE_PASSWORD'),
      'HOST': get_secret('DATABASE_HOST'),
      'PORT': get_secret('DATABASE_PORT'),
    }
  }
else:
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': os.getenv('DATABASE_NAME'),
      'USER': os.getenv('DATABASE_USER'),
      'PASSWORD': os.getenv('DATABASE_PASSWORD'),
      'HOST': os.getenv('DATABASE_HOST'),
      'PORT': os.getenv('DATABASE_PORT'),
    }
  }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# not used, remove in production
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'),]

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
# no static files are hosting on the api, remove in production

# STATICFILES_DIRS = [
#   os.path.join(BASE_DIR, 'roommatefinder', 'site_static'),
# ]

timestamp = get_git_changeset_timestamp(BASE_DIR)
STATIC_URL = f'/static/{timestamp}/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# model tuples might be better off elsewhere
POPULAR_CHOICES = ( # sample size, uofu28, 27 specific
                   ('1', 'Hanging out with friends'),
                   ('2', 'Shopping'),
                   ('3', 'Road Trips'),
                   ('4', 'Rushing'),
                   ('5', 'Reading'),
                   ('6', 'Concerts'),
                   ('7', 'Staying in'),
                   ('8', 'Going out'),
                   ('9', 'Being outside'),
                   ('10', 'Thrifting'),
                   ('11', 'Photography'),
                   ('12', 'Snowboarding'),
                   ('13', 'Skiing'),
                   ('14', 'Working out'),
                   ('15', 'Anything outdoors'),
                   ('16', 'Hiking'),
                   ('17', 'Surfing'),
                   ('18', 'Music'),
                   ('19', 'Dogs'),
                   ('20', 'Cats'),
                   ('21', 'Fishing'),
                   ('22', 'Basketball'),
                   ('23', 'Cliff Jumping'),
                   ('24', 'Church'),
                   ('25', 'Camping'),
                   ('26', 'Soccer'),
                   ('27', 'Lacrosse'),
                   ('28', 'Dirt Biking'),
                   ('29', 'Chill'),
                   ('30', 'Travel'),
                   ('31', 'Going on runs'),
                   ('32', 'Track and Field'), ('33', 'Football'), ('34', 'Baseball'), ('35', 'Cheer'),
                   ('36', 'Figure Skating'), ('37', 'Cross Country'),
                   ('38', 'Napping'),
                   ('39', 'Business Scholars'), ('40', 'Honors College'), ('41', 'ROTC'),
                   ('42', 'Rocket League'), ('43', 'Fortnite'), ('44', 'COD'),
                   ('45', 'Drinking'), ('46', 'Smoking'), ('47', 'LGBTQ+'),
                   ('48', 'Mountain Biking'), ('49', 'Rock Climbing'), ('50', 'Nature'),
                   )

DORM_CHOICES = (('1', 'Chapel Glen'), 
                ('2', 'Gateway Heights'),
                ('3' ,'Impact and Prosperity Epicenter'),
                ('4', 'Kahlert Village'),
                ('5', 'Lassonde Studios'),
                ('6', 'Officers Circle'),
                ('7', 'Sage Point'),
                ('8', 'Marriott Honors Community'),
                ('9', 'Guest House'),
                ('10', "I don't know 🤷‍♂️"))

PROMPTS = (('1', 'In one word, my friends would describe me as ...'),
           ('2', 'My ideal roommate is ...'),
           ('3', 'Hot take:'),
           ('4', 'The biggest red flag a roommate could have is ...'),
           ('5', 'The biggest green flag a roommate could have is ...'),
           ('6', 'A boundary of mine is ...'),
           ('7', 'All I ask of you is ...'),
           ('8', 'My dream career ...'),
           ('9', "If loving this is wrong, I don't want to be right ..."),
           ('10', 'My guilty pleasure is ...'),
           ('11', 'If someone broke into our dorm, my plan would be ...'),
           ('12', "Uh oh! Roommate's vape charger lit the room on fire, the first thing I'm grabbing is ..."),
           ('13', 'My parents would kill me if they found out I ...'),
           ('14', 'What would be the scariest sound to hear in your dorm room?'),
           ('15', 'The most embarrassing moment of my life was when ...'),
           ('16', 'My late night drive home along song is ...'),
           ('17', 'My ideal college day in the life looks like ...'),
           ('18', "Don't tell the RA ..."),
           ('19', 'My craziest side quest:'),
           ('20', 'My strange addiction:'),
           ('21', "I'm looking for a roommate who ..."),
           ('22', 'Weird flex:'),
           ('23', 'If I won the lottery, my first purchase would be ...'),
           ('24', 'Celebrity crush:'),
           ('25', "If I'm not in class, catch me ..."),
           ('26', "If you take my toothpaste I'll ..."),)



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# for future email account: https://youtu.be/tN2k08Gucto?si=2WCMjnvLrN6mld4w
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
if str_to_bool(os.getenv('USE_SECRETS', 'true')):
  EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
  EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
else:
  EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
  EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False