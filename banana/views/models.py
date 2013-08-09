"""
All views that visualise a model object (banana.models)
"""
import csv
import json
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.shortcuts import render
from banana.db import check_database
import banana.image
from banana.models import Image, Monitoringlist, Dataset, Extractedsource,\
    Runningcatalog, Assocxtrsource, Transient
from banana.views.etc import MultiDbMixin, HybridDetailView
#from django.views.generic import DetailView


def image_detail(request, db_name, image_id):
    check_database(db_name)
    try:
        image = Image.objects.using(db_name).get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404

    size = int(request.GET.get("size", 8))  # in inches

    sources = banana.image.extracted_sources_pixels(image, size)
    dpi = 100
    image_size = size * dpi

    context = {
        'image': image,
        'db_name': db_name,
        'sources': sources,
        'size': size,
    }
    return render(request, 'imagedetail.html', context)


def image(request, db_name, image_id):
    check_database(db_name)
    related = ['skyrgn', 'dataset', 'band', 'rejections']
    try:
        image = Image.objects.prefetch_related(*related).using(
            db_name).annotate(num_extractedsources=Count('extractedsources')
        ).get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404

    image_size = 4  # inches, don't ask why

    sources = banana.image.extracted_sources_pixels(image, image_size)

    context = {
        'image': image,
        'db_name': db_name,
        'sources': sources,
        'image_size': image_size,
    }
    return render(request, 'image.html', context)


def extracted_sources_pixel(request, db_name, image_id):
    try:
        image = Image.objects.using(db_name).get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404
    sources = banana.image.extracted_sources_pixels(image)
    return HttpResponse(json.dump(sources), "application/json")


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


def runningcatalog(request, db_name, runningcatalog_id):
    check_database(db_name)
    try:
        runningcatalog = Runningcatalog.objects.using(db_name).get(
            pk=runningcatalog_id)
    except Dataset.DoesNotExist:
        raise Http404
    format = request.GET.get("format", 'html')
    assocs = Assocxtrsource.objects.using(db_name).filter(runcat=runningcatalog_id)
    #extractedsources = [x.xtrsrc for x in assocs]
    related = ['image', 'image__band']
    extractedsources = Extractedsource.objects.using(db_name).filter(asocxtrsources__in=assocs).prefetch_related(*related)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s_runningcatalog_%s.csv"' % (db_name, runningcatalog_id)
        writer = csv.writer(response)
        writer.writerow(['id', 'taustart_ts', 'tau_time', 'freq_central', 'f_int', 'fint_err'])

        for extractedsource in extractedsources:
            writer.writerow([extractedsource.id,
                             extractedsource.image.taustart_ts,
                             extractedsource.image.tau_time,
                             extractedsource.image.band.freq_central,
                             extractedsource.f_int,
                             extractedsource.f_int_err])
        return response
    else:
        context = {
            'db_name': db_name,
            'runningcatalog': runningcatalog,
            'extractedsources': extractedsources,
        }
        return render(request, 'runningcatalog.html', context)


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


class TransientDetail(MultiDbMixin, HybridDetailView):

    model = Transient

    def get_context_data(self, **kwargs):
        context = super(TransientDetail, self).get_context_data(**kwargs)
        context['lightcurve'] = self.object.lightcurve()
        return context