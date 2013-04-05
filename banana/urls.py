from django.conf.urls import patterns, url
from banana import views


urlpatterns = patterns('',
    url(r'^$', views.databases, name='databases'),
    url(r'^(?P<db_name>\w+)/$', views.datasets, name='datasets'),
    url(r'^(?P<db_name>\w+)/dataset/(?P<dataset_id>\d+)/$', views.dataset,
        name='dataset'),
    url(r'^(?P<db_name>\w+)/image/(?P<image_id>\d+)/$', views.image,
        name='image'),
    url(r'^(?P<db_name>\w+)/images/$', views.images, name='images'),
    url(r'^(?P<db_name>\w+)/transients/$', views.transients, name='transients'),
    url(r'^(?P<db_name>\w+)/transient/(?P<transient_id>\d+)/$', views.transient,
        name='transient'),

    url(r'^(?P<db_name>\w+)/nsourcesplot/(?P<image_id>\d+)/$',
        views.nsources_plot, name='nsources_plot'),
    url(r'^(?P<db_name>\w+)/transientplot/(?P<transient_id>\d+)/$',
        views.transient_plot, name='transient_plot'),
    url(r'^(?P<db_name>\w+)/scatterplot/(?P<dataset_id>\d+)/$',
        views.scatter_plot, name='scatter_plot'),
)

