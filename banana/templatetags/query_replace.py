from django import template

register = template.Library()

@register.simple_tag(takes_context = True)
def query_replace(context, field, value):
    """
    Gets HttpRequest from context, returns querystring with updated field-value.

    django.core.context_processors.request places a request in the default
    context used by generic class-based views.

    We grab the querydict from this request and update one of its fields
    before generating an updated querystring that may be appended to an URL.

    Refs:
    https://docs.djangoproject.com/en/1.6/ref/templates/api/#django-core-context-processors-request
    https://docs.djangoproject.com/en/1.6/ref/request-response/#querydict-objects
    """
    dict_ = context['request'].GET.copy()
    dict_[field] = value
    return dict_.urlencode()
