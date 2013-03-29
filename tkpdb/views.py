import os.path
from django.shortcuts import render
from django.http import Http404
from django.db.models import Count
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
import pyfits
import aplpy
import numpy
from tkpdb.models import Dataset, Image
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

    #
    dataset = request.GET.get("dataset", None)
    images = Image.objects.select_related().prefetch_related(*related).using(db_name).annotate(
        num_extractedsources=Count('extractedsources'))

    if dataset:
        images = images.filter(dataset=dataset)

    context = {
        'images': images,
        'db_name': db_name,
        'dataset': dataset,
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


def plot(request, db_name, image_id):
    try:
        image = Image.objects.using(db_name).get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404

    response = HttpResponse(mimetype="image/png")
    sources = image.extractedsources.all()
    size = request.GET.get('size', 5)

    hdu = get_hdu(image.url)

    canvas = tkpdb.image.plot(hdu, size, sources)
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