"""
  using Django 4.2.10
"""

import os
from django.utils.translation import gettext_lazy as _
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = int(os.getenv('DEBUG', 1))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED', 'http://127.0.0.1').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party modules
    'django_render_partial',
    'phonenumber_field',
    'django_q',

    # Apps
    'apps.public',
    'apps.core',
    'apps.account',
    'apps.notification',
    'apps.dashboard',
    'apps.product',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'custom_tags': 'apps.core.templatetags.custom_tags'
            }
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGES = [
    ("fa", _("Persian")),
]

LOCALE_PATHS = [
    os.getenv('LOCALE_PATHS', BASE_DIR / 'locale'),
]

LANGUAGE_CODE = "fa-ir"

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = False

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'account.User'  # custom user model
LOGIN_URL = '/u/login-register'

COMMON_ADMIN_USER_ROLES = [
    'operator_user'
]

SUPER_ADMIN_ROLES = [
    'super_user'
]

ADMIN_USER_ROLES = [
    *COMMON_ADMIN_USER_ROLES,
    *SUPER_ADMIN_ROLES
]

USER_ROLES = [
    *ADMIN_USER_ROLES,
    'normal_user',
]

Q_CLUSTER = {
    'name': 'django-q',
    'timeout': 60,
    'orm': 'default'
}

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

REDIS_CONFIG = {
    'HOST': 'localhost',
    'PORT': '6379'
}

RESET_PASSWORD_CONFIG = {
    'TIMEOUT': 300,  # by sec
    'CODE_LENGTH': 6,
    'STORE_BY': 'reset_password_phonenumber_{}'
}

CONFIRM_PHONENUMBER_CONFIG = {
    'TIMEOUT': 300,  # by sec
    'CODE_LENGTH': 6,
    'STORE_BY': 'confirm_phonenumber_{}'
}

SMS_CONFIG = {
    'API_KEY': os.environ.get('SMS_API_KEY'),
    'API_URL': 'http://rest.ippanel.com/v1/messages/patterns/send',
    'ORIGINATOR': '983000505'
}
