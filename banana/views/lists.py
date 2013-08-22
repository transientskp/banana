"""
All views that generate lists of model objects
"""
from django.db.models import Count
from django.views.generic import ListView, TemplateView
import banana.db
from banana.models import Dataset, Image, Transient, Extractedsource, \
    Runningcatalog, Monitoringlist, Version
from banana.views.mixins import MultiDbMixin, HybridTemplateMixin, \
    SortListMixin, DatasetMixin
from banana.vcs import repo_info


def schema_version(database_name):
    """
    Gets schema version from database. Will return error if it can't connect.

    For now we use that in the template to check if we can actually connect to
    the database. Also banana.db would be a better place for this function,
    but that is used during Django init. No DB queries can be performed during
    that phase.
    """
    try:
        return Version.objects.using(database_name).get().value
    except Exception as e:
        return "error"


class DatabaseList(TemplateView):
    template_name = "banana/database_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DatabaseList, self).get_context_data(*args, **kwargs)
        context.update(repo_info())
        database_list = banana.db.list()
        for database in database_list:
            database['version'] = schema_version(database['name'])
        context['database_list'] = database_list
        return context


class DatasetList(SortListMixin, MultiDbMixin, HybridTemplateMixin, ListView):
    model = Dataset
    paginate_by = 100

    def get_queryset(self):
        qs = super(DatasetList, self).get_queryset()
        return qs.annotate(num_images=Count('images', distinct=True),
                           num_transients=Count('runningcatalogs__transients',
                                                distinct=True)
                           )

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
        qs = super(RunningcatalogList, self).get_queryset()
        dataset_id = self.get_dataset_id()
        if dataset_id:
            qs = qs.filter(dataset=dataset_id)
        return qs


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
