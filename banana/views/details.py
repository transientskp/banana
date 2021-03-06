"""
All views that visualise a model object (banana.models)
"""
from django.db.models import Count
from django.views.generic import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
import banana.image
from banana.models import (Image, Dataset, Extractedsource,
                           Runningcatalog,  Newsource, Assocxtrsource, Monitor,
                           Skyregion)
from banana.views.mixins import (HybridTemplateMixin,
                                 DatasetMixin, SortListMixin, FluxViewMixin)
from collections import OrderedDict


class ImageDetail(FluxViewMixin, SortListMixin, HybridTemplateMixin, ListView):
    model = Image
    paginate_by = 20
    template_name = "banana/image_detail.html"

    def get_size(self):
        image_size = 4  # in inches
        return image_size

    def get_queryset(self):
        qs = super(ImageDetail, self).get_queryset()
        self.object = get_object_or_404(qs, id=self.kwargs['pk'])
        return self.object.extractedsources.all().order_by(self.get_order())

    def get_context_data(self, **kwargs):
        previous, next = self.object.get_next_previous()
        context = super(ImageDetail, self).get_context_data(**kwargs)
        context['image_size'] = self.get_size()
        context['pixels'] = banana.image.extracted_sources_pixels(self.object,
                                                                  self.get_size())
        context['dataset'] = self.object.dataset
        context['object'] = self.object

        context['previous'] = previous

        context['next'] = next

        return context


class BigImageDetail(DatasetMixin, DetailView):
    template_name = "banana/bigimage_detail.html"
    model = Image
    image_size = 8

    def get_context_data(self, **kwargs):
        context = super(BigImageDetail, self).get_context_data(**kwargs)
        context['image_size'] = self.image_size
        context['sources'] = banana.image.extracted_sources_pixels(self.object,
                                                                   self.image_size)
        context['dataset'] = self.object.dataset
        return context


class ImageJs9Detail(DatasetMixin, DetailView):
    template_name = "banana/image_js9.html"
    model = Image

    def get_context_data(self, **kwargs):
        context = super(ImageJs9Detail, self).get_context_data(**kwargs)
        context['lightcurve'] = self.object.extractedsources.all()
        context['object'] = self.object
        context['dataset'] = self.object.dataset
        return context


class DatasetDetail(DetailView):
    model = Dataset


class HeatmapView(DetailView):
    """
    Only shows the heatmap.

    The heatmap is a 2D histogram of offsets between running catalog and
    extracted source positions.
    """
    model = Dataset

    template_name = 'banana/heatmap.html'


class QualityControlView(DetailView):
    """
    Show all quality control related information for a dataset
    """
    model = Dataset
    template_name = 'banana/dataset_qualitycontrol.html'

    def get_context_data(self, **kwargs):
        context = super(QualityControlView, self).get_context_data(**kwargs)
        context['frequencies'] = set([i.band.freq_central for i in self.object.images.all()])
        return context

    def get_queryset(self):
        qs = super(QualityControlView, self).get_queryset()
        related = ['images', 'images__band']
        return qs.prefetch_related(*related)


class NumSourceView(DetailView):
    model = Dataset
    template_name = 'banana/dataset_sourcenum.html'

    def get_context_data(self, **kwargs):
        context = super(NumSourceView, self).get_context_data(**kwargs)

        # annotated images
        images = Image.objects.using(self.request.SELECTED_DATABASE). \
            filter(dataset=self.object). \
            annotate(num_extractedsources=Count('extractedsources')). \
            values('id', 'band__freq_central', 'num_extractedsources', 'taustart_ts'). \
            order_by('taustart_ts')

        # gather data for lightcurve plot
        images_per_band = {}
        image_list = images.all()
        for image in image_list:
            label = str(image['band__freq_central'])
            images_per_band.setdefault(label, [])
            images_per_band[label].append({'num_extractedsources': image['num_extractedsources'],
                                           'image_id': image['id']})
        images_per_band = OrderedDict(sorted(images_per_band.iteritems(),
                                             key=lambda x: x[0]))

        context['dataset'] = self.object
        context['num_extractedsources'] = sum([i['num_extractedsources'] for i in image_list])
        context['images'] = images
        context['images_per_band'] = images_per_band
        return context



class ExtractedSourceDetail(DetailView):
    model = Extractedsource

    def get_context_data(self, **kwargs):
        context = super(ExtractedSourceDetail, self).get_context_data(**kwargs)
        context['extractedsource'] = self.object
        context['dataset'] = self.object.image.dataset
        return context


class MonitorDetail(DetailView):
    model = Monitor

    def get_context_data(self, **kwargs):
        context = super(MonitorDetail, self).get_context_data(**kwargs)
        context['dataset'] = self.object.dataset
        return context


class SkyregionDetail(SortListMixin, DatasetMixin, HybridTemplateMixin,
                      ListView):
    model = Skyregion
    paginate_by = 20
    template_name = "banana/skyregion_detail.html"

    def get_queryset(self):
        qs = super(SkyregionDetail, self).get_queryset()
        self.object = get_object_or_404(qs, id=self.kwargs['pk'])
        return self.object.images.all(). \
            order_by(self.get_order()). \
            annotate(num_extractedsources=Count('extractedsources'))

    def get_context_data(self, **kwargs):
        context = super(SkyregionDetail, self).get_context_data(**kwargs)
        context['object'] = self.object
        context['dataset'] = self.object.dataset
        return context


class NewsourceDetail(SortListMixin, DatasetMixin,
                      HybridTemplateMixin, ListView):
    model = Newsource
    paginate_by = 100
    default_order = 'image__taustart_ts'
    template_name = "banana/newsource_detail.html"

    def get_queryset(self):
        qs = super(NewsourceDetail, self).get_queryset()
        self.object = get_object_or_404(qs, id=self.kwargs['pk'])
        return self.object.runcat.extractedsources.order_by(self.get_order())

    def get_context_data(self, **kwargs):
        context = super(NewsourceDetail, self).get_context_data(**kwargs)
        context['object'] = self.object
        context['dataset'] = self.object.runcat.dataset
        return context


class RunningcatalogDetail(FluxViewMixin, SortListMixin, DatasetMixin,
                           HybridTemplateMixin, ListView):
    model = Runningcatalog
    paginate_by = 100
    default_order = 'xtrsrc__image__taustart_ts'
    template_name = "banana/runningcatalog_detail.html"

    def get_queryset(self):
        qs = super(RunningcatalogDetail, self).get_queryset() \
            .select_related('xtrsrc')
        self.object = get_object_or_404(qs, id=self.kwargs['pk'])
        assoc_related = ['xtrsrc', 'xtrsrc__image', 'xtrsrc__image__band']
        return Assocxtrsource.objects.using(qs.db) \
            .filter(runcat=self.object.id) \
            .select_related(*assoc_related) \
            .order_by(self.get_order())

    def get_context_data(self, **kwargs):
        context = super(RunningcatalogDetail, self).get_context_data(**kwargs)
        context['object'] = self.object
        context['dataset'] = self.object.dataset
        return context



