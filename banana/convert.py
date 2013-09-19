import math

SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 60**2
SECONDS_IN_DAY = 24 * SECONDS_IN_HOUR
RADIANS_IN_CIRCLE = 2 * math.pi
ASEC_IN_AMIN = 60
ASEC_IN_DEGREE = 60**2


def deg_to_hms(deg):
    """
    convert degrees to sexagesimal hours, minutes, seconds
    """
    rad = deg * (math.pi/180)
    rad %= RADIANS_IN_CIRCLE
    seconds = SECONDS_IN_DAY * rad / RADIANS_IN_CIRCLE
    hours, seconds = divmod(seconds, SECONDS_IN_HOUR)
    minutes, seconds = divmod(seconds, SECONDS_IN_MINUTE)
    return hours, minutes, seconds


def deg_to_dms(deg):
    """
    convert degrees to sexagesimal  degrees, arecmin and arcsec
    """
    rad = deg * (math.pi/180)
    sign = "+" if rad >= 0 else "-"
    rad = abs(rad)
    seconds = math.degrees(rad) * ASEC_IN_DEGREE
    degrees, seconds = divmod(seconds, ASEC_IN_DEGREE)
    minutes, seconds = divmod(seconds, ASEC_IN_AMIN)
    return sign, degrees, minutes, seconds
