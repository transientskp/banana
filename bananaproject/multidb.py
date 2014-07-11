"""
Select database based on URL variable

Inspired by this Django snipped:

https://djangosnippets.org/snippets/2037/

It's assumed that any view in the system with a cfg keyword argument passed to
it from the urlconf may be routed to a separate database. for example:

  url( r'^(?P<db>\w+)/account/$', 'views.account' )

The middleware and router will select a database whose alias is <db>,
"default" if no db argument is given and raise a 404 exception if not listed in
settings.DATABASES, all completely transparent to the view itself.
"""
import threading
from django.http import Http404

request_cfg = threading.local()


class MultiDbRouterMiddleware(object):
    """
    The Multidb router middelware.

    he middleware process_view (or process_request) function sets some context
    from the URL into thread local storage, and process_response deletes it. In
    between, any database operation will call the router, which checks for this
    context and returns an appropriate database alias.

    Add this to your middleware, for example:

    MIDDLEWARE_CLASSES += ['bananaproject.multidb.MultiDbRouterMiddleware']
    """
    def process_view(self, request, view_func, args, kwargs):
        if 'db' in kwargs:
            request_cfg.db = kwargs['db']
            request.SELECTED_DATABASE = request_cfg.db

    def process_response(self, request, response):
        if hasattr(request_cfg, 'db'):
            del request_cfg.db
        return response


class MultiDbRouter(object):
    """
    The multiple database router.

    Add this to your Django database router configuration, for example:

    DATABASE_ROUTERS += ['bananaproject.multidb.MultiDbRouter']
    """
    def _multi_db(self):
        from django.conf import settings
        if hasattr(request_cfg, 'db'):
            if request_cfg.db in settings.DATABASES:
                return request_cfg.db
            else:
                raise Http404
        else:
            return 'default'

    def db_for_read(self, model, **hints):
        if model._meta.app_label != 'banana':
            return 'default'
        return self._multi_db()

    db_for_write = db_for_read


def multidb_context_processor(request):
    """
    This context processor will add a db_name to the request.

    Add this to your Django context processors, for example:

    TEMPLATE_CONTEXT_PROCESSORS +=[
        'bananaproject.multidb.multidb_context_processor']
    """
    if hasattr(request, 'SELECTED_DATABASE'):
        return {'db_name': request.SELECTED_DATABASE}
    else:
        return {}
