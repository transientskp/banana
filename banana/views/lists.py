"""
All views that generate tables of model objects
"""
import csv
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from banana.db import check_database
import banana.db
from banana.models import Dataset, Image, Transient, Extractedsource,\
    Runningcatalog, Monitoringlist
from banana.views.etc import MultiDbMixin, HybridTemplateMixin, SortListMixin


def databases(request):
    database_list = banana.db.list()
    context = {'databases': database_list}
    return render(request, 'databases.html', context)


class DatasetList(SortListMixin, MultiDbMixin, ListView):
    model = Dataset
    paginate_by = 100

    def get_queryset(self):
        qs = super(DatasetList, self).get_queryset()
        return qs.annotate(num_images=Count('images'))
        # TODO: add transients count
        #num_transients=Count('runningcatalogs__transients'),  # wrong
        #num_transients=Count('runningcatalogs'),  # wrong


class ImageList(SortListMixin, MultiDbMixin, HybridTemplateMixin, ListView):
    model = Image
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(ImageList, self).get_context_data(**kwargs)
        context['dataset'] = self.request.GET.get("dataset", None)
        return context

    def get_queryset(self):
        qs = super(ImageList, self).get_queryset()
        dataset_id = self.request.GET.get("dataset", None)
        if dataset_id:
            qs = qs.filter(dataset=dataset_id)
        related = ['skyrgn', 'dataset', 'band', 'rejections',
                   'rejections__rejectreason']
        return qs.prefetch_related(*related).annotate(
                            num_extractedsources=Count('extractedsources'))


class TransientList(SortListMixin, MultiDbMixin, HybridTemplateMixin, ListView):
    model = Transient
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(TransientList, self).get_context_data(**kwargs)
        context['dataset'] = self.request.GET.get("dataset", None)
        return context

    def get_queryset(self):
        qs = super(TransientList, self).get_queryset()
        dataset_id = self.request.GET.get("dataset", None)
        if dataset_id:
            qs = qs.filter(runcat__dataset=dataset_id)
        related = ['band', 'runcat']
        return qs.prefetch_related(*related)



class ExtractedsourcesList(SortListMixin, MultiDbMixin, HybridTemplateMixin, ListView):
    model = Extractedsource
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(ExtractedsourcesList, self).get_context_data(**kwargs)
        context['dataset'] = self.request.GET.get("dataset", None)
        return context

    def get_queryset(self):
        qs = super(ExtractedsourcesList, self).get_queryset()
        dataset_id = self.request.GET.get("dataset", None)
        if dataset_id:
            qs = qs.filter(image__dataset=dataset_id)
        return qs


runningcatalogs_fields = [
    'id',
    'wm_ra',
    'wm_ra_err',
    'wm_decl',
    'wm_decl_err',
    'datapoints',
]


def runningcatalogs(request, db_name):
    check_database(db_name)
    dataset_id = request.GET.get("dataset", None)
    format = request.GET.get("format", 'html')
    order = request.GET.get('order', 'id')
    order_ = order[1:] if order.startswith('-') else order
    if order_ not in runningcatalogs_fields:
            raise Http404
    runcat_list = Runningcatalog.objects.using(db_name)
    if dataset_id:
        runcat_list = runcat_list.filter(dataset=dataset_id)
    runcat_list = runcat_list.order_by(order)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s_%s_runningcatalogs.csv"' % (db_name, dataset_id)
        writer = csv.writer(response)
        writer.writerow(runningcatalogs_fields)
        for runningcatalog in runcat_list:
            writer.writerow([getattr(runningcatalog, field)
                             for field in runningcatalogs_fields])
        return response
    else:
        page = request.GET.get('page', 1)
        paginator = Paginator(runcat_list, 100)
        runningcatalogs = paginator.page(page)

        context = {
            'page': page,
            'fields': extractedsources_fields,
            'runningcatalogs': runningcatalogs,
            'db_name': db_name,
            'dataset': dataset_id,
            'order': order,
        }
        return render(request, 'runningcatalogs.html', context)


monitoringlists_fields = [
    'id',
    'runcat',
    'ra',
    'decl',
    'dataset',
    'userentry',
]


def monitoringlists(request, db_name):
    check_database(db_name)
    dataset_id = request.GET.get("dataset", None)
    format = request.GET.get("format", 'html')
    order = request.GET.get('order', 'id')
    order_ = order[1:] if order.startswith('-') else order
    if order_ not in monitoringlists_fields:
            raise Http404

    related = ['runcat', 'dataset']
    monlist_list = Monitoringlist.objects.using(db_name).prefetch_related(*related)
    if dataset_id:
        monlist_list = monlist_list.filter(dataset=dataset_id)
    monlist_list = monlist_list.order_by(order)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s_%s_monitoringlists.csv"' % (db_name, dataset_id)
        writer = csv.writer(response)
        writer.writerow(monitoringlists_fields)
        for monitoringlist in monlist_list:
            writer.writerow([getattr(monitoringlist, field)
                             for field in monitoringlists_fields])
        return response
    else:
        page = request.GET.get('page', 1)
        paginator = Paginator(monlist_list, 100)
        monitoringlists = paginator.page(page)

        context = {
            'page': page,
            'fields': monitoringlists_fields,
            'monitoringlists': monitoringlists,
            'db_name': db_name,
            'dataset': dataset_id,
            'order': order,
        }
        return render(request, 'monitoringlists.html', context)