
from base import *
from banana.db import monetdb_list

DEBUG = True

TEMPLATE_DEBUG = DEBUG

MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INSTALLED_APPS += ['debug_toolbar']

SECRET_KEY = 'changeme!@'

MONETDB_HOST = 'localhost'
MONETDB_PORT = 50000
MONETDB_PASSPHRASE = 'blablabla'

for monetdb in monetdb_list(MONETDB_HOST, MONETDB_PORT, MONETDB_PASSPHRASE):
    name = monetdb['name']
    DATABASES[name] = {
        'ENGINE': 'djonet',
        'NAME': name,
        'USER': name,
        'PASSWORD': name,
        'HOST': MONETDB_HOST,
        'PORT': MONETDB_PORT,
    }

DATABASES['postgres_you'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'you',
        'USER': 'you',
        'PASSWORD': 'you',
        'HOST': 'localhost',
}  # add 'CONSOLE': True if you want to be able to perform sqlconsole queries

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