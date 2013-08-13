from django import template

register = template.Library()

def tableheader(context, field):
    context['field'] = field
    return context

register.inclusion_tag('tableheader.html', takes_context=True)(tableheader)