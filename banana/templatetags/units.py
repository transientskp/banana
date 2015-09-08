from django import template
from django.utils.safestring import mark_safe
from banana.convert import deg_to_dms, deg_to_hms, deg_to_asec
from collections import OrderedDict

register = template.Library()


# Handling unicode in an URL string is tricky (damn you, mu!).
# So we use a map of ascii_key -> ((optionally unicode) prefix , power_of_ten)
# This also allows us to specify a key for the 'unity' case.
units_map = OrderedDict((
            # ('tera',('T', 12)),
            # ('giga',('G', 9)),
            # ('mega',('M', 6)),
            # ('kilo',('k', 3)),
            ('unity',('', 0)),
            ('milli',('m', -3)),
            ('micro',(u"\u03BC", -6)),
            # ('nano',('n', -9))
            ))
# NB key of None denotes the default, empty QueryDict case.
# This can be altered in local_settings!
units_map[None]= units_map['unity']

@register.filter
def flux_unit(value, unit_prefix):
    """
    Normalises a flux value according to unit prefix.

    Should be passed a string matching a key in ``units_map``
    (or the empty string, which is treated equivalent to ``None``)
    """
    if not value:
        return

    # When getting a QueryDict value in a template,
    # None is annoyingly converted to empty string
    if unit_prefix == '':
        unit_prefix = None
    if unit_prefix in units_map:
        power = units_map[unit_prefix][1]
        return float(value) / (10.0 ** power)
    else:
        return value

def sec2hms(seconds):
    """Seconds to hours, minutes, seconds"""
    hours, seconds = divmod(seconds, 60**2)
    minutes, seconds = divmod(seconds, 60)
    return int(hours), int(minutes), seconds

@register.filter
def scientific(value, precision=3):
    try: value = float(value)
    except: return
    if 0.001 < abs(value) < 1000 or value == 0:
        format = "%%.%sf" % (precision+1)
    else:
        format = "%%.%se" % precision
    return format % value


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
        result = "%02d<sup>h</sup> %02d<sup>m</sup> %02.1f<sup>s</sup>" % (h, m, s)
    if format_type == "dms":
        sign, d, m, s = deg_to_dms(float(value))
        result = "%s%02d&deg; %02d&prime; %04.1f&Prime;" % (sign, d, m, s)
    return mark_safe(result)


@register.filter
def format_ra_error(value):
    return float(value) / 15


@register.inclusion_tag('tags/sexagesimal.html', takes_context=True)
def sexagesimal(context, ra, decl, ra_err, decl_err):
    """
    units in degrees
    """
    context['ra'] = ra
    context['decl'] = decl
    context['ra_err'] = ra_err
    context['decl_err'] = decl_err
    return context


@register.filter
def deg2asec(deg):
    return deg_to_asec(deg)
