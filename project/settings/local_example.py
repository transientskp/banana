from base import *
from banana.db import monetdb_list, postgres_list

# use settings below to debug the application
#DEBUG = True
#MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']
#INSTALLED_APPS += ['debug_toolbar']

TEMPLATE_DEBUG = DEBUG

# settings below is required if you run banana with WSGI
# http://stackoverflow.com/a/21005346/575524
DEBUG_TOOLBAR_PATCH_SETTINGS = False

#  always change the secret key of a django application!
SECRET_KEY = 'changeme!@'

# always set an ADMIN email adres. in case of problem used for error reporting
ADMINS += [('Administrator', 'change@me.nl'), ]

# also very important, change this to the hostname used for accessing banana
ALLOWED_HOSTS = [
    '127.0.0.1',
    'servername.nl',
]

# below is an example autoconfigure setup. It will probe PostgreSQL and
# MonetDB database servers, and will add all databases existing on these
# servers to the django database configuration. You don't have to configure
# banana like this! You can also just add the database by hand.
#
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
#
MONETDB_HOST = 'localhost'
MONETDB_PORT = 50000
MONETDB_PASSPHRASE = 'blablabla'

POSTGRES_HOST = 'localhost'
POSTGRES_USERNAME = 'gijs'
POSTGRES_PASSWORD = POSTGRES_USERNAME

for name in postgres_list(POSTGRES_HOST, POSTGRES_USERNAME, POSTGRES_PASSWORD):
    DATABASES["postgres_" + name] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': POSTGRES_HOST,
        'NAME': name,
        'USER': name,
        'PASSWORD': name,
    }

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


# mongodb is used for image storage.
MONGODB = {
    "enabled": True,
    "host": "localhost",
    "port": 27017,
    "database": "tkp"
}


# If page performance is slow, you can enable caching. to enable memcached,
# install memcached, python-memcached and python-pylibmc.
#
# https://docs.djangoproject.com/en/1.7/topics/cache/
#
#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#    }
#}