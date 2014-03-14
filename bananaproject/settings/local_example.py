from base import *
from banana.db import monetdb_list, postgres_list


DEBUG = True
TEMPLATE_DEBUG = DEBUG

## (For developer use only)
# MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# INSTALLED_APPS += ['debug_toolbar']

SECRET_KEY = 'changeme!@'

# Change default flux display prefix / units
# (Only applies to transients_detail page, currently)
from banana.templatetags.units import units_map
units_map[None]= units_map['unity'] #(Default)
# units_map[None]=units_map['milli']

MONETDB_HOST = 'localhost'
MONETDB_PORT = 50000
MONETDB_PASSPHRASE = 'blablabla'
MONETDB_USERNAME = 'gijs'

POSTGRES_HOST = 'localhost'
POSTGRES_USERNAME = 'gijs'
POSTGRES_PASSWORD = POSTGRES_USERNAME

AUTOMATIC_DATABASE_DETECTION = True


if AUTOMATIC_DATABASE_DETECTION:
    ## Probe databases automatically at startup
    if POSTGRES_HOST:
        for name in postgres_list(POSTGRES_HOST, POSTGRES_USERNAME, POSTGRES_PASSWORD):
            DATABASES[name + "_postgres"] = {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'HOST': POSTGRES_HOST,
                'NAME': name,
                'USER': POSTGRES_USERNAME,
                'PASSWORD': POSTGRES_PASSWORD,
                'CONSOLE': False,  # True if you you want sqlconsole queries
            }

    if MONETDB_HOST:
        for monetdb in monetdb_list(MONETDB_HOST, MONETDB_PORT, MONETDB_PASSPHRASE):
            name = monetdb['name']
            DATABASES[name + "_monet"] = {
                'ENGINE': 'djonet',
                'NAME': name,
                'USER': MONETDB_USERNAME,
                'PASSWORD': MONETDB_USERNAME,
                'HOST': MONETDB_HOST,
                'PORT': MONETDB_PORT,
                'CONSOLE': True,
            }

else:
    ## Manual config. Example loops assume same username / password for all DB's
    for name in ('test', 'production'):
        DATABASES[name + "_postgres"] = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': name,
            'HOST': POSTGRES_HOST,
            'USER': POSTGRES_USERNAME,
            'PASSWORD': POSTGRES_USERNAME,
            'CONSOLE': False,  # True if you you want sqlconsole queries
        }

    for name in ('test', 'production'):
        DATABASES[name + "_monet"] = {
            'ENGINE': 'djonet',
            'NAME': name,
            'USER': MONETDB_USERNAME,
            'PASSWORD': MONETDB_USERNAME,
            'HOST': MONETDB_HOST,
            'PORT': MONETDB_PORT,
            'CONSOLE': True,
        }






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
