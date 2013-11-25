"""
All views that generate lists of model objects
"""
from django.db.models import Count
from django.views.generic import ListView, TemplateView
import banana.db
from banana.db import db_schema_version, check_database
from banana.models import Dataset, Image, Transient, Extractedsource, \
    Runningcatalog, Monitoringlist, schema_version
from banana.views.mixins import MultiDbMixin, HybridTemplateMixin, \
    SortListMixin, DatasetMixin
from banana.vcs import repo_info
from bananaproject.settings.database import update_config
from django.utils.datastructures import MultiValueDictKeyError


class DatabaseList(TemplateView):
    template_name = "banana/database_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DatabaseList, self).get_context_data(*args, **kwargs)
        update_config()
        context.update(repo_info())
        database_list = banana.db.list()
        for database in database_list:
            database['version'] = db_schema_version(database['name'])
        context['database_list'] = database_list
        context['schema_version'] = schema_version
        return context


class DatasetList(SortListMixin, MultiDbMixin, HybridTemplateMixin, ListView):
    model = Dataset
    paginate_by = 100

    def get_queryset(self):
        qs = super(DatasetList, self).get_queryset()
        return qs.annotate(num_images=Count('images'))
                # TODO: multiple annotations don't work
                #  num_transients=Count('runningcatalogs__transients')


class ImageList(SortListMixin, MultiDbMixin, HybridTemplateMixin,
                DatasetMixin, ListView):
    model = Image
    paginate_by = 100

    def get_queryset(self):
        qs = super(ImageList, self).get_queryset()
        dataset_id = self.get_dataset_id()
        if dataset_id:
            qs = qs.filter(dataset=dataset_id)
        related = ['skyrgn', 'dataset', 'band', 'rejections',
                   'rejections__rejectreason']
        return qs.prefetch_related(*related).annotate(
                            num_extractedsources=Count('extractedsources'))


class TransientList(SortListMixin, MultiDbMixin, HybridTemplateMixin,
                    DatasetMixin, ListView):
    model = Transient
    paginate_by = 100

    def get_queryset(self):
        qs = super(TransientList, self).get_queryset()
        dataset_id = self.get_dataset_id()
        if dataset_id:
            qs = qs.filter(runcat__dataset=dataset_id)
        related = ['band', 'runcat']
        return qs.prefetch_related(*related)


class ExtractedsourcesList(SortListMixin, MultiDbMixin, HybridTemplateMixin,
                           DatasetMixin, ListView):
    model = Extractedsource
    paginate_by = 100

    def get_queryset(self):
        qs = super(ExtractedsourcesList, self).get_queryset()
        dataset_id = self.get_dataset_id()
        if dataset_id:
            qs = qs.filter(image__dataset=dataset_id)
        return qs


class RunningcatalogList(SortListMixin, MultiDbMixin, HybridTemplateMixin,
                         DatasetMixin, ListView):
    model = Runningcatalog
    paginate_by = 100

    def get_queryset(self):
        dataset_id = self.get_dataset_id()
        area = self.get_area()
        self.db_name = self.kwargs.get('db', 'default')
        check_database(self.db_name)
        if area:
            ra, decl, distance = area
            queryset = self.model._default_manager.near_position(ra, decl,
                                                                 distance)
        else:
            queryset = self.model._default_manager.all()
        queryset = queryset.using(self.db_name)
        if dataset_id:
            queryset = queryset.filter(dataset=dataset_id)
        return queryset

    def get_area(self):
        try:
            return [float(self.request.GET[x]) for x in ('ra', 'decl',
                                                       'distance')]
        except MultiValueDictKeyError:
            return False



class MonitoringlistList(SortListMixin, MultiDbMixin, HybridTemplateMixin,
                         DatasetMixin, ListView):
    model = Monitoringlist
    paginate_by = 100

    def get_queryset(self):
        qs = super(MonitoringlistList, self).get_queryset()
        dataset_id = self.get_dataset_id()
        if dataset_id:
            qs = qs.filter(dataset=dataset_id)
        related = ['runcat', 'dataset']
        qs = qs.prefetch_related(*related)
        return qs
