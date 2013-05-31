import sys
from django.conf import settings
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render
from banana.db import check_database
from banana.models import Transient, Dataset, Assocxtrsource, Extractedsource,\
    Runningcatalog, Monitoringlist, Image


def transient(request, db_name, transient_id):
    check_database(db_name)
    try:
        transient = Transient.objects.using(db_name).get(pk=transient_id)
    except Dataset.DoesNotExist:
        raise Http404
    assocs = Assocxtrsource.objects.using(db_name).filter(
        xtrsrc=transient.trigger_xtrsrc)
    related = ['xtrsrc', 'xtrsrc__image', 'xtrsrc__image__band']
    lightcurve = Assocxtrsource.objects.using(db_name).filter(
        runcat__in=assocs).prefetch_related(*related)
    context = {
        'db_name': db_name,
        'transient': transient,
        'lightcurve': lightcurve,
    }
    return render(request, 'transient.html', context)


def extractedsource(request, db_name, extractedsource_id):
    check_database(db_name)
    try:
        extractedsource = Extractedsource.objects.using(db_name).get(
            pk=extractedsource_id)
    except Dataset.DoesNotExist:
        raise Http404
    context = {
        'db_name': db_name,
        'extractedsource': extractedsource,
    }
    return render(request, 'extractedsource.html', context)


def runningcatalog(request, db_name, runningcatalog_id):
    check_database(db_name)
    try:
        runningcatalog = Runningcatalog.objects.using(db_name).get(
            pk=runningcatalog_id)
    except Dataset.DoesNotExist:
        raise Http404

    assocs = Assocxtrsource.objects.using(db_name).filter(runcat=runningcatalog_id)
    #extractedsources = [x.xtrsrc for x in assocs]
    related = ['image', 'image__band']
    extractedsources = Extractedsource.objects.using(db_name).filter(asocxtrsources__in=assocs).prefetch_related(*related)
    context = {
        'db_name': db_name,
        'runningcatalog': runningcatalog,
        'extractedsources': extractedsources,
    }
    return render(request, 'runningcatalog.html', context)


def monitoringlist(request, db_name, monitoringlist_id):
    check_database(db_name)
    try:
        monitoringlist = Monitoringlist.objects.using(db_name).get(
            pk=monitoringlist_id)
    except Dataset.DoesNotExist:
        raise Http404
    context = {
        'db_name': db_name,
        'monitoringlist': monitoringlist,
    }
    return render(request, 'monitoringlist.html', context)


def banana_500(request):
    """a 500 error view that shows the exception. Since we have a lot of
     MonetDB problems this may become useful.
    """
    type_, value, tb = sys.exc_info()
    context = {
         'STATIC_URL': settings.STATIC_URL,
         'exception_value': value,
    }
    return render(request, '500.html', context)


def dataset(request, db_name, dataset_id):
    check_database(db_name)
    try:
        dataset = Dataset.objects.using(db_name).get(pk=dataset_id)
    except Dataset.DoesNotExist:
        raise Http404

    images_per_band = {}
    related = ['band']
    images = Image.objects.using(db_name).filter(dataset=dataset).prefetch_related(*related).annotate(
        num_extractedsources=Count('extractedsources')).order_by('taustart_ts')
    num_extractedsources = Extractedsource.objects.using(db_name).filter(image__in=images.all()).count()

    for image in images:
        label = str(image.band)
        if label not in images_per_band:
           images_per_band[label] = []
        images_per_band[label].append(image.num_extractedsources)

    context = {
        'db_name': db_name,
        'dataset': dataset,
        'images': images,
        'num_extractedsources': num_extractedsources,
        'images_per_band': images_per_band,
    }
    return render(request, 'dataset.html', context)