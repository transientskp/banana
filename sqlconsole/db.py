
from django.conf import settings
from django.http import Http404


def check_database(db_name):
    """
    check if db_name is in the Django database configuration and CONSOLE = True
    """
    if db_name in settings.DATABASES:
        if "CONSOLE" in settings.DATABASES[db_name]:
            if settings.DATABASES[db_name]["CONSOLE"]:
                return
    raise Http404

