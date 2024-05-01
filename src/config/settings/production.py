import os
from config.settings import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
	'PASSWORD': os.environ.get('DB_PASSWORD'),
	'HOST': os.environ.get('DB_HOST'),
	'PORT': os.environ.get('DB_PORT'),

    }
}



# STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT =  '/var/www/html/cando-2/media/'
STATIC_ROOT = '/var/www/html/cando-2/static/'

DEBUG = False

HOST_ADDRESS = 'http://app.candoocomplex.com' # without slash

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['http://app.candoocomplex.com']

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

LOGGING = {
    # TODO: add formatters
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR.parent / 'logs/server.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}



Q_CLUSTER = {
    'name': 'django-q',
    'timeout': 60,
    'redis': {
      'host': '127.0.0.1',
      'port': 6379,
      'db': 10,
   }
}


REDIS_CONFIG = {
    'HOST': 'localhost',
    'PORT': '6379'
}

