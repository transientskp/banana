
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


class InvalidVarException(object):
    """
    used to make sure templates don't contain unused variables
    """
    def __mod__(self, missing):
        try:
            missing_str = unicode(missing)
        except:
            missing_str = 'Failed to create string representation'
        raise Exception('Unknown variable %r %s' % (missing, missing_str))

    def __contains__(self, search):
        if search == '%s':
            return True
        return False

TEMPLATE_DEBUG = True
TEMPLATE_STRING_IF_INVALID = InvalidVarException()

# settings this is required for surpressing 1_6.W001 warning
TEST_RUNNER = 'django.test.runner.DiscoverRunner'