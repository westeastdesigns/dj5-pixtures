"""
Django settings for bookmarks project.

Generated by 'django-admin startproject' using Django 5.0.6.

"""

from pathlib import Path

from decouple import config
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-#)e&e3&*ad1x%*^uq#8z(*=)(+_!o4vo=+$+s3yd2ccf)c&h%5"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["mysite.com", "localhost", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "account.apps.AccountConfig",  # local app, manages user accounts for project
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # admindocs
    "django.contrib.admindocs",
    # third-party applications
    "debug_toolbar",
    "django_extensions",
    "easy_thumbnails",
    "social_django",
    # local applications
    "actions.apps.ActionsConfig",  # provides actions for project
    "images.apps.ImagesConfig",  # manages the images for project
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
]

ROOT_URLCONF = "bookmarks.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bookmarks.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# tells Django which URL to redirect the user to after successful login, if no 'next'
#   parameter is present in the request
LOGIN_REDIRECT_URL = "dashboard"
# URL to redirect the user to log in
LOGIN_URL = "login"
# URL to redirect the user to log out
LOGOUT_URL = "logout"

# DEVELOPMENT: lets Django email to the standard output instead of through SMTP server
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# location of media files
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "account.authentication.EmailAuthBackend",
    # google social authentication backend
    "social_core.backends.google.GoogleOAuth2",
]

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("GOOGLE_OAUTH2_SECRET")

# allows a Profile object to be created in the db when a new user is created via
# social authentication
SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "account.authentication.create_profile",  # look up Profile of User, create if new
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
]

# for debugging easy-thumbnails
# THUMBNAIL_DEBUG = True

# adds a get_absolute_url() method to any of the models listed here
ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda u: reverse_lazy("user_detail", args=[u.username])
}

# Django Debug Toolbar only displays if the IP debugging from matches an entry here
INTERNAL_IPS = [
    "127.0.0.1",
]

# if MIME type errors occur, apply the correct mapping for JavaScript & CSS
# if DEBUG:
#     import mimetypes
#     mimetypes.add_type('application/javascript', '.js', True)
#     mimetypes.add_type('text/css', '.css', True)

# these settings for the Redis server integrate Redis into the project
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
