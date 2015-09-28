"""
All views that generate images
"""
from django.http import HttpResponse
import banana.image
from banana.models import Extractedsource, Image
from banana.mongo import get_hdu, fetch
from django.views.generic import DetailView


class ImagePlot(DetailView):
    model = Image

    def get_context_data(self, **kwargs):
        context = super(ImagePlot, self).get_context_data(**kwargs)
        context['sources'] = self.object.extractedsources.all()
        try:
            context['size'] = int(self.request.GET.get('size', 5))
        except ValueError:
             context['size'] = 5
        context['hdu'] = get_hdu(self.object.url)
        return context

    def render_to_response(self, context, **kwargs):
        response = HttpResponse(content_type="image/png")
        if context['hdu']:
            canvas = banana.image.image_plot(context['hdu'], context['size'],
                                             context['sources'])
            canvas.print_figure(response, format='png', bbox_inches='tight',
                                pad_inches=0, dpi=100)
        return response


class ExtractedSourcePlot(DetailView):
    model = Extractedsource

    def get_context_data(self, **kwargs):
        context = super(ExtractedSourcePlot, self).get_context_data(**kwargs)
        context['size'] = int(self.request.GET.get('size', 1))
        context['hdu'] = get_hdu(self.object.image.url)
        return context

    def render_to_response(self, context, **kwargs):
        response = HttpResponse(content_type="image/png")
        if context['hdu']:
            canvas = banana.image.extractedsource(context['hdu'], self.object,
                                                  context['size'])
            canvas.print_figure(response, format='png', bbox_inches='tight',
                                pad_inches=0, dpi=100)
        return response


class RawImage(DetailView):
    model = Image

    def render_to_response(self, context, **kwargs):
        handler = fetch(self.object.url)
        response = HttpResponse(handler, content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename="banana.fits"'
        return response
