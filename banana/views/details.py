"""
All views that visualise a model object (banana.models)
"""
from django.db.models import Count
from django.views.generic import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
import banana.image
from banana.models import Image, Dataset, Extractedsource, Runningcatalog,\
                          Transient
from banana.views.mixins import MultiDbMixin, HybridTemplateMixin,\
                                DatasetMixin, SortListMixin
from collections import OrderedDict


class ImageDetail(SortListMixin, MultiDbMixin, DatasetMixin,
                      HybridTemplateMixin, ListView):
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
        context = super(ImageDetail, self).get_context_data(**kwargs)
        context['image_size'] = self.get_size()
        context['pixels'] = banana.image.extracted_sources_pixels(self.object,
                                                               self.get_size())
        context['object'] = self.object
        return context


class BigImageDetail(MultiDbMixin, DatasetMixin, DetailView):
    template_name = "banana/bigimage_detail.html"
    model = Image
    image_size = 8

    def get_context_data(self, **kwargs):
        context = super(BigImageDetail, self).get_context_data(**kwargs)
        context['image_size'] = self.image_size
        context['sources'] = banana.image.extracted_sources_pixels(self.object,
                                                               self.image_size)
        return context


class DatasetDetail(MultiDbMixin, DetailView):
    model = Dataset

    def get_context_data(self, **kwargs):
        context = super(DatasetDetail, self).get_context_data(**kwargs)

        # annotated images
        related = ['band']
        images = Image.objects.using(self.db_name).filter(dataset=self.object
                ).prefetch_related(*related).annotate(
                    num_extractedsources=Count('extractedsources')
                ).order_by('taustart_ts')
        images_per_band = {}
        for image in images:
            label = str(image.band)
            images_per_band.setdefault(label, [])
            images_per_band[label].append(image.num_extractedsources)
        images_per_band = OrderedDict(sorted(images_per_band.iteritems(),
                                             key=lambda x: x[0]))
        context['dataset'] = self.object
        context['num_extractedsources'] = Extractedsource.objects.using(
            self.db_name).filter(image__in=images.all()).count()
        context['images'] = images
        context['images_per_band'] = images_per_band
        return context


class ExtractedSourceDetail(MultiDbMixin, DetailView):
    model = Extractedsource

    def get_context_data(self, **kwargs):
        context = super(ExtractedSourceDetail, self).get_context_data(**kwargs)
        context['extractedsource'] = self.object
        return context


class TransientDetail(SortListMixin, MultiDbMixin, DatasetMixin,
                      HybridTemplateMixin, ListView):
    model = Transient
    paginate_by = 10
    template_name = "banana/transient_detail.html"

    def get_queryset(self):
        qs = super(TransientDetail, self).get_queryset()
        self.transient = get_object_or_404(qs, id=self.kwargs['pk'])
        return self.transient.lightcurve().order_by(self.get_order())

    def get_context_data(self, **kwargs):
        context = super(TransientDetail, self).get_context_data(**kwargs)
        context['object'] = self.transient
        return context


class RunningcatalogDetail(SortListMixin, MultiDbMixin, DatasetMixin,
                           HybridTemplateMixin, ListView):
    model = Runningcatalog
    paginate_by = 10
    default_order = 'image__taustart_ts'
    template_name = "banana/runningcatalog_detail.html"

    def get_queryset(self):
        qs = super(RunningcatalogDetail, self).get_queryset()
        self.runningcatalog = get_object_or_404(qs, id=self.kwargs['pk'])
        return self.runningcatalog.lightcurve().order_by(self.get_order())

    def get_context_data(self, **kwargs):
        context = super(RunningcatalogDetail, self).get_context_data(**kwargs)
        context['object'] = self.runningcatalog
        return context
