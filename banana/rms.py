"""
RMS calculation for a dataset.
"""
import math
import numpy
from scipy.optimize import leastsq
from matplotlib import pyplot


def norm2(x, mean, sd):
    """
    creates a normal distribution in a simple array for plotting
    """
    normdist = []
    for i in range(len(x)):
        normdist += [1.0/(sd*numpy.sqrt(2*numpy.pi))*numpy.exp(-(x[i] - mean)**2/(2*sd**2))]
    return numpy.array(normdist)


def guess_p(x):
    """
    estimate the mean and rms as initial inumpy.ts to the Gaussian fitting
    """
    if len(x) == 0:
        return [0, 0, 0]
    median = numpy.median(x)
    temp = [n*n-(median*median) for n in x]
    rms = math.sqrt((abs(sum(temp))/len(x)))
    return [median, rms, math.sqrt(len(x))]


def res(p, y, x):
    """
    calculate residuals between data and Gaussian model
    """
    m1, sd1, a = p
    y_fit = a*norm2(x, m1, sd1)
    err = y - y_fit
    return err


def rms_histogram(x, sigma=8, name='rms_plot'):
    """
    args:
        x: an array of RMS values

    returns:
        a matplotlib figure canvas
    """
    p = guess_p(x)
    hist_x = numpy.histogram(x, bins=50)              # histogram of data
    range_x = [hist_x[1][n]+(hist_x[1][n+1]-hist_x[1][n])/2. for n in range(len(hist_x[1])-1)]
    plsq = leastsq(res, p, args=(hist_x[0], range_x))  # fit Gaussian to data
    fit2 = plsq[0][2]*norm2(range_x, plsq[0][0], plsq[0][1])  # create Gaussian distribution for plotting on graph
    sigcut = plsq[0][0]+plsq[0][1]*sigma  # max threshold defined as (mean + RMS * sigma)
    sigcut2 = plsq[0][0]-plsq[0][1]*sigma  # min threshold defined as (mean - RMS * sigma)

    xvals = numpy.arange(int(min(range_x)), int(max(range_x)+1.5), 1)
    xlabs = [str(10.**a) for a in xvals]
    fig = pyplot.figure(figsize=(5, 5))
    pyplot.hist(x, bins=50, histtype='stepfilled')
    pyplot.plot(range_x, fit2, 'r-', linewidth=3)
    pyplot.axvline(x=sigcut, linewidth=2, color='k', linestyle='--')
    pyplot.axvline(x=sigcut2, linewidth=2, color='k', linestyle='--')
    pyplot.xticks(xvals, xlabs)
    pyplot.xlabel(name)
    pyplot.ylabel('Number of images')
    return fig.canvas