import json
import sys
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
import banana.image
from banana.models import Image


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


def extracted_sources_pixel(request, db, image_id):
    try:
        image = Image.objects.using(db).get(pk=image_id)
    except Image.DoesNotExist:
        raise Http404
    sources = banana.image.extracted_sources_pixels(image, 5)
    return HttpResponse(json.dumps(sources), "application/json")


