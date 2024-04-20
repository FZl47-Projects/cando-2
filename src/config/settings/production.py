from config.settings import BASE_DIR

# STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT =  '/var/www/html/cando-2/media/'
STATIC_ROOT = '/var/www/html/cando-2/static/'


DEBUG = True

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



