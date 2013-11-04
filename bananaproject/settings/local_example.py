
from base import *
from database import update_config


DEBUG = True

TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INSTALLED_APPS += ['debug_toolbar']

SECRET_KEY = 'changeme!@'

# Set this to True if you want to automatically configure all reachable DB's
# You need to set the MONETDB_* and POSTGRES_ settings below also.
DATABASE_AUTOCONFIG = True

MONETDB_HOST = 'localhost'
MONETDB_PORT = 50000
MONETDB_PASSPHRASE = 'blablabla'

POSTGRES_HOST = 'localhost'
POSTGRES_USERNAME = 'gijs'
POSTGRES_PASSWORD = POSTGRES_USERNAME

update_config()

ADMINS += [('Gijs Molenaar', 'bill@microsoft.com'), ]

MONGODB = {
    "enabled": True,
    "host": "localhost",
    "port": 27017,
    "database": "tkp"
}

ALLOWED_HOSTS = [
    '127.0.0.1',
    'servername.nl',
]

## to enable memcached, install memcached, python-memcached and python-pylibmc.
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}