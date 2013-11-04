
from banana.db import monetdb_list, postgres_list


def monetdb_db_config(host, port, passphrase, console=True):
    """
    generates a Django DATABASE configuration dict containing all
    MonetDB databases.
    """
    databases = {}
    for monetdb in monetdb_list(host, port, passphrase):
        name = monetdb['name']
        databases[name] = {
            'ENGINE': 'djonet',
            'NAME': name,
            'USER': name,
            'PASSWORD': name,
            'HOST': host,
            'PORT': port,
            'CONSOLE': console,
        }
    return databases


def postgresql_db_config(host, username, password):
    """
    generates a Django DATABASE configuration dict containing all
    postgresql databases.
    """
    databases = {}
    for name in postgres_list(host, username, password):
        databases["postgres_" + name] = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': name,
            'USER': name,
            'PASSWORD': name,
            'CONSOLE': True,
        }
    return databases


def update_config():
    """
    This will autoconfigure the django database configuration. It will
    enable all MonetDB and PostgreSQL databases reachable with the credentials
    set in the Django settings.
    """
    # we need to import this here since this module is used in the settings
    from django.conf import settings
    if not hasattr(settings, 'DATABASE_AUTOCONFIG') \
           or not settings.DATABASE_AUTOCONFIG:
        return
    settings.DATABASES.update(monetdb_db_config(settings.MONETDB_HOST,
                                                settings.MONETDB_PORT,
                                                settings.MONETDB_PASSPHRASE))
    settings.DATABASES.update(postgresql_db_config(settings.POSTGRES_HOST,
                                                   settings.POSTGRES_USERNAME,
                                                   settings.POSTGRES_PASSWORD))