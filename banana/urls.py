from django.conf.urls import patterns, url
from banana.views import etc, images, tables
from banana.views.etc import dataset


urlpatterns = patterns('',
    url(r'^$', tables.databases, name='databases'),
    url(r'^(?P<db_name>\w+)/$', tables.datasets, name='datasets'),
    url(r'^(?P<db_name>\w+)/dataset/(?P<dataset_id>\d+)/$', dataset,
        name='dataset'),
    url(r'^(?P<db_name>\w+)/images/$', tables.images, name='images'),
    url(r'^(?P<db_name>\w+)/transients/$', tables.transients,
        name='transients'),
    url(r'^(?P<db_name>\w+)/extractedsources/$', tables.extractedsources,
        name='extractedsources'),
    url(r'^(?P<db_name>\w+)/runningcatalogs/$', tables.runningcatalogs,
        name='runningcatalogs'),
    url(r'^(?P<db_name>\w+)/monitoringlists/$', tables.monitoringlists,
        name='monitoringlists'),

    url(r'^(?P<db_name>\w+)/transient/(?P<transient_id>\d+)/$', etc.transient,
        name='transient'),

    url(r'^(?P<db_name>\w+)/extractedsource/(?P<extractedsource_id>\d+)/$',
        etc.extractedsource, name='extractedsource'),
    url(r'^(?P<db_name>\w+)/runningcatalog/(?P<runningcatalog_id>\d+)/$',
        etc.runningcatalog, name='runningcatalog'),
    url(r'^(?P<db_name>\w+)/monitoringlist/(?P<monitoringlist_id>\d+)/$',
        etc.monitoringlist, name='monitoringlist'),

    url(r'^(?P<db_name>\w+)/image/(?P<image_id>\d+)/$', images.image,
        name='image'),
    url(r'^(?P<db_name>\w+)/extractedsourceplot/(?P<extractedsource_id>\d+)/$',
        images.extractedsource_plot,
        name='extractedsource_plot'),
    url(r'^(?P<db_name>\w+)/imageplot/(?P<image_id>\d+)/$',
        images.image_plot, name='image_plot'),
    url(r'^(?P<db_name>\w+)/imagedetail/(?P<image_id>\d+)/$',
        images.image_detail, name='image_detail'),
    url(r'^(?P<db_name>\w+)/transientplot/(?P<transient_id>\d+)/$',
        images.transient_plot, name='transient_plot'),
    url(r'^(?P<db_name>\w+)/lightcurveplot/(?P<runningcatalog_id>\d+)/$',
        images.lightcurve_plot, name='lightcurve_plot'),
    url(r'^(?P<db_name>\w+)/scatterplot/(?P<dataset_id>\d+)/$',
        images.scatter_plot, name='scatter_plot'),
    url(r'^(?P<db_name>\w+)/extractedsourcespx/(?P<image_id>\d+)/$',
        images.extracted_sources_pixel, name='extracted_sources_pixel'),
)
