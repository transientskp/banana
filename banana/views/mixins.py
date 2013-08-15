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

    def get_template_names(self):
        format = self.request.GET.get('format', 'html')
        if format == 'json':
            self.content_type = 'application/json'
            extension = format
        elif format == 'csv':
            self.content_type = 'text/csv'
            extension = format
        else:
            extension = 'html'

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
                                extension)]

    def render_to_response(self, context, **response_kwargs):
        format = self.request.GET.get('format', 'html')
        if format == 'json':
            response_kwargs['content_type'] = 'application/json'
        elif format == 'csv':
            response_kwargs['content_type'] = 'text/csv'
        return super(HybridTemplateMixin, self).render_to_response(context, **response_kwargs)


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
