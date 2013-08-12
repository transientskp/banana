"""
All views that generate tables of model objects
"""
import csv
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import render
from banana.db import check_database
import banana.db
from banana.models import Dataset, Image, Transient, Extractedsource,\
    Runningcatalog, Monitoringlist
from banana.tools import recur_getattr


def databases(request):
    database_list = banana.db.list()
    context = {'databases': database_list}
    return render(request, 'databases.html', context)


def datasets(request, db_name):
    check_database(db_name)
    order = request.GET.get('order', 'id')
    datasets_list = Dataset.objects.using(db_name).all().annotate(
        #num_transients=Count('runningcatalogs__transients'),  # wrong
        #num_transients=Count('runningcatalogs'),  # wrong
        num_images=Count('images')).order_by(order)

    page = request.GET.get('page', 1)
    paginator = Paginator(datasets_list, 100)
    datasets = paginator.page(page)
    context = {
        'datasets': datasets,
        'db_name': db_name,
        'order': order,
    }
    return render(request, 'datasets.html', context)


images_fields = [
    'id',
    'skyrgn__centre_ra',
    'skyrgn__centre_decl',
    'taustart_ts',
    'tau_time',
    'freq_eff',
    'freq_bw',
    'num_extractedsources',
    'rejections',
    'url',
]


def images(request, db_name):
    check_database(db_name)
    dataset_id = request.GET.get("dataset", None)
    format = request.GET.get("format", 'html')
    order = request.GET.get('order', 'id')
    order_ = order[1:] if order.startswith('-') else order
    if order_ not in images_fields:
        raise Http404
    related = ['skyrgn', 'dataset', 'band', 'rejections',
               'rejections__rejectreason']
    image_list = Image.objects.select_related(
    ).prefetch_related(*related).using(db_name).annotate(
        num_extractedsources=Count('extractedsources'))
    if dataset_id:
        image_list = image_list.filter(dataset=dataset_id)
    image_list = image_list.order_by(order)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s_%s_images.csv"' % (db_name, dataset_id)
        writer = csv.writer(response)
        writer.writerow(images_fields)
        for image in image_list:
            writer.writerow([recur_getattr(image, field) for field in images_fields])
        return response
    else:
        page = request.GET.get('page', 1)
        paginator = Paginator(image_list, 100)
        images = paginator.page(page)
        context = {
            'images': images,
            'db_name': db_name,
            'dataset': dataset_id,
            'order': order,
        }
        return render(request, 'images.html', context)


transients_fields = [
    'id',
    'runcat__wm_ra',
    'runcat__wm_decl',
    't_start',
    'siglevel',
    'band',
    'eta_int',
    'v_int',
    'runcat__datapoints',
    'runcat'
]

def transients(request, db_name):
    check_database(db_name)
    dataset_id = request.GET.get("dataset", None)
    format = request.GET.get("format", 'html')
    order = request.GET.get('order', 'id')
    order_ = order[1:] if order.startswith('-') else order
    if order_ not in transients_fields:
        raise Http404
    related = ['band', 'runcat']
    transient_list = Transient.objects.using(db_name).prefetch_related(*related)
    if dataset_id:
        transient_list = transient_list.filter(runcat__dataset=dataset_id)
    transient_list = transient_list.order_by(order)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s_%s_transients.csv"' % (db_name, dataset_id)
        writer = csv.writer(response)
        writer.writerow(transients_fields)
        for transient in transient_list:
            writer.writerow([recur_getattr(transient, field) for field in transients_fields])
        return response
    else:
        page = request.GET.get('page', 1)
        paginator = Paginator(transient_list, 100)
        transients = paginator.page(page)
        context = {
            'transients': transients,
            'fields': transients_fields,
            'db_name': db_name,
            'dataset': dataset_id,
            'order': order,
        }
        return render(request, 'transients.html', context)


extractedsources_fields = [
    'id',
    'ra',
    'ra_err',
    'decl',
    'decl_err',
    'det_sigma',
    'f_peak',
    'f_peak_err',
    'f_int',
    'f_int_err',
    'extract_type',
]

def extractedsources(request, db_name):
    check_database(db_name)
    dataset_id = request.GET.get("dataset", None)
    format = request.GET.get("format", 'html')
    order = request.GET.get('order', 'id')
    order_ = order[1:] if order.startswith('-') else order
    if order_ not in extractedsources_fields:
            raise Http404
    extrsrc_list = Extractedsource.objects.using(db_name)
    if dataset_id:
        extrsrc_list = extrsrc_list.filter(image__dataset=dataset_id)
    extrsrc_list = extrsrc_list.order_by(order)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s_%s_extractedsources.csv"' % (db_name, dataset_id)
        writer = csv.writer(response)
        writer.writerow(extractedsources_fields)
        for extrsrc in extrsrc_list:
            writer.writerow([getattr(extrsrc, field) for field in extractedsources_fields])
        return response
    else:
        page = request.GET.get('page', 1)
        paginator = Paginator(extrsrc_list, 100)
        extrsrcs = paginator.page(page)

        context = {
            'page': page,
            'fields': extractedsources_fields,
            'extractedsources': extrsrcs,
            'db_name': db_name,
            'dataset': dataset_id,
            'order': order,
        }
        return render(request, 'extractedsources.html', context)


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