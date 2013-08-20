from django import template

register = template.Library()

def tableheader(context, field, description=False):
    if not description:
        description = field.title()
    context['field'] = field
    context['description'] = description
    return context

register.inclusion_tag('tableheader.html', takes_context=True)(tableheader)