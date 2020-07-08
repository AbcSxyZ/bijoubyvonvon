"""
Django settings for bijouvonvon project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import glob

#####################
## Django settings ##
#####################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ADMINS = [("Simon", "rossi.sim@outlook.com")]
LOG_FILE = "/var/log/apache2/django-error.log"

LIST_HOSTS = os.environ["DOMAINS"].split(" ")

if DEBUG == False:
    ALLOWED_HOSTS = []
    for host in LIST_HOSTS:
        ALLOWED_HOSTS.extend([host, "www." + host])
else:
    ALLOWED_HOSTS = LIST_HOSTS


# Application definition

INSTALLED_APPS = [
    #Default apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Custom apps
    'jewelry.apps.JewelryConfig',
    'stands.apps.StandsConfig',
    'leaflet.apps.LeafletConfig',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'jewelry.middleware.ExceptionMiddleware',
]

ROOT_URLCONF = 'bijouvonvon.urls'

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

                #Custom settings
                'jewelry.context_processor.template_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'bijouvonvon.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ["DB_NAME"],
        "HOST": os.environ["DOCKER_MYSQL_CONTAINER"],
        "PORT": os.environ["DB_PORT"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASS"],
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Security variables
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/



#####################
## Custom Settings ##
#####################

MATOMO_DOMAIN_PATH = "{}:8080".format(ALLOWED_HOSTS[0])

# Configuration for mail
EMAIL_HOST = os.environ["MAIL_HOST"]
EMAIL_USE_TLS = True
EMAIL_PORT = os.environ["MAIL_PORT"]
EMAIL_HOST_USER = os.environ["MAIL_USER"]
EMAIL_HOST_PASSWORD = os.environ["MAIL_PASS"]

# Filesystem customization

#Default filesystem
DEFAULT_FILE_STORAGE = "jewelry.file_storage.JewelryFileStorage"
DEFAULT_STORAGE_IMAGE_SIZE = (1000, 1000)

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Some custom directory to collect staticfiles
STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "staticfiles"),
        ]

# Personnal filesystem with CustomMediaStorage.
# Config of the filesystem

CUSTOM_MEDIA_URL = "/custom-media/"
CUSTOM_MEDIA_ROOT = os.path.join(BASE_DIR, "custom-media")
CUSTOM_STORAGE_IMAGE_SIZE = (2500, 2500)

# Pattern for CustomMedia of editable files
HEADER_IMAGE = "homepage_image.*"
PROFIL_IMAGE = "profil_image.*"

# Description file location for edition
DESCRIPTION_FILE = "description.txt"
DESCRIPTION_FILE = os.path.join(BASE_DIR, DESCRIPTION_FILE)