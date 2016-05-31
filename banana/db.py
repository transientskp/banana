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
        monetdb_control = pymonetdb.control.Control(host, port, passphrase)
        statuses = monetdb_control.status()
    except socket.error as e:
        logger.error(str(e))
        statuses = []

    for status in statuses:
        status['status'] = status_map[status['state']]
        status['type'] = 'monetdb'
        status['owner'] = 'unknown'  # we can't figure out who is the owner for MonetDB

        # convert to datetime objects
        for field in ['last_crash', 'last_start']:
            if status[field] > 0:
                status[field] = datetime.datetime.fromtimestamp(status[field])
            else:
                status[field] = ""
    return statuses


def postgres_list(host, user, password, port=5432):
    """
    List all non system databases

    returns: a list of tuples (name, owner) for each database
    """
    import psycopg2
    con = psycopg2.connect(host=host, port=port, user=user, password=password,
                           dbname='postgres')
    cur = con.cursor()
    q = """
SELECT pg_database.datname as "name",
       pg_user.usename as "owner"
FROM pg_database, pg_user
WHERE pg_database.datdba = pg_user.usesysid
AND datistemplate = false;
    """
    cur.execute(q)
    system = ["template1", "template0", "postgres"]

    result = []
    for name, owner in cur.fetchall():
        if name not in system:
            result.append((name, owner))
    return result


def list():
    """
    :return: a list of all configured databases
    """
    if not hasattr(settings, 'MONETDB_HOST') or not settings.MONETDB_HOST:
        # no monetdb database configured
        databases = []
    else:
        databases = monetdb_list(settings.MONETDB_HOST, settings.MONETDB_PORT,
                                 settings.MONETDB_PASSPHRASE)
    for dbname, dbparams in settings.DATABASES.items():
        if dbparams['ENGINE'] != 'djonet' and dbname != 'default':
            path = 'postgresql://%(USER)s@%(HOST)s:%(PORT)s/%(NAME)s' % dbparams
            databases.append({'name': dbname, 'type': 'postgresql', 'path': path, 'owner': dbparams['OWNER']})
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
