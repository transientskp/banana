from django.shortcuts import render
from django.http import Http404
from django.db.models import Count
from tkpdb.models import Dataset, Image
from tkpdb.util import monetdb_list
from banana.settings import MONETDB_HOST, MONETDB_PORT, MONETDB_PASSPHRASE


def databases(request):
    databases = monetdb_list(MONETDB_HOST, MONETDB_PORT, MONETDB_PASSPHRASE)
    context = {'databases': databases}
    return render(request, 'databases.html', context)


def datasets(request, db_name):
    datasets = Dataset.objects.using(db_name).all().annotate(
        num_transients=Count('runningcatalogs__transients'),
        num_images=Count('images'))

    context = {
        'datasets': datasets,
        'db_name': db_name,
    }
    return render(request, 'datasets.html', context)


def dataset(request, db_name, dataset_id):
    try:
        dataset = Dataset.objects.using(db_name).get(pk=dataset_id)
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
    """
    from django.http import HttpResponse
    from PIL import Image

    import random
    INK = "red", "blue", "green", "yellow"
    # ... create/load image here ...
    image = Image.new("RGB", (800, 600), random.choice(INK))

    # serialize to HTTP response
    response = HttpResponse(mimetype="image/png")
    image.save(response, "PNG")
    return response
    """


    related = ['skyrgn', 'dataset', 'band', 'rejections']
    try:
        image = Image.objects.prefetch_related(*related).using(db_name).annotate(num_extractedsources=Count('extractedsources')).get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404
    return render(request, 'image.html', {'image': image})
