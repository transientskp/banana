"""
This is a bit of a hack to add a CSS class to a form element.

http://vanderwijk.info/blog/adding-css-classes-formfields-in-django-templates/
"""
from django import template
register = template.Library()


@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class": css})