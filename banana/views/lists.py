"""
All views that generate lists of model objects
"""
from django.db.models import Count
from django.views.generic import ListView, TemplateView
import banana.db
from banana.models import Dataset, Image, Transient, Extractedsource, \
    Runningcatalog, Monitoringlist
from banana.views.mixins import MultiDbMixin, HybridTemplateMixin, SortListMixin, DatasetMixin


class DatabaseList(TemplateView):
    template_name = "banana/database_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DatabaseList, self).get_context_data(*args, **kwargs)
        context['database_list'] = banana.db.list()
        return context


class DatasetList(SortListMixin, MultiDbMixin, ListView):
    model = Dataset
    paginate_by = 100

    def get_queryset(self):
        qs = super(DatasetList, self).get_queryset()
        return qs.annotate(num_images=Count('images'))
        # TODO: add transients count. We can have multiple count annotations
        #num_transients=Count('runningcatalogs__transients'),  # wrong
        #num_transients=Count('runningcatalogs'),  # wrong


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
                            ListView):
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
