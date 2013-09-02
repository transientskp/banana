from django.conf.urls import patterns, url
from sqlconsole.views import SQLConsoleView


urlpatterns = patterns('',
    url(r'^(?P<db>\w+)/$', SQLConsoleView.as_view(), name='sqlconsole'),
)
