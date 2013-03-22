from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from banana import settings
from tkpdb import views
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.databases, name='databases'),
    url(r'^(?P<db_name>\w+)/$', views.datasets, name='datasets'),
    url(r'^(?P<db_name>\w+)/dataset/(?P<dataset_id>\d+)/$',
        views.dataset, name='dataset'),
    url(r'^(?P<db_name>\w+)/image/(?P<image_id>\d+)/$',
        views.image, name='image'),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
            urlpatterns += static(settings.STATIC_URL,
                                  document_root=settings.STATIC_ROOT)
