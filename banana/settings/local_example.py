
from base import *
from tkpdb.util import monetdb_list


DEBUG = True
TEMPLATE_DEBUG = DEBUG


# We <3 django debug toolbar
# pip install django-debug-toolbar
MIDDLEWARE_CLASSES += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INSTALLED_APPS += ['debug_toolbar']

SECRET_KEY = ''


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

ADMINS += [('Gijs Molenaar', 'bill@microsoft.com'),]


MONGODB = {
    "enabled": True,
    "host": "localhost",
    "port": 27017,
    "database": "tkp"
}