import os.path
from django.shortcuts import render
from django.http import Http404
from django.db.models import Count
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
import pyfits
from tkpdb.models import Dataset, Image, Transient, Assocxtrsource
from tkpdb.util import monetdb_list
import tkpdb.mongo
import tkpdb.image



def databases(request):
    databases = monetdb_list(settings.MONETDB_HOST, settings.MONETDB_PORT, settings.MONETDB_PASSPHRASE)
    context = {'databases': databases}
    return render(request, 'databases.html', context)


def datasets(request, db_name):
    fields = ['id', 'description', 'rerun', 'process_ts', 'num_transients', 'num_images']
    datasets = Dataset.objects.using(db_name).all().annotate(
        #num_transients=Count('runningcatalogs__transients'), # disabled since very slow...
        num_images=Count('images'))

    try:
        datasets.count()
    except StandardError as e:
        messages.add_message(request, messages.ERROR, str(e))
        datasets = []

    
    context = {
        'datasets': datasets,
        'db_name': db_name,
    }
    return render(request, 'datasets.html', context)


def dataset(request, db_name, dataset_id):
    try:
        dataset = Dataset.objects.using(db_name).annotate(num_runningcatalogs=Count('runningcatalogs'),
                                                          num_extractedsources=Count('images__extractedsources')
                                                          ).get(pk=dataset_id)
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
    related = ['skyrgn', 'dataset', 'band', 'rejections', 'rejections__rejectreason']
    images = Image.objects.select_related().prefetch_related(*related).using(db_name).annotate(
        num_extractedsources=Count('extractedsources'))

    dataset_id = request.GET.get("dataset", None)
    if dataset_id:
        images = images.filter(dataset=dataset_id)

    context = {
        'images': images,
        'db_name': db_name,
        'dataset': dataset_id,
    }
    return render(request, 'images.html', context)


def image(request, db_name, image_id):
    related = ['skyrgn', 'dataset', 'band', 'rejections']
    try:
        image = Image.objects.prefetch_related(*related).using(
            db_name).annotate(num_extractedsources=Count('extractedsources')).get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404

    # This extract pixel coordinates of sources
    """
    hdu = get_hdu(image.url)
    aplpy_fits = aplpy.FITSFigure(hdu)
    source_px = []
    for source in image.extractedsources.all():
        decl = source.decl
        ra = source.ra
        source_px = aplpy.wcs_util.world2pix(aplpy_fits._wcs,
                                             numpy.array(ra),
                                             numpy.array(decl))
    """
    context = {
        'image': image,
        'db_name': db_name,
        #'source_px': source_px,
    }
    return render(request, 'image.html', context)


def transient(request, db_name, transient_id):
    try:
        transient = Transient.objects.using(db_name).get(pk=transient_id)
    except Dataset.DoesNotExist:
        raise Http404

    assocs = Assocxtrsource.objects.using(db_name).filter(xtrsrc=transient.trigger_xtrsrc)
    related = ['xtrsrc', 'xtrsrc__image', 'xtrsrc__image__band']
    lightcurve = Assocxtrsource.objects.using(db_name).filter(runcat__in=assocs).prefetch_related(*related)

    context = {
        'db_name': db_name,
        'transient': transient,
        'lightcurve': lightcurve,
    }
    return render(request, 'transient.html', context)


def transients(request, db_name):
    dataset_id = request.GET.get("dataset", None)
    related = ['band', 'runcat']
    transients = Transient.objects.using(db_name).prefetch_related(*related)

    if dataset_id:
        transients = transients.filter(runcat__dataset=dataset_id)

    context = {
        'transients': transients,
        'db_name': db_name,
        'dataset': dataset_id,
    }
    return render(request, 'transients.html', context)


def nsources_plot(request, db_name, image_id):
    try:
        image = Image.objects.using(db_name).get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404

    sources = image.extractedsources.all()
    size = request.GET.get('size', 5)
    hdu = get_hdu(image.url)
    canvas = tkpdb.image.nsources_plot(hdu, size, sources)
    response = HttpResponse(mimetype="image/png")
    canvas.print_figure(response, format='png')
    return response


def transient_plot(request, db_name, transient_id):
    try:
        transient = Transient.objects.using(db_name).get(pk=transient_id)
    except Dataset.DoesNotExist:
        raise Http404

    assocs = Assocxtrsource.objects.using(db_name).filter(xtrsrc=transient.trigger_xtrsrc)
    related = ['xtrsrc', 'xtrsrc__image', 'xtrsrc__image__band']
    lightcurve = Assocxtrsource.objects.using(db_name).filter(runcat__in=assocs).prefetch_related(*related)

    response = HttpResponse(mimetype="image/png")
    canvas = tkpdb.image.plot(lightcurve)
    canvas.print_figure(response, format='png')
    return response



def get_hdu(url):
    if settings.MONGODB["enabled"]:
        mongo_file = tkpdb.mongo.fetch(url)
        return pyfits.open(mongo_file, mode="readonly")
    elif os.path.exists(url):
        return pyfits.open(url, readonly=True)
    else:
        raise Exception("Can't find file")