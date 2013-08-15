
from base import *

SECRET_KEY = "NSA is watching you"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS += [
    'bananatest',
]
