from django.conf.urls import patterns, url
from django.conf.urls.static import static
from banana import settings
from tkpdb import views


urlpatterns = patterns('',
    url(r'^$', views.databases, name='databases'),
    url(r'^(?P<db_name>\w+)/$', views.datasets, name='datasets'),
    url(r'^(?P<db_name>\w+)/dataset/(?P<dataset_id>\d+)/$', views.dataset,
        name='dataset'),
    url(r'^(?P<db_name>\w+)/image/(?P<image_id>\d+)/$', views.image,
        name='image'),

    url(r'^(?P<db_name>\w+)/plot/(?P<image_id>\d+)/$', views.plot,
        name='plot'),

    url(r'^(?P<db_name>\w+)/images/$', views.images, name='images'),
)

if settings.DEBUG:
            urlpatterns += static(settings.STATIC_URL,
                                  document_root=settings.STATIC_ROOT)
