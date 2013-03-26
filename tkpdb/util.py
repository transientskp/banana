import os.path
import monetdb.control
import pyfits
import aplpy
from matplotlib.figure import Figure

status_map = {
    1: 'running',
    2: '?',
    3: 'under maintenance',
}

def monetdb_list(host, port, passphrase):
    """
    returns a list of MonetDB databases
    """
    monetdb_control = monetdb.control.Control(host, port, passphrase)
    statuses = monetdb_control.status()

    for status in statuses:
        status['status'] = status_map[status['state']]

    return statuses
    #return [m['name'] for m in monetdb_control.status()]
"""

def image(path, sources=[]):
    if not os.path.exists(path):
        raise Exception("FITS file not available")


    image = aplpy.FITSFigure(path)
    image.show_colorscale()

    return
    hdu = pyfits.open(path, readonly=True)
    size = (5, 5)
    format='png'
    #figure = Figure(figsize=size)
    image = aplpy.FITSFigure(hdu, figure=figure, auto_refresh=False)
    image.show_grayscale()
    image.tick_labels.set_font(size=5)
    if sources:
        ra = [source['ra'] for source in sources]
        dec = [source['decl'] for source in sources]
        semimajor = [source['semimajor'] / 900 for source in sources]
        semiminor = [source['semiminor'] / 900 for source in sources]
        pa = [source['pa'] + 90 for source in sources]
        image.show_ellipses(ra, dec, semimajor, semiminor, pa,
                            facecolor='none', edgecolor='yellow', linewidth=1)

    def output(self, ):        if self.response:
            self.canvas.print_figure(self.response, format=format)
            self.image = self.response
        memfig = StringIO.StringIO()
        self.canvas.print_figure(memfig, format=format, transparent=True)
        encoded_png = StringIO.StringIO()
        encoded_png.write('data:image/%s;base64,\n' % format)
        encoded_png.write(base64.b64encode(memfig.getvalue()))
        self.image = encoded_png.getvalue()
        """