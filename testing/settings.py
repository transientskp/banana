
from project.settings.base import *

SECRET_KEY = "NSA is watching you"


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

DEBUG = True

TEMPLATE_DEBUG = True


# settings this is required for surpressing 1_6.W001 warning
TEST_RUNNER = 'django.test.runner.DiscoverRunner'