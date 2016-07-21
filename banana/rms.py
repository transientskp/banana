"""
RMS calculation for a dataset.
"""
from threading import Lock
from scipy.stats import norm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

# used for solving multithreaded drawing issue with matplotlib
lock = Lock()


def rms_histogram(all_rms, est_sigma, frequency_name, bin_num=50):
    """
    args:
        x: an array of RMS values
    """
    # best fit of data
    (mu, sigma) = norm.fit(all_rms)

    lock.acquire()
    fig = plt.figure(figsize=(5, 5))

    # the histogram of the data
    n, bins, patches = plt.hist(all_rms, bin_num, facecolor='green',
                                normed=1, alpha=0.6)

    thres_low = mu - sigma * est_sigma
    thres_high = mu + sigma * est_sigma

    # add a 'best fit' line
    y = mlab.normpdf(bins, mu, sigma)
    l = plt.plot(bins, y, 'r--', linewidth=2)

    plt.xlabel('RMS')
    plt.ylabel('Number of Images in Bin')
    plt.suptitle(r'$f={}\ \mu={:.3f},\ \sigma={:.3f}$'.format(frequency_name, mu, sigma))
    plt.title(r'$t={},\ t_{{\uparrow}}={:.3f},\ t_{{\downarrow}}={:.3f}$'.format(est_sigma, thres_low, thres_high))

    plt.axvline(x=thres_low, linewidth=2, color='k', linestyle='--')
    plt.axvline(x=thres_high, linewidth=2, color='k', linestyle='--')
    plt.grid(True)
    plt.xlim(mu - sigma * est_sigma * 1.5,
             mu + sigma * est_sigma * 1.5)

    plt.close()
    lock.release()
    return fig.canvas
