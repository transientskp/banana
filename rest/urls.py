from django.conf.urls import patterns, url, include
from rest.routers import BananaRouter
from rest.views import RunningcatalogViewSet, ExtractedsourceViewSet,\
    DatasetViewSet, ImageViewSet, AssocxtrsourceViewset, TransientViewset


router = BananaRouter()
router.register(r'runningcatalogs', RunningcatalogViewSet)
router.register(r'extractedsources', ExtractedsourceViewSet)
router.register(r'datasets', DatasetViewSet)
router.register(r'images', ImageViewSet)
router.register(r'assocxtrsources', AssocxtrsourceViewset)
router.register(r'transients', TransientViewset)

urlpatterns = patterns('',
                       url(r'', include(router.urls)),
)
