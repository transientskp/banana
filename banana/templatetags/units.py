# -*- coding: UTF-8 -*-

from django import template
from django.utils.safestring import mark_safe
from banana.convert import deg_to_dms, deg_to_hms


register = template.Library()


units = [('T', 12), ('G', 9), ('M', 6), ('k', 3),  ('', 0), ('m', -3),
         ('µ', -6), ('n', -9)]


def sec2hms(seconds):
    """Seconds to hours, minutes, seconds"""
    hours, seconds = divmod(seconds, 60**2)
    minutes, seconds = divmod(seconds, 60)
    return int(hours), int(minutes), seconds


def dectodms(decdegs):
    """Convert Declination in decimal degrees format to hours, minutes,
    seconds format.

    Keyword arguments:
    decdegs -- Dec. in degrees format

    Return value:
    dec -- list of 3 values, [degrees,minutes,seconds]

    """

    sign = -1 if decdegs < 0 else 1
    decdegs = abs(decdegs)
    if decdegs > 90:
        raise ValueError("coordinate out of range")
    decd = int(decdegs)
    decm = int((decdegs - decd) * 60)
    decs = (((decdegs - decd) * 60) - decm) * 60
    # Necessary because of potential roundoff errors
    if decs - 60 > -1e-7:
        decm += 1
        decs = 0
        if decm == 60:
            decd += 1
            decm = 0
            if decd > 90:
                raise ValueError("coordinate out of range")

    if sign == -1:
        if decd == 0:
            if decm == 0:
                decs = -decs
            else:
                decm = -decm
        else:
            decd = -decd
    return decd, decm, decs


def ratohms(radegs):
    """Convert RA in decimal degrees format to hours, minutes,
    seconds format.

    Keyword arguments:
    radegs -- RA in degrees format

    Return value:
    ra -- tuple of 3 values, [hours,minutes,seconds]

    """

    radegs %= 360
    raseconds = radegs * 3600 / 15.0
    return sec2hms(raseconds)


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
def format_angle(value, format_type):
    if format_type == "time":
        h, m, s = ratohms(value)
        result = "%d:%d:%.1f" % (h, m, s)
    if format_type == "dms":
        d, m, s = dectodms(value)
        if d > 0:
            sign = '+'
        else:
            sign = '-'
        result = "%s%d:%d:%.1f" % (sign, d, m, s)
    return result


@register.filter
def datetime2seconds(value):
    return value.strftime('%s.%f')


@register.filter
def datetime2miliseconds(value):
    return float(value.strftime('%s.%f')) * 1000


@register.filter
def format_angle(value, format_type="time"):
    if format_type == "time":
        h, m, s = deg_to_hms(float(value))
        result = "%d<sup>h</sup> %d<sup>m</sup> %.1f<sup>s</sup>" % (h, m, s)
    if format_type == "dms":
        sign, d, m, s = deg_to_dms(float(value))
        result = "%s%d&deg; %d&prime; %.1f&Prime;" % (sign, d, m, s)
    return mark_safe(result)