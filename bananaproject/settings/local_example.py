
from base import *
from banana.db import monetdb_list, postgres_list


DEBUG = True

TEMPLATE_DEBUG = DEBUG

## (For developer use only)
# MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# INSTALLED_APPS += ['debug_toolbar']

SECRET_KEY = 'changeme!@'

MONETDB_HOST = 'localhost'
MONETDB_PORT = 50000
MONETDB_PASSPHRASE = 'blablabla'
MONETDB_USERNAME = 'gijs'

POSTGRES_HOST = 'localhost'
POSTGRES_USERNAME = 'gijs'
POSTGRES_PASSWORD = POSTGRES_USERNAME

## Manual config. Example loops assume same username / password for all DB's

for pg_db_name in ('test', 'production'):
    DATABASES["pg_"+pg_db_name] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': POSTGRES_HOST,
        'NAME': pg_db_name,
        'USER': POSTGRES_USERNAME,
        'PASSWORD': POSTGRES_USERNAME,
        'CONSOLE': False,  # True if you you want sqlconsole queries
    }

for monetdb_name in ('test', 'production'):
    DATABASES['mn_'+monetdb_name] = {
        'ENGINE': 'djonet',
        'NAME': monetdb_name,
        'USER': MONETDB_USERNAME,
        'PASSWORD': MONETDB_USERNAME,
        'HOST': MONETDB_HOST,
        'PORT': MONETDB_PORT,
        'CONSOLE': True,
    }



## Experimental autodetection; not currently supported.
# for name in postgres_list(POSTGRES_HOST, POSTGRES_USERNAME, POSTGRES_PASSWORD):
#     DATABASES["postgres_" + name] = {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'HOST': POSTGRES_HOST,
#         'NAME': name,
#         'USER': name,
#         'PASSWORD': name,
#         'CONSOLE': False,  # True if you you want sqlconsole queries
#     }
#
#
#
# for monetdb in monetdb_list(MONETDB_HOST, MONETDB_PORT, MONETDB_PASSPHRASE):
#     name = monetdb['name']
#     DATABASES[name] = {
#         'ENGINE': 'djonet',
#         'NAME': name,
#         'USER': name,
#         'PASSWORD': name,
#         'HOST': MONETDB_HOST,
#         'PORT': MONETDB_PORT,
#         'CONSOLE': True,
#     }


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