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

transient_query = """
SELECT
    r2.id as runcat_id,
    a2.id as assoc_id,
    i2.taustart_ts as timestamp,
    i2.freq_eff as frequency,
    a2.v_int,
    a2.eta_int
FROM
    (runningcatalog r2
    JOIN assocxtrsource a2 ON a2.runcat = r2.id
    JOIN extractedsource e2 ON a2.xtrsrc = e2.id
    JOIN image i2 ON e2.image = i2.id)
    -- we need to join the query with the tables again to get the actual
    -- relevant rows. You can't do that in one go, you first need to select
    -- the runningcatalog ID's and the maximum timestmap per frequency.
    JOIN (
        -- select the latest timestamp per runningcatalog
        SELECT
            r.id as runcat_id,
            i.freq_eff as frequency,
            max(i.taustart_ts) as MaxTimestamp

        FROM
            runningcatalog r
            JOIN assocxtrsource a ON a.runcat = r.id
            JOIN extractedsource e ON a.xtrsrc = e.id
            JOIN image i ON e.image = i.id
        GROUP BY
            runcat_id, frequency
        ) last_timestamps
    ON  r2.id = last_timestamps.runcat_id
    AND i2.freq_eff = last_timestamps.frequency
    AND i2.taustart_ts = last_timestamps.MaxTimestamp
"""


class TransientViewset(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Assocxtrsources to be viewed.
    """
    from django.db.models import Max
    timestamps = Assocxtrsource.objects.using('postgres_gijs')\
        .values('runcat', 'xtrsrc__image__freq_eff')\
        .annotate(max_timestamp=(Max('xtrsrc__image__taustart_ts')))

    queryset = Runningcatalog.objects.raw(transient_query)
    serializer_class = AssocxtrsourceSerializer