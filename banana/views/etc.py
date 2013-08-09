import sys
from django.conf import settings
from django.shortcuts import render
from django.views.generic.detail import SingleObjectTemplateResponseMixin,\
    BaseDetailView
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from banana.db import check_database



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


class MultiDbMixin(object):
    """
    This mxin makes a Django class based views support multiple databases.

    It requires a db_name variable in your request.
    """
    def get_queryset(self):
        self.db_name = self.kwargs['db_name']
        check_database(self.db_name)
        return self.model._default_manager.all().using(self.db_name)

    def get_context_data(self, **kwargs):
        context = super(MultiDbMixin, self).get_context_data(**kwargs)
        context['db_name'] = self.db_name
        return context


class HybridSingleObjectTemplateResponseMixin(SingleObjectTemplateResponseMixin):

    def get_template_names(self):
        """
        This does the same as ``get_template_names`` in
        ``SingleObjectTemplateResponseMixin`` but checks the request for a
        ``format`` variable and sets template and content_type accordingly.
        """
        format = self.request.GET.get('format', 'html')
        if format == 'json':
            self.content_type = 'application/json'
            extension = format
        elif format == 'csv':
            self.content_type = 'text/csv'
            extension = format
        else:
            self.content_type = extension = 'html'

        try:
            names = super(SingleObjectTemplateResponseMixin, self).get_template_names()
        except ImproperlyConfigured:
            # If template_name isn't specified, it's not a problem --
            # we just start with an empty list.
            names = []

        # If self.template_name_field is set, grab the value of the field
        # of that name from the object; this is the most specific template
        # name, if given.
        if self.object and self.template_name_field:
            name = getattr(self.object, self.template_name_field, None)
            if name:
                names.insert(0, name)

        # The least-specific option is the default <app>/<model>_detail.html;
        # only use this if the object in question is a model.
        if isinstance(self.object, models.Model):
            names.append("%s/%s%s.%s" % (
                self.object._meta.app_label,
                self.object._meta.object_name.lower(),
                self.template_name_suffix,
                extension
            ))
        elif hasattr(self, 'model') and self.model is not None and issubclass(self.model, models.Model):
            names.append("%s/%s%s.%s" % (
                self.model._meta.app_label,
                self.model._meta.object_name.lower(),
                self.template_name_suffix,
                extension
            ))
        return names


class HybridDetailView(HybridSingleObjectTemplateResponseMixin, BaseDetailView):
    pass