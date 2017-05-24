"""
Django settings for optimum project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!rmta@tzbj5d&a%vc&_6tz&&pc82keac*9(gu#(wg+q$7zetk9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


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
    'social.apps.django_app.default',
    'allauth',
    'allauth.account',
    'star_ratings',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/accounts/login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
#LOGIN_ERROR_URL    = '/login-error/'

#TEMPLATE_DIRS = (
#  'jaqpot_ui/templates',
#)

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
   'django.core.context_processors.request',
)

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.facebook.FacebookAppOAuth2',
   'social.backends.google.GoogleOAuth2',
   'social.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
)

TWITTER_CONSUMER_KEY         = 'm69DRR5qxEl8DDYzmNkOgI3dX'
TWITTER_CONSUMER_SECRET      = 'gHtJr6z7qlJxBI6XqWJ8NTi9kAQxpFJ0TKSlBSR0vnSMGSOYY4'
SOCIAL_AUTH_FACEBOOK_KEY     = '188714861496456'
SOCIAL_AUTH_FACEBOOK_SECRET  = '95071c9888bb7bbad4b695c9271feb61'
GOOGLE_CONSUMER_KEY          = 'anonymous'
GOOGLE_CONSUMER_SECRET       = 'anonymous'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '627494330377-i453drmks3pp1hr78m3hb7bct0etpvja.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '4LqzCRH2x-m-kHaoiTqTEVE9'



SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'ru_RU',
  'fields': 'id, name, email, age_range'
}

FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'user_friends', 'user_likes', 'public_profile', 'user_about_me', 'user_likes',
                                 'user_photos', 'user_posts', 'user_relationships','user_relationship_details',
                                 'user_religion_politics', 'user_tagged_places', 'user_videos', 'user_website','user_work_history',
                                 'user_birthday', 'user_education_history', 'user_events', 'user_games_activity', 'user_hometown',
                                 'user_actions.books', 'user_actions.fitness','user_actions.music','user_actions.news',
                                'user_actions.video']


STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

# Google OAuth2 (google-oauth2)
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
'https://www.googleapis.com/auth/userinfo.email',
'https://www.googleapis.com/auth/userinfo.profile'
]

# Google+ SignIn (google-plus)
SOCIAL_AUTH_GOOGLE_PLUS_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_PLUS_SCOPE = [
'https://www.googleapis.com/auth/plus.login',
'https://www.googleapis.com/auth/userinfo.email',
'https://www.googleapis.com/auth/userinfo.profile'
]

SOCIAL_AUTH_GOOGLE_OAUTH2_USE_DEPRECATED_API = True
SOCIAL_AUTH_GOOGLE_PLUS_USE_DEPRECATED_API = True
