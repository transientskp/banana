import aplpy
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


def plot(pyfits_hdu, size=5, sources=[]):
    """
    :param pyfits_hdu: a pyfits file object
    :size: size in inches
    :sources: a list of Extractedsource ORM models

    :returns: a matplotlib canvas which can be used to write the image to
              something (like a django HTTP resonse)
    """
    figure = Figure(figsize=(size, size))
    canvas = FigureCanvasAgg(figure)
    plot = aplpy.FITSFigure(pyfits_hdu, figure=figure, auto_refresh=False)
    plot.show_grayscale()
    plot.tick_labels.set_font(size=5)

    if sources:
        ra = [source.ra for source in sources]
        dec = [source.decl for source in sources]
        semimajor = [source.semimajor / 900 for source in sources]
        semiminor = [source.semiminor / 900 for source in sources]
        pa = [source.pa + 90 for source in sources]
        plot.show_ellipses(ra, dec, semimajor, semiminor, pa, facecolor='none',
                           edgecolor='yellow', linewidth=1)
    return canvas
