SQL Console
===========

This Django app is a web based SQL console to your database. Bananaproject
is configured so that it is enabled for authenticated administrators. You can
enable the SQL console per database in the settings file by adding a
`'console': True` key to the configuration, for example::

    DATABASES["trap"] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'trap',
        'USER': 'trap',
        'PASSWORD': 'secret',
        'CONSOLE': True,
    }


.. warning::

    The is no write protection in SQL Console! e.g. enabling SQL Console for a
    database gives the webinterface user the same access levels as Django,
    so if the user is a super user you can create and destroy databases and
    probably do much more harm.