import os
here = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = []


MANAGERS = ADMINS


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(here, '../../default.db'),
    }
}


TIME_ZONE = 'Europe/Amsterdam'


LANGUAGE_CODE = 'en-us'

SITE_ID = 1


USE_I18N = True


USE_L10N = True


USE_TZ = True


MEDIA_ROOT = ''


MEDIA_URL = ''


STATIC_ROOT = os.path.join(here, '../../static')


STATIC_URL = '/static/'


STATICFILES_DIRS = ()


STATICFILES_FINDERS = (
    #'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'banana.urls'


WSGI_APPLICATION = 'banana.wsgi.application'


TEMPLATE_DIRS = ()


INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'tkpdb',
]


INTERNAL_IPS = ['127.0.0.1',]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

