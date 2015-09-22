"""
All views that generate lists of model objects
"""
from django.db.models import Count, Case, When
from django.views.generic import ListView, TemplateView
from django_filters.views import FilterView
from banana.filters import RunningcatalogFilter
from banana.db import db_schema_version
from banana.db import list as db_list
from banana.models import (Dataset, Image, Newsource, Extractedsource,
                           AugmentedRunningcatalog, Runningcatalog,
                           schema_version, Monitor, Skyregion)
from banana.views.mixins import (HybridTemplateMixin,
                                 SortListMixin, DatasetMixin, FluxViewMixin)
from banana.vcs import repo_info


class DatabaseList(TemplateView):
    template_name = "banana/database_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DatabaseList, self).get_context_data(*args, **kwargs)
        context.update(repo_info())
        database_list = db_list()
        for database in database_list:
            database['version'] = db_schema_version(database['name'])
        context['database_list'] = database_list
        context['schema_version'] = schema_version
        return context


class DatasetList(SortListMixin, HybridTemplateMixin, ListView):
    model = Dataset
    paginate_by = 100

    def get_queryset(self):
        qs = super(DatasetList, self).get_queryset()
        return qs.annotate(num_images=Count('images'))


class ImageList(SortListMixin, HybridTemplateMixin,
                DatasetMixin, ListView):
    model = Image
    paginate_by = 100

    def get_queryset(self):
        qs = super(ImageList, self).get_queryset()
        related = ['skyrgn', 'dataset', 'band', 'rejections',
                   'rejections__rejectreason']
        return qs.prefetch_related(*related).\
            annotate(num_extractedsources=Count('extractedsources')).\
            annotate(num_blind_extractedsources=Count(
                    Case(
                        When(extractedsources__extract_type=0,then=1)
                        )
                    )).\
            annotate(num_forced_extractedsources=Count(
                    Case(
                        When(extractedsources__extract_type=1,then=1)
                        )
                    ))


class NewsourceList(SortListMixin, HybridTemplateMixin,
                    DatasetMixin, ListView):
    model = Newsource
    paginate_by = 100
    dataset_field = 'runcat__dataset'


class MonitorList(SortListMixin, HybridTemplateMixin, DatasetMixin, ListView):
    model = Monitor
    paginate_by = 100


class SkyregionList(SortListMixin, HybridTemplateMixin, DatasetMixin, ListView):
    model = Skyregion
    paginate_by = 100


class ExtractedsourcesList(FluxViewMixin, SortListMixin, HybridTemplateMixin,
                           DatasetMixin, ListView):
    model = Extractedsource
    paginate_by = 100
    dataset_field = 'image__dataset'

    def get_queryset(self):
        qs = super(ExtractedsourcesList, self).get_queryset()
        related = ['runningcatalog_set']
        qs = qs.prefetch_related(*related)
        return qs


class RunningcatalogList(FluxViewMixin, SortListMixin, HybridTemplateMixin,
                         DatasetMixin, FilterView):

    model = Runningcatalog
    template_name = "banana/runningcatalog_filter.html"
    filterset_class = RunningcatalogFilter
    paginate_by = 100

    def get_queryset(self):
        qs = super(RunningcatalogList, self).get_queryset()
        qs = qs.prefetch_related('newsource')
        return qs


class AugmentedRunningcatalogList(FluxViewMixin, SortListMixin,
                                  HybridTemplateMixin, DatasetMixin, FilterView):

    model = AugmentedRunningcatalog
    template_name = "banana/augmentedrunningcatalog_filter.html"
    filterset_class = RunningcatalogFilter
    paginate_by = 100

    def get_queryset(self):
        qs = super(AugmentedRunningcatalogList, self).get_queryset()
        qs = qs.prefetch_related('newsource')
        return qs
