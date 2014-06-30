from django.conf.urls import patterns, url, include
from rest.routers import BananaRouter
from rest.views import RunningcatalogViewSet, ExtractedsourceViewSet,\
    DatasetViewSet, ImageViewSet


router = BananaRouter()
router.register(r'runningcatalogs', RunningcatalogViewSet)
router.register(r'extractedsources', ExtractedsourceViewSet)
router.register(r'datasets', DatasetViewSet)
router.register(r'images', ImageViewSet)

urlpatterns = patterns('',
                       url(r'^rest/', include(router.urls)),
)
