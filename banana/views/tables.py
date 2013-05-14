import csv
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import render
from banana.db import monetdb_list, check_database
from banana.models import Dataset, Image, Transient, Extractedsource


def databases(request):
    databases = monetdb_list(settings.MONETDB_HOST, settings.MONETDB_PORT,
                             settings.MONETDB_PASSPHRASE)

    for dbname, dbparams in settings.DATABASES.items():
        if dbparams['ENGINE'] != 'djonet' and dbname != 'default':
            databases.append({'name': dbname, 'type': 'postgresql'})

    context = {'databases': databases}
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


def dataset(request, db_name, dataset_id):
    check_database(db_name)
    try:
        dataset = Dataset.objects.using(db_name).get(pk=dataset_id)
           # .annotate(
           # num_runningcatalogs=Count('runningcatalogs'),
           # num_extractedsources=Count('images__extractedsources'))
    except Dataset.DoesNotExist:
        raise Http404

    images = Image.objects.using(db_name).filter(dataset=dataset).annotate(
        num_extractedsources=Count('extractedsources'))
    context = {
        'db_name': db_name,
        'dataset': dataset,
        'images': images,
    }
    return render(request, 'dataset.html', context)


def images(request, db_name):
    check_database(db_name)

    related = ['skyrgn', 'dataset', 'band', 'rejections',
               'rejections__rejectreason']
    images_list = Image.objects.select_related(
    ).prefetch_related(*related).using(db_name).annotate(
        num_extractedsources=Count('extractedsources'))

    dataset_id = request.GET.get("dataset", None)
    if dataset_id:
        images_list = images_list.filter(dataset=dataset_id)

    page = request.GET.get('page', 1)
    paginator = Paginator(images_list, 100)
    images = paginator.page(page)
    context = {
        'images': images,
        'db_name': db_name,
        'dataset': dataset_id,
    }
    return render(request, 'images.html', context)


def transients(request, db_name):
    check_database(db_name)
    dataset_id = request.GET.get("dataset", None)
    format = request.GET.get("format", 'html')
    order = request.GET.get('order', 'id')
    if order not in Transient._meta.get_all_field_names():
        raise Http404
    related = ['band', 'runcat']
    transient_list = Transient.objects.using(db_name).prefetch_related(*related)
    if dataset_id:
        transient_list = transient_list.filter(runcat__dataset=dataset_id)

    transient_list = transient_list.order_by(order)

    if format == 'csv':
        fields = ['id', 'runcat.wm_ra', 'runcat.wm_decl', 'startdate',
                  'siglevel', 'band', 'eta_int', 'v_int', 'runcat.datapoints',
                  'runcat']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s_transients.csv"' % db_name

        writer = csv.writer(response)
        writer.writerow(fields)
        for transient in transient_list:
            #writer.writerow([getattr(transient, field) for field in fields])
            writer.writerow([transient.id, transient.runcat.wm_ra,
                             transient.runcat.wm_decl,
                             transient.t_start, transient.siglevel,
                             transient.band,
                             transient.eta_int, transient.v_int,
                             transient.runcat.datapoints, transient.runcat])
        return response
    else:
        page = request.GET.get('page', 1)
        paginator = Paginator(transient_list, 100)
        transients = paginator.page(page)

        context = {
            'transients': transients,
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
        response['Content-Disposition'] = 'attachment; filename="%s_extractedsources.csv"' % db_name
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

"""
other tables:
Assoccatsource
Assocskyrgn
Assocxtrsource
Catalog
Catalogedsource
Classification
Extractedsource
Frequencyband
Monitoringlist
Runningcatalog
RunningcatalogFlux
Temprunningcatalog
"""