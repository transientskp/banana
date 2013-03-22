from django.shortcuts import render
from django.http import Http404
from tkpdb.models import Dataset, Image
from tkpdb.util import monetdb_list
from banana.settings import MONETDB_HOST, MONETDB_PORT, MONETDB_PASSPHRASE


def databases(request):
    databases = monetdb_list(MONETDB_HOST, MONETDB_PORT, MONETDB_PASSPHRASE)
    context = {'databases': databases}
    return render(request, 'databases.html', context)


def datasets(request, db_name):
    datasets = Dataset.objects.using(db_name).all()

    for dataset in datasets:
        dataset.image_count = dataset.images.count()

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
    context = {
        'dataset': dataset,
        'image_num': dataset.images.count(),
        'runningcatalog_num': dataset.runningcatalogs.count()
    }
    return render(request, 'dataset.html', context)


def image(request, db_name, dataset_id):
    try:
        image = Image.objects.using(db_name).get(pk=dataset_id)
    except Image.DoesNotExist:
        raise Http404
    return render(request, 'image.html', {'image': image})