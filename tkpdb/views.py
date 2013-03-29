import os.path
from django.shortcuts import render
from django.http import Http404
from django.db.models import Count
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
import pyfits
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
    related = ['skyrgn', 'dataset', 'band', 'rejections']

    dataset = request.GET.get("dataset", None)
    images = Image.objects.prefetch_related(*related).using(db_name).annotate(
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
    context = {
        'image': image,
        'db_name': db_name,
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

    if settings.MONGODB["enabled"]:
        mongo_file = tkpdb.mongo.fetch(image.url)
        hdu = pyfits.open(mongo_file, mode="readonly")
    elif os.path.exists(image.url):
        hdu = pyfits.open(image.url, readonly=True)
    else:
        raise Exception("Can't find file")

    canvas = tkpdb.image.plot(hdu, size, sources)
    canvas.print_figure(response, format='png')
    return response


