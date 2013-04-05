import numpy
import aplpy
import time
import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection


def nsources_plot(pyfits_hdu, size=5, sources=[]):
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


def transient_plot(lc, T0=None, images=None, trigger_index=None, size=5):
    figure = Figure(figsize=(size, size))
    canvas = FigureCanvasAgg(figure)
    times = numpy.array([time.mktime(point.xtrsrc.image.taustart_ts.timetuple()) for point in lc])
    tau_times = [point.xtrsrc.image.tau_time / 2. for point in lc]
    fluxes = [point.xtrsrc.f_int for point in lc]
    errors = [point.xtrsrc.f_int_err for point in lc]
    bands = [point.xtrsrc.image.band.freq_central for point in lc]
    #stokes = [point[6] for point in lc]
    bandnames = ["%.1f MHz" % (point.xtrsrc.image.band.freq_central / 1e6,) for point in lc]

    # colors to use for band labeling.
    colors = 'bgrcmykw'

    # This makes a mapping from band ID to (color, name)
    unique_bands = list(set(zip(bands, bandnames)))
    mapping_list = []
    for index, (band,name) in enumerate(unique_bands):
        color = colors[index % len(colors)]
        mapping_list.append((band, (color, name)))
    mapping = dict(mapping_list)

    ecolor = [mapping[x][0] for x in bands]

    if T0 is None:
        tmin = sorted(times)[0]
        if images:
            tmin2 = time.mktime(sorted(zip(*images)[0])[0].timetuple())
            if tmin2  < tmin:
                tmin = tmin2
        tmin = datetime.datetime.fromtimestamp(tmin)
        T0 = datetime.datetime(tmin.year, tmin.month, tmin.day, 0, 0, 0)
    tdiff = T0 - datetime.datetime(1970, 1, 1)
    tdiff = (tdiff.microseconds + (tdiff.seconds + tdiff.days * 86400) * 1e6) / 1e6
    times -= tdiff
    axes = figure.add_subplot(1, 1, 1)
    axes.errorbar(x=times, y=fluxes, yerr=errors, xerr=numpy.array(tau_times)/2., fmt='bo')
    axes.scatter(x=times, y=fluxes, color=ecolor, zorder=100)

    # construct legend
    sorted_mapping = sorted(mapping.values(), key=lambda x: x[1])
    band_colors, band_names = zip(*sorted_mapping)
    legend_elements = [Rectangle((0, 0), 1, 1, fc=c) for c in band_colors]
    axes.legend(legend_elements, band_names, loc='best')

    if trigger_index is not None:
        axes.errorbar(x=times[trigger_index], y=fluxes[trigger_index], fmt='o', mec='r', ms=15., mfc='None')
    ylimits = axes.get_ylim()
    if images:
        images = zip(*images)
        x = numpy.array([time.mktime(x.timetuple()) for x in images[0]]) - tdiff
        xerr = numpy.array(images[1])/2.
        patches = [Rectangle((xx - xxerr, ylimits[0]), xxerr, ylimits[1]-ylimits[0])
                   for xx, xxerr in zip(x, xerr)]
        patches = PatchCollection(patches, alpha=0.3, linewidth=0, visible=True, color='r')
        axes.add_collection(patches)
    axes.set_xlabel('Seconds since %s' % T0.strftime('%Y-%m-%dT%H:%M:%S'))
    axes.set_ylabel('Flux (Jy)')
    return canvas




def scatter_plot(extractedsources, size=5):
    """Plot positions of all counterparts for all (unique) sources for
    the given dataset.

    The positions of all (unique) sources in the running catalog are
    at the centre, whereas the positions of all their associated
    sources are scattered around the central point.  Axes are in
    arcsec relative to the running catalog position.
    """
    figure = Figure(figsize=(size, size))
    canvas = FigureCanvasAgg(figure)

    # no list comprehension here since we use raw query
    ra_dist_arcsec= []
    decl_dist_arcsec = []
    ra_err = []
    decl_err = []
    for source in extractedsources:
        ra_dist_arcsec.append(source.ra_dist_arcsec)
        decl_dist_arcsec.append(source.decl_dist_arcsec)
        ra_err.append(source.ra_err / 2)
        decl_err.append(source.decl_err / 2)

    axes = figure.add_subplot(1, 1, 1)
    axes.errorbar(ra_dist_arcsec, decl_dist_arcsec, xerr=ra_err, yerr=decl_err,
                  fmt='+', color='b', label="xtr")
    axes.set_xlabel(r'RA (arcsec)')
    axes.set_ylabel(r'DEC (arcsec)')
    lim = 1 + max(int(numpy.trunc(max(abs(min(ra_dist_arcsec)),
                                      abs(max(ra_dist_arcsec))))),
                  int(numpy.trunc(max(abs(min(decl_dist_arcsec)),
                                      abs(max(decl_dist_arcsec))))))
    axes.set_xlim(xmin=-lim, xmax=lim)
    axes.set_ylim(ymin=-lim, ymax=lim)
    axes.grid(False)
    # Shifts plot spacing to ensure that axes labels are displayed
    figure.tight_layout()
    return canvas
