import logging
import socket
from django.conf import settings
from django.http import Http404
import monetdb.control

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

    return statuses


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
            databases.append({'name': dbname, 'type': 'postgresql'})
    return databases


def check_database(db_name):
    if db_name not in settings.DATABASES:
        raise Http404