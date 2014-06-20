import numpy
import aplpy
from matplotlib import pyplot
from banana.mongo import get_hdu


# colors for the extracted types
#  0: blind fit, 1: forced fit, 2: manual monitoring
source_colors = ['yellow', 'lightgreen', 'cyan']


def extract_props(sources, pyfits_hdu):
    """
    Extracts relevant information from a list of extracted sources.

    args:
        sources: a list of extracted sources
        pyfits_hdu: a pyfits header

    returns:
        a list of lists for ra, dec, semimajor, semiminor, pa, color
    """
    # If the image has a reference declination pointing to the north
    # celestial pole (ie, CRVAL2=90), our APLpy will incorrectly plot them
    # with an RA 180 degrees wrong. We rotate them back here. See Trap
    # issue #4599 for (much) more discussion.
    if "CRVAL2" in pyfits_hdu[0].header and \
                   pyfits_hdu[0].header["CRVAL2"] == 90:
        ra = [(source.ra + 180) % 360 for source in sources]
    else:
        ra = [source.ra for source in sources]
    dec = [source.decl for source in sources]
    semimajor = [source.semimajor / 900 for source in sources]
    semiminor = [source.semiminor / 900 for source in sources]
    pa = [source.pa + 90 for source in sources]
    color = [source_colors[source.extract_type] for source in sources]

    return ra, dec, semimajor, semiminor, pa, color


def image_plot(pyfits_hdu, size=5, sources=[], transients=[]):
    """
    Plot image from fits HDU and draw circles around sources.

    args:
        pyfits_hdu: a pyfits file object
        size: size in inches
        sources: a list of Extractedsource ORM models
        transients: a list of sources that are part of a transient lightcurve

    Returns:
        a matplotlib canvas which can be used to write the image to
        something (like a django HTTP resonse)
    """
    fig = pyplot.figure(figsize=(size, size))
    plot = aplpy.FITSFigure(pyfits_hdu, figure=fig, subplot=[0, 0, 1, 1],
                            auto_refresh=False)
    plot.show_grayscale()
    plot.axis_labels.hide()
    plot.tick_labels.hide()
    plot.ticks.hide()

    if not sources:
        return fig.canvas

    ra, dec, semimajor, semiminor, pa, color = extract_props(sources,
                                                              pyfits_hdu)
    plot.show_ellipses(ra, dec, semimajor, semiminor, pa, facecolor='none',
                       edgecolor=color, linewidth=1,)

    # and the same for transient sources
    ra, dec, semimajor, semiminor, pa, color = extract_props(transients,
                                                              pyfits_hdu)
    plot.show_circles(ra, dec, 0.1, color='blue')
    return fig.canvas


def extracted_sources_pixels(image, size):
    """
    :param image: a banana.models.Image object
    :returns: a list of sources of an image
    """
    hdu = get_hdu(image.url)
    if not hdu:
        return None

    # make an image
    fig = pyplot.figure(figsize=(size, size))
    plot = aplpy.FITSFigure(hdu, figure=fig, subplot=[0, 0, 1, 1],
                            auto_refresh=False)

    # get source info from database
    sources = image.extractedsources.all()
    ids = [source.id for source in sources]
    # If the image has a reference declination pointing to the north
    # celestial pole (ie, CRVAL2=90), our APLpy will incorrectly plot them
    # with an RA 180 degrees wrong. We rotate them back here. See Trap
    # issue #4599 for (much) more discussion.
    if "CRVAL2" in hdu[0].header and hdu[0].header["CRVAL2"] == 90:
        x_world = [(source.ra + 180) % 360 for source in sources]
    else:
        x_world = [source.ra for source in sources]
    y_world = [source.decl for source in sources]
    w_world = numpy.array([source.semimajor / 900 for source in sources])
    h_world = numpy.array([source.semiminor / 900 for source in sources])

    # first convert positions to matplotlib image coordinates
    x_plot, y_plot = plot.world2pixel(x_world, y_world)
    arcperpix = aplpy.wcs_util.arcperpix(plot._wcs)
    w_plot = 3600.0 * w_world / arcperpix
    h_plot = 3600.0 * h_world / arcperpix

    # then transform them to true pixel coordinates
    ax = fig.axes[0]
    xy_pixels = ax.transData.transform(numpy.vstack([x_plot, y_plot]).T)
    x_px, y_px = xy_pixels.T

    # In matplotlib, 0,0 is the lower left corner, whereas it's usually the
    # upper right for most image software, so we'll flip the y-coords
    fig_width, fig_height = fig.canvas.get_width_height()
    y_px = fig_height - y_px

    # because of an unknown reason we need to scale the coordinates with 25%
    y_px *= 1.25
    x_px *= 1.25

    # create average size since areamap can only draw circles
    size_px = (w_plot + h_plot) / 4
    return zip(ids, list(x_px), list(y_px), list(size_px))


def extractedsource(hdu, source, size=1):
    fig = pyplot.figure(figsize=(size, size))
    fits = aplpy.FITSFigure(hdu, figure=fig, subplot=[0, 0, 1, 1],
                            auto_refresh=False)
    #fits.show_grayscale()
    fits.show_colorscale()
    fits.axis_labels.hide()
    fits.tick_labels.hide()
    fits.ticks.hide()
    fits.recenter(source.ra, source.decl, width=source.semimajor / 90,
                  height=source.semiminor / 90)
    return fig.canvas
