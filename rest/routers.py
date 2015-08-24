"""
We need to create our own REST URL router, so we can use our multi DB setup.

Use this in combination with the MultiDbMixin from banana.views.
"""
from django.conf.urls import url
from rest_framework.routers import Route, DefaultRouter
from rest_framework import views
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.urlpatterns import format_suffix_patterns


class BananaRouter(DefaultRouter):
    """
    This is just a clone of DefaultRouter, but it adds db keyword arguments
    to the keyword arguments in the URL handling. Also the APIRoot view
    is modified so it passes a db keyword to the reverse URL lookup.
    """
    routes = [
        # List route.
        Route(
            url=r'^(?P<db>\w+)/{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Detail route.
        Route(
            url=r'^(?P<db>\w+)/{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated routes.
        # Generated using @action or @link decorators on methods of the viewset.
        Route(
            url=r'^(?P<db>\w+)/{prefix}/{lookup}/{methodname}{trailing_slash}$',
            mapping={
                '{httpmethod}': '{methodname}',
            },
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]

    def get_api_root_view(self):
        """
        Return a view to use as the API root.
        """
        api_root_dict = {}
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            api_root_dict[prefix] = list_name.format(basename=basename)

        class APIRoot(views.APIView):
            _ignore_model_permissions = True

            def get(self, request, db, format=None):
                ret = {}
                for key, url_name in api_root_dict.items():
                    ret[key] = reverse(url_name, request=request, format=format,
                                       kwargs={'db': db})
                return Response(ret)
        return APIRoot.as_view()

    def get_urls(self):
        """
        Generate the list of URL patterns, including a default root view
        for the API, and appending `.json` style format suffixes.
        """
        urls = []

        if self.include_root_view:
            root_url = url(r'^(?P<db>\w+)$', self.get_api_root_view(),
                           name=self.root_view_name)
            urls.append(root_url)

        default_urls = super(DefaultRouter, self).get_urls()
        urls.extend(default_urls)

        if self.include_format_suffixes:
            urls = format_suffix_patterns(urls)

        return urls
