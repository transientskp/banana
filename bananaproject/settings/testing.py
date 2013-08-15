
from base import *

SECRET_KEY = "NSA is watching you"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
    }
}



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gijs',
        'USER': 'gijs',
        'PASSWORD': 'gijs',
        'HOST': 'localhost',
    }
}