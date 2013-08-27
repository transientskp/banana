"""
All views that visualise a model object (banana.models)
"""
from django.db.models import Count
from django.views.generic import DetailView

import banana.image
from banana.models import Image, Monitoringlist, Dataset, Extractedsource,\
    Runningcatalog, Transient
from banana.views.mixins import MultiDbMixin, HybridTemplateMixin


class ImageDetail(MultiDbMixin, DetailView):
    model = Image

    def get_size(self):
        image_size = 4  # in inches
        return image_size

    def get_context_data(self, **kwargs):
        context = super(ImageDetail, self).get_context_data(**kwargs)
        context['image_size'] = self.get_size()
        context['sources'] = banana.image.extracted_sources_pixels(self.object,
                                                               self.get_size())
        context['image'] = self.object
        return context

    def get_queryset(self):
        """ Anotate the image a bit
        """
        qs = super(ImageDetail, self).get_queryset()

        related = ['skyrgn', 'dataset', 'band', 'rejections']
        return qs.prefetch_related(*related).using(
            self.db_name).annotate(
            num_extractedsources=Count('extractedsources')
        )


class BigImageDetail(ImageDetail):
    template_name = "banana/bigimage_detail.html"

    def get_size(self):
        size = int(self.request.GET.get("size", 8))  # in inches
        dpi = 100
        return size * dpi


class MonitoringlistDetail(MultiDbMixin, DetailView):
    model = Monitoringlist

    def get_context_data(self, **kwargs):
        context = super(MonitoringlistDetail, self).get_context_data(**kwargs)
        context['monitoringlist'] = self.object
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
        context['dataset'] = self.object
        context['num_extractedsources'] = Extractedsource.objects.using(
            self.db_name).filter(image__in=images.all()).count()
        context['images'] = images
        context['images_per_band'] = images_per_band
        return context


class RunningcatalogDetail(MultiDbMixin, HybridTemplateMixin, DetailView):
    model = Runningcatalog

    def get_context_data(self, **kwargs):
        context = super(RunningcatalogDetail, self).get_context_data(**kwargs)
        context['runningcatalog'] = self.object
        context['lightcurve'] = self.object.lightcurve()
        return context


class ExtractedSourceDetail(MultiDbMixin, DetailView):
    model = Extractedsource

    def get_context_data(self, **kwargs):
        context = super(ExtractedSourceDetail, self).get_context_data(**kwargs)
        context['extractedsource'] = self.object
        return context


class TransientDetail(MultiDbMixin, HybridTemplateMixin, DetailView):
    model = Transient

    def get_context_data(self, **kwargs):
        context = super(TransientDetail, self).get_context_data(**kwargs)
        context['lightcurve'] = self.object.lightcurve()
        return context
