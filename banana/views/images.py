import json
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.cache import cache
from banana.db import check_database
import banana.image
from banana.models import Extractedsource, Transient, Dataset, Assocxtrsource, Image
from banana.mongo import get_hdu


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


def lightcurve_plot(request, db_name, runningcatalog_id):
    check_database(db_name)
    assocs = Assocxtrsource.objects.using(db_name).filter(runcat=runningcatalog_id)
    related = ['xtrsrc', 'xtrsrc__image', 'xtrsrc__image__band']
    lightcurve = Assocxtrsource.objects.using(db_name).filter(
        runcat__in=assocs).prefetch_related(*related)
    response = HttpResponse(mimetype="image/png")
    canvas = banana.image.transient_plot(lightcurve)
    canvas.print_figure(response, format='png')
    return response


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
    canvas.print_figure(response, format='png', bbox_inches='tight',
                        pad_inches=0, dpi=100)
    return response


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


def extractedsource_plot(request, db_name, extractedsource_id):
    check_database(db_name)
    try:
        extractedsource = Extractedsource.objects.using(db_name).get(id=extractedsource_id)
    except Image.DoesNotExist:
        raise Http404
    try:
        size = int(request.GET.get('size', 1))
    except ValueError:

        raise Http404
    hdu = get_hdu(extractedsource.image.url)
    canvas = banana.image.extractedsource(hdu, extractedsource, size)
    response = HttpResponse(mimetype="image/png")
    canvas.print_figure(response, format='png', bbox_inches='tight',
                        pad_inches=0, dpi=100)
    return response
