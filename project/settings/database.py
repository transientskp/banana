
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
        }
    return databases


def postgresql_db_config(host, username, password, port=5432, console=True):
    """
    generates a Django DATABASE configuration dict containing all
    postgresql databases.
    """
    databases = {}
    for name in postgres_list(host, username, password):
        databases["postgres_" + name] = {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'HOST': host,
            'PORT': port,
            'NAME': name,
            'USER': name,
            'PASSWORD': name,
        }
    return databases
