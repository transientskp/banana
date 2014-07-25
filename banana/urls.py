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
    url(r'^(?P<db>\w+)/transients/$',
        lists.TransientList.as_view(),
        name='transients'),
    url(r'^(?P<db>\w+)/assocxtrsources/$',
        lists.AssocxtrsourceList.as_view(),
        name='assocxtrsources'),
    url(r'^(?P<db>\w+)/extractedsources/$',
        lists.ExtractedsourcesList.as_view(),
        name='extractedsources'),
    url(r'^(?P<db>\w+)/runningcatalogs/$',
        lists.RunningcatalogList.as_view(),
        name='runningcatalogs'),
    url(r'^(?P<db>\w+)/monposs/$',
        lists.MonposList.as_view(),
        name='monposs'),


    url(r'^(?P<db>\w+)/transient/(?P<pk>\d+)/$',
        details.TransientDetail.as_view(),
        name='transient'),
    url(r'^(?P<db>\w+)/dataset/(?P<pk>\d+)/$',
        details.DatasetDetail.as_view(),
        name='dataset'),
    url(r'^(?P<db>\w+)/extractedsource/(?P<pk>\d+)/$',
        details.ExtractedSourceDetail.as_view(),
        name='extractedsource'),
    url(r'^(?P<db>\w+)/runningcatalog/(?P<pk>\d+)/$',
        details.RunningcatalogDetail.as_view(),
        name='runningcatalog'),
    url(r'^(?P<db>\w+)/image/(?P<pk>\d+)/$',
        details.ImageDetail.as_view(),
        name='image'),
    url(r'^(?P<db>\w+)/bigimage/(?P<pk>\d+)/$',
        details.BigImageDetail.as_view(),
        name='bigimage'),

    url(r'^(?P<db>\w+)/extractedsourcespx/(?P<image_id>\d+)/$',
        extracted_sources_pixel,
        name='extracted_sources_pixel'),

    url(r'^(?P<db>\w+)/extractedsourceplot/(?P<pk>\d+)/$',
        cache_page(cache_time)(images.ExtractedSourcePlot.as_view()),
        name='extractedsource_plot'),
    url(r'^(?P<db>\w+)/imageplot/(?P<pk>\d+)/$',
        cache_page(cache_time)(images.ImagePlot.as_view()),
        name='image_plot'),
)
