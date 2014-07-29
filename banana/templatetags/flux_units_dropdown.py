from banana.templatetags.units import units_map
from django import template

register = template.Library()

@register.inclusion_tag('tags/flux_units_dropdown.html',takes_context=True)
def flux_units_dropdown(context):
    simple_units_map = units_map.copy()
    del simple_units_map[None]
    context['units_map'] = simple_units_map
    return context
