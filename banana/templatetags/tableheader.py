from django import template
from banana.templatetags.units import units_map

register = template.Library()

@register.inclusion_tag('tags/tableheader.html', takes_context=True)
def tableheader(context, field, description=False):
    if not description:
        description = field.title()
    context['field'] = field
    flux_prefix = context['request'].GET.get('flux_prefix', None)
    if flux_prefix in units_map:
        if 'Jy' in description:
            description = description.replace('Jy',
                                              units_map[flux_prefix][0]+u'Jy')
    context['description'] = description
    return context

