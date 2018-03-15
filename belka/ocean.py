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
STATIC_ROOT = '/home/dev/static/'
MEDIA_ROOT = '/home/dev/media/'

SITE_URL = 'http://188.166.81.158'
