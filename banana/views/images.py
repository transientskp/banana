"""
All views that generate images
"""
from django.http import HttpResponse
import banana.image
from banana.models import Extractedsource, Transient, Image, Runningcatalog, Dataset
from banana.mongo import get_hdu
from banana.views.mixins import MultiDbMixin
from django.views.generic import DetailView


class ScatterPlot(MultiDbMixin, DetailView):
    model = Dataset

    def get_context_data(self, **kwargs):
        context = super(ScatterPlot, self).get_context_data(**kwargs)
        context['sources'] = self.object.scatterplot()
        return context

    def render_to_response(self, context, **kwargs):
        response = HttpResponse(mimetype="image/png")
        canvas = banana.image.scatter_plot(context['sources'])
        canvas.print_figure(response, format='png')
        return response


class ImagePlot(MultiDbMixin, DetailView):
    model = Image

    def get_context_data(self, **kwargs):
        context = super(ImagePlot, self).get_context_data(**kwargs)
        context['sources'] = self.object.extractedsources.all()
        context['size'] = int(self.request.GET.get('size', 5))
        context['hdu'] = get_hdu(self.object.url)
        return context

    def render_to_response(self, context, **kwargs):
        response = HttpResponse(mimetype="image/png")
        if context['hdu']:
            canvas = banana.image.image_plot(context['hdu'], context['size'],
                                             context['sources'])
            canvas.print_figure(response, format='png', bbox_inches='tight',
                                pad_inches=0, dpi=100)
        return response


class ExtractedSourcePlot(MultiDbMixin, DetailView):
    model = Extractedsource

    def get_context_data(self, **kwargs):
        context = super(ExtractedSourcePlot, self).get_context_data(**kwargs)
        context['size'] = int(self.request.GET.get('size', 1))
        context['hdu'] = get_hdu(self.object.image.url)
        return context

    def render_to_response(self, context, **kwargs):
        response = HttpResponse(mimetype="image/png")
        if context['hdu']:
            canvas = banana.image.extractedsource(context['hdu'], self.object,
                                                  context['size'])
            canvas.print_figure(response, format='png', bbox_inches='tight',
                                pad_inches=0, dpi=100)
        return response
