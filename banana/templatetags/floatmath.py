from django import template

register = template.Library()


@register.filter
def float_add(field, value):
    return str(float(field) + float(value))


@register.filter
def float_substract(field, value):
    return str(float(field) - float(value))