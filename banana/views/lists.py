"""
All views that generate lists of model objects
"""
from django.db.models import Count
from django.views.generic import ListView, TemplateView
import banana.db
from banana.db import db_schema_version, check_database
from banana.models import Dataset, Image, Transient, Extractedsource, \
                          Runningcatalog, schema_version, Assocxtrsource
from banana.views.mixins import HybridTemplateMixin, \
                                SortListMixin, DatasetMixin
from banana.vcs import repo_info
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Max, Avg

class DatabaseList(TemplateView):
    template_name = "banana/database_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(DatabaseList, self).get_context_data(*args, **kwargs)
        context.update(repo_info())
        database_list = banana.db.list()
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
                # TODO: multiple annotations don't work
                #  num_transients=Count('runningcatalogs__transients')


class ImageList(SortListMixin, HybridTemplateMixin,
                DatasetMixin, ListView):
    model = Image
    paginate_by = 100

    def get_queryset(self):
        qs = super(ImageList, self).get_queryset()
        related = ['skyrgn', 'dataset', 'band', 'rejections',
                   'rejections__rejectreason']
        return qs.prefetch_related(*related).\
            annotate(num_extractedsources=Count('extractedsources'))


class TransientList(SortListMixin, HybridTemplateMixin,
                    DatasetMixin, ListView):
    model = Transient
    paginate_by = 100
    dataset_field = 'runcat__dataset'

    def get_queryset(self):
        qs = super(TransientList, self).get_queryset()

        related = ['band', 'runcat']
        return qs.prefetch_related(*related)\
            .annotate(lightcurve_max=Max('runcat__extractedsources__f_int',
                                         distinct=True))\
            .annotate(lightcurve_mean=Avg('runcat__extractedsources__f_int',
                                          distinct=True))

class ExtractedsourcesList(SortListMixin, HybridTemplateMixin,
                           DatasetMixin, ListView):
    model = Extractedsource
    paginate_by = 100
    dataset_field = 'image__dataset'


class RunningcatalogList(SortListMixin, HybridTemplateMixin,
                         DatasetMixin, ListView):
    model = Runningcatalog
    paginate_by = 100

    def get_queryset(self):
        self.area = self.get_area()
        manager = self.model._default_manager

        if self.area:
            ra, decl, distance = self.area
            qs = manager.near_position(ra, decl, distance)
        else:
            qs = manager.all()
        qs = qs.order_by(self.get_order())\
            .annotate(lightcurve_max=Max('extractedsources__f_int',
                                         distinct=True))\
            .annotate(lightcurve_mean=Avg('extractedsources__f_int',
                                          distinct=True))
        qs = self.filter_queryset(qs)
        return qs

    def get_area(self):
        try:
            return [float(self.request.GET[x]) for x in ('ra', 'decl',
                                                         'distance')]
        except (MultiValueDictKeyError, ValueError):
            return False

    def get_context_data(self, *args, **kwargs):
        context = super(RunningcatalogList, self).get_context_data(*args,
                                                                   **kwargs)
        context['area'] = self.area
        return context


class MonposList(RunningcatalogList):
    """
    Monitored Position list. This is just a list of runningcatalogs that
    have extracted sources with extract type 2
    """
    def get_queryset(self):
        qs = super(MonposList, self).get_queryset()
        qs = qs.filter(assocxtrsources__xtrsrc__extract_type=2).distinct()
        return qs


class AssocxtrsourceList(SortListMixin, HybridTemplateMixin,
                         DatasetMixin, ListView):
    model = Assocxtrsource
    paginate_by = 100
    dataset_field = 'xtrsrc__image__dataset'

    def get_queryset(self):
        self.v, self.eta = self.get_filters()
        qs = self.model._default_manager.transients(self.v,  self.eta,
                                                    self.get_dataset_id())
        qs = qs.using(self.request.SELECTED_DATABASE).\
            order_by(self.get_order())
        qs = self.filter_queryset(qs)
        return qs

    def get_filters(self):
        try:
            v = float(self.request.GET.get('v'))
        except TypeError, ValueError:
            v = None
        try:
            eta = float(self.request.GET.get('eta'))
        except TypeError, ValueError:
            eta = None
        return v, eta

    def get_context_data(self, *args, **kwargs):
        context = super(AssocxtrsourceList, self).get_context_data(*args,
                                                                   **kwargs)
        context['v'] = self.v
        context['eta'] = self.eta
        return context
