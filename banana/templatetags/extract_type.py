from django import template

register = template.Library()

extract_types = {
    0: "blind (0)",
    1: "forced (1)",
    2: "manual (2)",
}


@register.filter
def extract_type(value):
    """
    Returns a string format for the extract_type column in the
    extracted source table.
    """
    return extract_types[value]