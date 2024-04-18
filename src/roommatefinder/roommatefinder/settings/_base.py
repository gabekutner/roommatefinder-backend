"""
Django settings for roommatefinder project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
import json
from datetime import timedelta

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from roommatefinder.apps.core.versioning import get_git_changeset_timestamp

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
  
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
  
# cors headers
CORS_ALLOW_CREDENTIALS = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

CORS_ALLOWED_ORIGINS = [
  "http://127.0.0.1:3000"
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
  "*",
  "127.0.0.1",
  "0.0.0.0",
]

AUTH_USER_MODEL = "api.Profile"
CORS_ORIGIN_ALLOW_ALL = True

# Application definition
INSTALLED_APPS = [
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
  "DEFAULT_PERMISSION_CLASSES": [
    "rest_framework.permissions.AllowAny",
  ],
  "DEFAULT_AUTHENTICATION_CLASSES": [
    "rest_framework_simplejwt.authentication.JWTAuthentication",
  ],
}

# redis channels here ...

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
# ASGI_APPLICATION = "roommatefinder.asgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

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

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale'),]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_DIRS = [
  os.path.join(BASE_DIR, 'roommatefinder', 'site_static'),
]

timestamp = get_git_changeset_timestamp(BASE_DIR)
STATIC_URL = f'/static/{timestamp}/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


INTEREST_CHOICES = (('1', 'Road Trips'), ('2', 'Second-hand apparel'), ('3', 'Country Music'),
                    ('4', 'Football'), ('5', 'Snowboarding'), ('6', 'Skiing'),
                    ('7', 'Festivals'), ('8', 'Crossfit'), ('9', 'K-Pop'),
                    ('10', 'Reading'), ('11', 'Sports'), ('12', 'Photography'),
                    ('13', 'Shopping'), ('14', 'Collecting'), ('15', 'Clubbing'),
                    ('16', 'Cars'), ('17', 'Boba Tea'), ('18', 'Rugby'),
                    ('19', 'Boxing'), ('20', 'Self Care'), ('21', 'Meditation'),
                    ('22', 'Sneakers'), ('23', 'Movies'), ('24', 'Home Workout'),
                    ('25', 'Basketball'), ('26', 'Running'), ('27', 'Hockey'),
                    ('28', 'Gym'), ('29', 'Skincare'), ('30', 'Skateboarding'),
                    ('31', 'Singing'), ('32', 'Stand up Comedy'), ('33', 'Coffee'),
                    ('34', 'Fortnite'), ('35', 'Poetry'), ('36', 'Karaoke'),
                    ('37', 'Jiu-jitsu'), ('38', 'Investing'), ('39', 'Ice Skating'),
                    ('40', 'Pilates'), ('41', 'Cheerleading'), ('42', 'Content Creation'),
                    ('43', 'E-Sports'), ('44', 'Binge-Watching TV shows'), ('45', 'Cosplay'),
                    ('46', 'Motor Sports'), ('47', 'Bicycle Racing'), ('48', 'Surfing'),
                    ('49', 'Bowling'), ('50', 'Painting'), ('51', 'Songwriter'),
                    ('52', 'Motorcycles'), ('53', 'Astrology'), ('54', 'Cooking'),
                    ('55', 'Soccer'), ('56', 'Dancing'), ('57', 'Gardening'),
                    ('58', 'Politics'), ('59', 'Art'), ('60', 'Real Estate'),
                    ('61', 'Podcasts'), ('62', 'Volunteering'), ('63', 'Board Games'),
                    ('64', 'Drummer'), ('65', 'Drawing'), ('66', 'Electronic Music'),
                    ('67', 'Writing'), ('68', 'Martial Arts'), ('69', 'Marvel'),
                    ('70', 'Volleyball'), ('71', 'Band'), ('72', 'Ballet'),
                    ('73', 'Baseball'), ('74', 'Sailing'), ('75', 'Mountains'),
                    ('76', 'Hiking'), ('77', 'Concerts'), ('78', 'Climbing'),
                    ('79', 'Fishing'), ('80', 'Backpacking'), ('81', 'Camping'),
                    ('82', 'Baking'), ('83', 'Cycling'), ('84', 'Fashion'),
                    ('85', 'Blogging'), ('86', 'Active Lifestyle'), ('87', 'Outdoors'),
                    ('88', 'Anime'), ('89', 'Stocks'), ('90', 'Comedy'),
                    ('91', 'Triathlon'), ('92', 'Swimming'), ('93', 'Music'),
                    ('94', 'Yoga'), ('95', 'Gymnastics'), ('96', 'Freelance'),
                    ('97', 'Guitarist'), ('98', 'Gospel'), ('99', 'House Parties'),
                    ('100', 'Heavy Metal'), ('101', 'Live Music'), ('102', 'Frat'),
                    ('103', 'Sorority'), ) 

TEST_CHOICES = (# activities
                ('1', 'Shopping'), ('2', 'Partying'), ('3', 'Travel'),
                ('4', 'Cooking'), ('5', 'Photography'), ('6', 'Volunteering'),
                ('7', 'Entrepreneurship'), ('8', 'Coding'), ('9', 'Buy/Sell'),
                ('10', 'On-campus Events'), ('11', 'Greek Life'),
                # entertainment
                ('12', 'Concerts'), ('13', 'Festivals'), ('14', 'Music'),
                ('15', 'Movies'), ('16', 'TV/Streaming'), ('17', 'Video Games'),
                ('18', 'UFC'), ('19', 'Fortnite'), ('20', 'NFL'),
                ('21', 'NCAA Football'), ('22', 'NBA'), ('23', 'MLB'),
                ('24', 'NHL'), ('25', 'Call of Duty'),
                # lifestyle
                ('26', 'Fitness'), ('27', 'Food'), ('28', 'Playing Music'), 
                ('29', 'Memes'), ('30', 'Bargain Hunting'), ('31', 'Activism'),
                ('32', 'Beauty/Makeup'), ('33', 'Republican'), ('34', 'Fashion'),
                ('35', 'Democrat'), ('36', 'Streetwear'),
                # Outdoors
                ('37', 'Hiking'), ('38', 'Biking'), ('39', 'Camping'),
                ('40', 'Jogging'), ('41', 'Skiing/Snowboarding'), ('42', 'Surfing'),
                ('43', 'Hunting/Fishing'),
                # Sports
                ('44', 'Basketball'), ('45', 'Golf'), ('46', 'Tennis'),
                ('47', 'Soccer'), ('48', 'Baseball/Softball'), ('49', 'Volleyball'),
                ('50', 'Hockey'), ('51', 'Ultimate Frisbee'),)

CHOICES = (('1', 'Fraternity'), ('2', 'Sorority'), ('3', 'Travel'),
           ('4', 'Biking'), ('5', 'Skiing'), ('6', 'Snowboarding'),
           ('7', 'Camping'), ('8', 'Partying'), ('9', 'House Parties'),
           ('10', 'Staying in'), ('11', 'Staying out'), ('12', 'Movies'),
           ('13', 'Rock Climbing'), ('14', 'Greek Life'), ('15', 'Shopping'),
           ('16', 'Concerts'), ('17', 'Festivals'), ('18', 'NCAA Sports'),
           ('19', 'Food'), ('20', 'Politics'), ('21', 'On-campus Events'),
           ('22', 'Surfing'), ('23', 'Reading'), ('24', 'Photography'),
           ('25', 'DJ'), ('26', 'Comedy'), ('27', 'Band'),
           ('28', 'Drawing'), ('29', 'Cooking'), ('30', 'Baseball'),
           ('31', 'Lacrosse'), ('32', 'Football'), ('33', 'Golf'),
           ('34', 'Softball'), ('35', 'Soccer'), ('36', 'Volleyball'),
           ('37', 'Ultimate Frisbee'), ('38', 'Tennis'), ('39', 'Boxing'),
           ('40', 'Martial Arts'), ('41', 'Memes'), ('42', 'Fortnite'),
           ('43', 'Call of Duty'),)


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
                   # sports
                   ('32', 'Track and Field'), ('33', 'Football'), ('34', 'Baseball'), ('35', 'Cheer'),
                   ('36', 'Figure Skating'), ('37', 'Cross Country'),
                   ('38', 'Napping'),
                   ('39', 'Business Scholars'), ('40', 'Honors College'), ('41', 'ROTC'),
                   ('42', 'Rocket League'), ('43', 'Fortnite'), ('44', 'COD'),
                   # funny (transparent)
                   ('45', 'Drinking'), ('46', 'Smoking'), ('47', 'LGBTQ+'),
                   ('48', 'Mountain Biking'), ('49', 'Rock Climbing'), ('50', 'Nature'),
                   )

DORM_CHOICES = (('1', 'Chapel Glen'), 
                ('2', 'Gateway Heights'),
                ('3', 'Impact and Prosperity Epicenter'),
                ('4', 'Kahlert Village'),
                ('5', 'Lassonde Studios'),
                ('6', 'Officers Circle'),
                ('7', 'Sage Point'),
                ('8', 'Marriott Honors Community'),
                ('9', 'Guest House'),
                ('10', 'Off Campus'), )

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# EMAIL_HOST = get_secret("EMAIL_HOST")
# EMAIL_PORT = get_secret("EMAIL_PORT")
# EMAIL_HOST_USER = get_secret("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = get_secret("EMAIL_HOST_PASSWORD")
