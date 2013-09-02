from django.conf.urls import patterns, url
from sqlconsole.views import SQLConsoleView


urlpatterns = patterns('',
    url(r'^$', SQLConsoleView.as_view(), name='sqlconsole'),
)
