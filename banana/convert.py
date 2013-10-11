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


def alpha(theta, dec):
    """
    Compute the RA expansion of an east-west angle theta for declination dec.
    http://research.microsoft.com/apps/pubs/default.aspx?id=64524 section 2.1.

    theta, dec in degrees.
    """
    if abs(dec) + theta > 89.9:
        return 180
    else:
        return math.degrees(
            abs(
                math.atan(
                    math.sin(math.radians(theta)) /
                    math.sqrt(abs(
                        math.cos(math.radians(dec - theta)) *
                        math.cos(math.radians(dec + theta))
                    ))
                )
            )
        )


def deg_to_asec(deg):
    return deg * ASEC_IN_DEGREE