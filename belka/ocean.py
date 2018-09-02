from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'belka_database',
        'USER': 'belka_user',
        'PASSWORD': 'belka_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/root/static/'
MEDIA_ROOT = '/root/media/'

SITE_URL = 'http://159.65.15.112'
