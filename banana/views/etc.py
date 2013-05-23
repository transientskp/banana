import sys
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from banana.db import check_database
from banana.models import Transient, Dataset, Assocxtrsource, Extractedsource,\
    Runningcatalog, Monitoringlist

__author__ = 'gijs'


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