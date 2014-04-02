"""
Django settings for coreux project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8xk!ug+a2u+2f4-)kv2h*#_!nssov32p*(e%yk7203@!k44fbf'

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
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'sumnews',
    'registration',
)

TEMPLATE_CONTEXT_PROCESSORS = ( "django.contrib.auth.context_processors.auth",
                                "django.core.context_processors.debug",
                                "django.core.context_processors.i18n",
                                "django.core.context_processors.media",
                                "django.core.context_processors.static",
                                "django.core.context_processors.tz",
                                "django.contrib.messages.context_processors.messages",
                                "sumnews.context_processors.edition.edition_list",
                                "sumnews.context_processors.edition.selected_edition")

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "sumnews.middleware.edition.EditionMiddleware",
)

ROOT_URLCONF = 'coreux.urls'

WSGI_APPLICATION = 'coreux.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database/db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "staticfiles"),
)

TEMPLATE_DIRS = ('./templates/',)

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/'

import logging
if DEBUG:
    logging.root.setLevel(logging.INFO)
else:
    logging.root.setLevel(logging.WARNING)

editions = [
    ("bg-bg", "Български"),
    ("en-gb", "English - United Kingdom"),
    ("en-us", "English - United States"),
    ("hu-hu", "Magyar"),
    ("pt-pt", "Português - Portugal"),
    ("pt-br", "Português - Brasil"),
    ("uk-uk", "Українська"),
]

default_edition = "en-us"