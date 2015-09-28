from django.conf.urls import patterns, url
from django.views.decorators.cache import cache_page
from banana.views import images, lists, details
from banana.views.etc import extracted_sources_pixel

# maximum cache time...

cache_time = 60*60*24*30

urlpatterns = patterns('',
    url(r'^$',
        lists.DatabaseList.as_view(),
        name='databases'),
    url(r'^(?P<db>\w+)/$',
        lists.DatasetList.as_view(),
        name='datasets'),
    url(r'^(?P<db>\w+)/images/$',
        lists.ImageList.as_view(),
        name='images'),
    url(r'^(?P<db>\w+)/newsources/$',
        lists.NewsourceList.as_view(),
        name='newsources'),
    url(r'^(?P<db>\w+)/extractedsources/$',
        lists.ExtractedsourcesList.as_view(),
        name='extractedsources'),
    url(r'^(?P<db>\w+)/varmetric/$',
        lists.VarmetricList.as_view(),
        name='varmetrics'),
    url(r'^(?P<db>\w+)/monitors/$',
        lists.MonitorList.as_view(),
        name='monitors'),
    url(r'^(?P<db>\w+)/skyregions/$',
        lists.SkyregionList.as_view(),
        name='skyregions'),
    url(r'^(?P<db>\w+)/configs/$',
        lists.ConfigList.as_view(),
        name='configs'),

    url(r'^(?P<db>\w+)/newsource/(?P<pk>\d+)/$',
        details.NewsourceDetail.as_view(),
        name='newsource'),
    url(r'^(?P<db>\w+)/dataset/(?P<pk>\d+)/$',
        details.DatasetDetail.as_view(),
        name='dataset'),
    url(r'^(?P<db>\w+)/heatmap/(?P<pk>\d+)/$',
        details.HeatmapView.as_view(),
        name='heatmap'),
    url(r'^(?P<db>\w+)/extractedsource/(?P<pk>\d+)/$',
        details.ExtractedSourceDetail.as_view(),
        name='extractedsource'),
    url(r'^(?P<db>\w+)/runningcatalog/(?P<pk>\d+)/$',
        details.RunningcatalogDetail.as_view(),
        name='runningcatalog'),
    url(r'^(?P<db>\w+)/monitor/(?P<pk>\d+)/$',
        details.MonitorDetail.as_view(),
        name='monitor'),
    url(r'^(?P<db>\w+)/image/(?P<pk>\d+)/$',
        details.ImageDetail.as_view(),
        name='image'),
    url(r'^(?P<db>\w+)/bigimage/(?P<pk>\d+)/$',
        details.BigImageDetail.as_view(),
        name='bigimage'),
    url(r'^(?P<db>\w+)/skyregion/(?P<pk>\d+)/$',
        details.SkyregionDetail.as_view(),
        name='skyregion'),



    url(r'^(?P<db>\w+)/extractedsourcespx/(?P<image_id>\d+)/$',
        extracted_sources_pixel,
        name='extracted_sources_pixel'),

    url(r'^(?P<db>\w+)/extractedsourceplot/(?P<pk>\d+)/$',
        cache_page(cache_time)(images.ExtractedSourcePlot.as_view()),
        name='extractedsource_plot'),
    url(r'^(?P<db>\w+)/imageplot/(?P<pk>\d+)/$',
        cache_page(cache_time)(images.ImagePlot.as_view()),
        name='image_plot'),
     url(r'^(?P<db>\w+)/rawimage/(?P<pk>\d+)/$',
        (images.RawImage.as_view()),
        name='rawimage'),



)
