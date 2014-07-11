from banana.models import Runningcatalog, Extractedsource, Dataset, Image, Assocxtrsource
from rest_framework import viewsets
import django_filters
from rest.serializers import RunningcatalogSerializer,\
    ExtractedsourceSerializer, DatasetSerializer, ImageSerializer,\
    AssocxtrsourceSerializer

import rest_framework.filters


class RunningcatalogFilter(django_filters.FilterSet):
    v_int = django_filters.NumberFilter(name="assocxtrsources__v_int",
                                        lookup_type='gte')
    eta_int = django_filters.NumberFilter(name="assocxtrsources__eta_int",
                                          lookup_type='gte')

    class Meta:
        model = Runningcatalog
        fields = ['dataset', 'id', 'assocxtrsources__v_int',
                  'assocxtrsources__eta_int']


class RunningcatalogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Runningcatalogs to be viewed.
    """
    queryset = Runningcatalog.objects.all()
    serializer_class = RunningcatalogSerializer
    filter_class = RunningcatalogFilter
    filter_backends = (rest_framework.filters.DjangoFilterBackend,)


class ExtractedsourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Extractedsources to be viewed.
    """
    queryset = Extractedsource.objects.all()
    serializer_class = ExtractedsourceSerializer


class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Datasets to be viewed.
    """
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class ImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Images to be viewed.
    """
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class AssocxtrsourceViewset(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Assocxtrsources to be viewed.
    """
    queryset = Assocxtrsource.objects.all()
    serializer_class = AssocxtrsourceSerializer