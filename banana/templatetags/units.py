# -*- coding: UTF-8 -*-

from django import template
from django.utils.safestring import mark_safe
from banana.convert import deg_to_dms, deg_to_hms
import math

register = template.Library()


units = [('T', 12), ('G', 9), ('M', 6), ('k', 3),  ('', 0), ('m', -3),
         ('µ', -6), ('n', -9)]


def sec2hms(seconds):
    """Seconds to hours, minutes, seconds"""
    hours, seconds = divmod(seconds, 60**2)
    minutes, seconds = divmod(seconds, 60)
    return int(hours), int(minutes), seconds


@register.filter
def engineering(value, precision=3):
    if type(value) is str and not value.isdigit():
        return
    for symbol, power in units:
        if value > 10.0 ** power:
            format = "%%.%sf%%s" % precision
            return format % (value / (10.0 ** power), symbol)
    return value


@register.filter
def scientific(value, precision=3):
    if type(value) is str and not value.isdigit():
        return
    if 0.0001 < abs(value) < 1000 or value == 0:
        format = "%%.%sf" % precision
    else:
        format = "%%.%se" % precision
    return format % value


@register.filter
def mega(value, precision=3):
    if type(value) is str and not value.isdigit():
        return
    format = "%%.%sf" % precision
    return format % (value / (10.0 ** 6))


@register.filter
def datetime2seconds(value):
    return value.strftime('%s.%f')


@register.filter
def datetime2miliseconds(value):
    return float(value.strftime('%s.%f')) * 1000


@register.filter
def format_angle(value, format_type="time"):
    """
    format_type: time (hours, min, sec) or dms (degrees, arcmin, arcsec)
    """
    if format_type == "time":
        h, m, s = deg_to_hms(float(value))
        result = "%d<sup>h</sup>%d<sup>m</sup>%.1f<sup>s</sup>" % (h, m, s)
    if format_type == "dms":
        sign, d, m, s = deg_to_dms(float(value))
        result = "%s%d&deg; %d&prime; %.1f&Prime;" % (sign, d, m, s)
    return mark_safe(result)


@register.filter
def format_ra_error(value, decl):
    return float(value) / 15 * math.cos(decl)


def sexagesimal(context, ra, decl, ra_err, decl_err):
    context['ra'] = ra
    context['decl'] = decl
    context['ra_err'] = ra_err
    context['decl_err'] = decl_err
    return context


register.inclusion_tag('sexagesimal.html', takes_context=True)(sexagesimal)