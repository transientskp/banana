import sys
import json
import numpy
import aplpy
from django.shortcuts import render
from django.http import Http404
from django.db.models import Count
from django.conf import settings
from django.http import HttpResponse
from django.core.paginator import Paginator
from banana.db import check_database, monetdb_list
from banana.models import Dataset, Image, Transient, Assocxtrsource, Extractedsource
import banana.mongo
import banana.image
from banana.mongo import get_hdu


def databases(request):
    databases = monetdb_list(settings.MONETDB_HOST, settings.MONETDB_PORT,
                             settings.MONETDB_PASSPHRASE)
    context = {'databases': databases}
    return render(request, 'databases.html', context)


def datasets(request, db_name):
    check_database(db_name)
    order = request.GET.get('order', 'id')
    datasets_list = Dataset.objects.using(db_name).all().annotate(
        #num_transients=Count('runningcatalogs__transients'), # disabled, slow
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


def transients(request, db_name):
    check_database(db_name)
    dataset_id = request.GET.get("dataset", None)
    related = ['band', 'runcat']
    transient_list = Transient.objects.using(db_name).prefetch_related(*related)
    if dataset_id:
        transient_list = transient_list.filter(runcat__dataset=dataset_id)

    page = request.GET.get('page', 1)
    paginator = Paginator(transient_list, 100)
    transients = paginator.page(page)

    context = {
        'transients': transients,
        'db_name': db_name,
        'dataset': dataset_id,
    }
    return render(request, 'transients.html', context)


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

    sources += [
        ('calibrate1', 0, 0, 10),
        ('calibrate2', image_size, image_size, 10),
        ]

    context = {
        'image': image,
        'db_name': db_name,
        'sources': sources,
        'size': size,
        }
    return render(request, 'imagedetail.html', context)


def image_plot(request, db_name, image_id):
    check_database(db_name)
    try:
        image = Image.objects.using(db_name).get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404
    sources = image.extractedsources.all()
    try:
        size = int(request.GET.get('size', 5))
    except ValueError:
        raise Http404
    hdu = get_hdu(image.url)
    canvas = banana.image.image_plot(hdu, size, sources)
    response = HttpResponse(mimetype="image/png")
    canvas.print_figure(response, format='png', bbox_inches='tight', \
                        pad_inches=0, dpi=100)
    return response


def transient_plot(request, db_name, transient_id):
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
    response = HttpResponse(mimetype="image/png")
    canvas = banana.image.transient_plot(lightcurve)
    canvas.print_figure(response, format='png')
    return response


scatterplot_query = """\
SELECT
  x.id
  ,3600 * (x.ra - r.wm_ra) as ra_dist_arcsec
  ,3600 * (x.decl - r.wm_decl) as decl_dist_arcsec
  ,x.ra_err
  ,x.decl_err
FROM assocxtrsource a
  ,extractedsource x
  ,runningcatalog r
  ,image im1
WHERE a.runcat = r.id
AND a.xtrsrc = x.id
AND x.image = im1.id
AND im1.dataset = %(dataset_id)s
"""


def scatter_plot(request, db_name, dataset_id):
    check_database(db_name)
    sources = Extractedsource.objects.raw(scatterplot_query,
                                    {'dataset_id': dataset_id}).using(db_name)
    response = HttpResponse(mimetype="image/png")
    canvas = banana.image.scatter_plot(sources)
    canvas.print_figure(response, format='png')
    return response


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
