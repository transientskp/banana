
from base import *
from banana.db import monetdb_list


DEBUG = True
TEMPLATE_DEBUG = DEBUG


# We <3 django debug toolbar
# pip install django-debug-toolbar
MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INSTALLED_APPS += ['debug_toolbar']

SECRET_KEY = 'p$3h$l)zt^t=14!hcx-m!%&amp;!8qt#0w(1a!ca3z%-jdsw872%in'


MONETDB_HOST = 'localhost'
MONETDB_PORT = 50000
MONETDB_PASSPHRASE = 'testdb'


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

ADMINS += [('Gijs Molenaar', 'gijs@pythonic.nl'),]


MONGODB = {
    "enabled": True,
    "host": "localhost",
    "port": 27017,
    "database": "tkp"
}

STATIC_SERVE = False