from banana.models import Runningcatalog, Extractedsource, Dataset, Image
from rest_framework import viewsets
import django_filters
from rest.serializers import RunningcatalogSerializer,\
    ExtractedsourceSerializer, DatasetSerializer, ImageSerializer


class RunningcatalogFilter(django_filters.FilterSet):
    dataset = django_filters.NumberFilter(name='dataset')
    class Meta:
        model = Runningcatalog
        fields = ['dataset', 'id']


class RunningcatalogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Runningcatalogs to be viewed.
    """
    queryset = Runningcatalog.objects.all()
    serializer_class = RunningcatalogSerializer
    #filter_class = RunningcatalogFilter
    filter_fields = ['dataset']



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