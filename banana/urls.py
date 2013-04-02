from django.conf.urls import patterns, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('', (r'^', include('tkpdb.urls')),) + \
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

