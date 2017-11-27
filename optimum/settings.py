"""
Django settings for optimum project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from credentials import *

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SETTINGS_PATH = os.path.dirname(__file__)
PROJECT_PATH = os.path.join(SETTINGS_PATH, os.pardir)
PROJECT_PATH = os.path.abspath(PROJECT_PATH)
TEMPLATES_PATH = os.path.join(PROJECT_PATH, "templates")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!rmta@tzbj5d&a%vc&_6tz&&pc82keac*9(gu#(wg+q$7zetk9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['optimum-facebook-survey.imu-projects.eu', 'localhost']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'optimum',
    #'social.apps.django_app.default',
    'social_django',
    'allauth',
    'allauth.account',
    'star_ratings',
)

MIDDLEWARE_CLASSES = (
   'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'social_django.middleware.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'optimum.urls'

WSGI_APPLICATION = 'optimum.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        #'NAME': 'dj_optimum',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
#STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'jaqpot_ui/static',
#)

#SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/'
#LOGIN_ERROR_URL    = '/login-error/'

#TEMPLATE_DIRS = (
#  'jaqpot_ui/templates',
#)

TEMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR,'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'social_django.context_processors.backends', 
            'social_django.context_processors.login_redirect',

        ],
    },
},] 

AUTHENTICATION_BACKENDS = (
   'social_core.backends.facebook.FacebookOAuth2',
   'django.contrib.auth.backends.ModelBackend',
)


SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

#SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_friends', 'user_likes', 'public_profile', 'user_about_me', 'user_likes',
#                                 'user_photos', 'user_posts', 'user_relationships','user_relationship_details',
#                                 'user_religion_politics', 'user_tagged_places', 'user_videos', 'user_website','user_work_history',
#                                 'user_birthday', 'user_education_history', 'user_events', 'user_games_activity', 'user_hometown',
#                                 'user_actions.books', 'user_actions.fitness','user_actions.music','user_actions.news',
#                                'user_actions.video']

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_likes', 'public_profile', 'user_about_me',
                                 'user_photos', 'user_posts']

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'ru_RU',
  'fields': 'id, name, email, age_range'
}

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    # Verifies that the social association can be disconnected from the current
    # user (ensure that the user login mechanism is not compromised by this
    # disconnection).
    #'social_core.pipeline.disconnect.allowed_to_disconnect',

    # Collects the social associations to disconnect.
    'social_core.pipeline.disconnect.get_entries',

    # Revoke any access_token when possible.
    'social_core.pipeline.disconnect.revoke_tokens',

    # Removes the social associations.
    'social_core.pipeline.disconnect.disconnect',
)

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

