from django.db import models
from banana.db import check_database


class MultiDbMixin(object):
    """
    This mxin makes a Django class based views support multiple databases.

    It requires a db variable in your request.
    """
    def get_queryset(self):
        self.db_name = self.kwargs.get('db', 'default')
        check_database(self.db_name)
        return super(MultiDbMixin, self).get_queryset().using(self.db_name)

    def get_context_data(self, **kwargs):
        context = super(MultiDbMixin, self).get_context_data(**kwargs)
        context['db_name'] = self.db_name
        return context


class HybridTemplateMixin(object):
    """
    Checks the request for a format variable. If it is json or csv, will
    set the content_type and template accordingly.
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
    mixin view that checks for a dataset request variable and adds it to the
    context
    """
    def get_dataset_id(self):
        return self.request.GET.get("dataset", None)

    def get_context_data(self, *args, **kwargs):
        context = super(DatasetMixin, self).get_context_data(*args, **kwargs)
        context['dataset'] = self.get_dataset_id()
        return context
