from django.db import models
from django.shortcuts import get_object_or_404
from banana.models import Dataset


class HybridTemplateMixin(object):
    """
    Assigns a default ``template_name``, and checks the request for a format.

    If the format specified in the querystring is json or csv, this will change
    the ``content_type`` and ``template_name`` accordingly.

    If template name is not explicitly set, we assign one based on the
    object or model in the view. We derive the template path as:

        <app_label>/<object_name.lower()><template_name_suffix><extension>

    where ``template_name_suffix`` is something like '_list' or '_detail'
    (inherited from the Django standard class views)
    e.g.:

        banana/extractedsource_list.html
    
        banana/extractedsource_detail.html
    """
    def dispatch(self, *args, **kwargs):
        self.extension = self.request.GET.get('format', 'html')
        assert(self.extension in ('html', 'csv', 'json'))
        return super(HybridTemplateMixin, self).dispatch(*args, **kwargs)

    def get_template_names(self):
        # override manual set template name to match content type
        if self.template_name and self.template_name.endswith('html'):
            return self.template_name[:-4] + self.extension

        if hasattr(self, 'object') and \
                isinstance(self.object, models.Model) and \
                hasattr(self.object, 'model'):
            opts = self.object.model._meta
        elif hasattr(self, 'model') and self.model is not None and \
                issubclass(self.model, models.Model):
            opts = self.model._meta
        else:
            return []

        return ["%s/%s%s.%s" % (opts.app_label,
                                opts.object_name.lower(),
                                self.template_name_suffix,
                                self.extension)]

    def get_paginate_by(self, *args, **kwargs):
        if self.extension in ('csv', 'json'):
            return False
        return super(HybridTemplateMixin, self).get_paginate_by(*args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.extension == 'json':
            response_kwargs['content_type'] = 'application/json'
        elif self.extension == 'csv':
            response_kwargs['content_type'] = 'text/csv'
        return super(HybridTemplateMixin,
                     self).render_to_response(context, **response_kwargs)


class SortListMixin(object):
    """
    View mixin which provides sorting for ListView.
    """
    default_order = 'id'

    def get_order(self):
        return self.request.GET.get('order', self.default_order)

    def get_queryset(self):
        order = self.get_order()

        # TODO: this does not work with annotated fields
        #if order not in self.model._meta.get_all_field_names():
        #    raise Http404

        qs = super(SortListMixin, self).get_queryset()
        return qs.order_by(order)

    def get_context_data(self, *args, **kwargs):
        context = super(SortListMixin, self).get_context_data(*args, **kwargs)
        order = self.get_order()
        context.update({
            'order': order,
        })
        return context


class DatasetMixin(object):
    """
    Mixin view that adds the 'dataset' request variable to the context.
    """

    # if the queryset dataset filter has a different name, you should
    # override this here.
    dataset_field = 'dataset'

    def get_dataset_id(self):
        return self.request.GET.get("dataset", None)

    def get_context_data(self, *args, **kwargs):
        context = super(DatasetMixin, self).get_context_data(*args, **kwargs)
        context['dataset'] = get_object_or_404(Dataset,
                                               id=self.get_dataset_id)
        return context

    def filter_queryset(self, qs):
        dataset_id = self.get_dataset_id()
        if dataset_id:
            qs = qs.filter(**{self.dataset_field: dataset_id})
        return qs

    def get_queryset(self):
        qs = super(DatasetMixin, self).get_queryset()
        return self.filter_queryset(qs)



class FluxViewMixin(object):
    """
    Mixin view that adds the 'flux_prefix' request variable to the context.
    """
    def get_context_data(self, *args, **kwargs):
        context = super(FluxViewMixin, self).get_context_data(*args, **kwargs)
        context['flux_prefix'] = self.request.GET.get('flux_prefix', None)
        return context
