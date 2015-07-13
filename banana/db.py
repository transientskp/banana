import logging
import socket
from django.conf import settings
from django.http import Http404
import pymonetdb.control
import datetime


logger = logging.getLogger(__name__)

status_map = {
    1: 'running',
    2: '?',
    3: 'stopped',
}


def monetdb_list(host, port, passphrase):
    """
    returns a list of MonetDB databases
    """
    try:
        monetdb_control = monetdb.control.Control(host, port, passphrase)
        statuses = monetdb_control.status()
    except socket.error as e:
        logger.error(str(e))
        statuses = []

    for status in statuses:
        status['status'] = status_map[status['state']]
        status['type'] = 'monetdb'

        # convert to datetime objects
        for field in ['last_crash', 'last_start']:
            if status[field] > 0:
                status[field] = datetime.datetime.fromtimestamp(status[field])
            else:
                status[field] = ""
    return statuses


def postgres_list(host, user, password, port=5432):
    import psycopg2
    con = psycopg2.connect(host=host, port=port, user=user, password=password,
                           dbname='postgres')
    cur = con.cursor()
    cur.execute("select datname from pg_database")
    names = [n[0] for n in cur.fetchall()]
    system = ["template1", "template0", "postgres"]
    names = [n for n in names if n not in system]
    return names


def list():
    """
    :return: a list of all configured databases
    """
    if not hasattr(settings, 'MONETDB_HOST') or not settings.MONETDB_HOST:
        # no monetdb database configureds
        databases = []
    else:
        databases = monetdb_list(settings.MONETDB_HOST, settings.MONETDB_PORT,
                                 settings.MONETDB_PASSPHRASE)
    for dbname, dbparams in settings.DATABASES.items():
        if dbparams['ENGINE'] != 'djonet' and dbname != 'default':
            path = 'postgresql://%(USER)s@%(HOST)s:%(PORT)s/%(NAME)s' % dbparams
            databases.append({'name': dbname, 'type': 'postgresql', 'path': path})
    databases.sort(key=lambda x: x['name'])
    return databases


def check_database(db_name):
    """
    check if db_name is in the Django database configuration.
    """
    if db_name not in settings.DATABASES:
        raise Http404


def db_schema_version(database_name):
    """
    Gets schema version from database. Will return error if it can't connect.

    WARNING: don't use this function in the settings file. We can't use the
    Django ORM during Django initialisation. That is also why we import the
    Version here.
    """
    from banana.models import Version
    try:
        return Version.objects.using(database_name).get().value
    except Exception as e:
        return "error"