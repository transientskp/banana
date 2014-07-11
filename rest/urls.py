from django.conf.urls import patterns, url, include
from rest.routers import BananaRouter
from rest.views import RunningcatalogViewSet, ExtractedsourceViewSet,\
    DatasetViewSet, ImageViewSet, AssocxtrsourceViewset


router = BananaRouter()
router.register(r'runningcatalogs', RunningcatalogViewSet)
router.register(r'extractedsources', ExtractedsourceViewSet)
router.register(r'datasets', DatasetViewSet)
router.register(r'images', ImageViewSet)
router.register(r'assocxtrsources', AssocxtrsourceViewset)

urlpatterns = patterns('',
                       url(r'', include(router.urls)),
)
