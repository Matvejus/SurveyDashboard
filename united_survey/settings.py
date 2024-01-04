import django_heroku
from pathlib import Path
# in production .env file will be used to keep valuable params.
from dotenv import load_dotenv
import os
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# Stored in .env (in production)
SECRET_KEY = 'CONESU'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 1
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [

    # my apps:
    'organization',
    'info_pages',
    'users',
    'djf_surveys',

    # apps:
    'jquery',
    'bootstrap5',
    'django_extensions',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

AUTH_USER_MODEL = "users.CustomUser"
LOGIN_REDIRECT_URL = 'users:redirectgroup'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'united_survey.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "organization" / "templates" / "organization",
            BASE_DIR / "organization" / "static" / "organization",
            BASE_DIR / "Survey" / "static" / "Survey",
            BASE_DIR / "info_pages" / "templates" / "static",
            BASE_DIR / "surveydashboard" / "djf_surveys" / "templates",
            BASE_DIR / "djf_surveys" / "templates" / "djf_surveys",

        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'djf_surveys.context_processors.surveys_context'
            ],
        },
    },
]


WSGI_APPLICATION = 'united_survey.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
     "default": {
         "ENGINE": "django.db.backends.mysql",
         "NAME": "conesuproject",
         "USER": "root",
         "HOST": "127.0.0.1",
         "PORT": 3306,
         "PASSWORD": "Password@123",
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / "uploads/"
MEDIA_URL = "/user-media/"

SURVEY_USER_PHOTO_PROFILE = "self.CustomUser.avatar.url"


django_heroku.settings(locals())
