
from bananaproject.settings.base import *

SECRET_KEY = "NSA is watching you"

TESTING = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS += [
    'testing',
]

LOGIN_REDIRECT_URL = '/'

USE_TZ = False