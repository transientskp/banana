import os.path
from django.conf import settings
from pymongo import MongoClient
from gridfs import GridFS, NoFile
from astropy import log as astro_log
import astropy.io.fits
import logging

astro_log.setLevel('ERROR')
logger = logging.getLogger(__name__)


def fetch(filename):
    mongo_connection = MongoClient(host=settings.MONGODB["host"],
                                  port=settings.MONGODB["port"])
    gfs = GridFS(mongo_connection[settings.MONGODB["database"]])
    return gfs.get_last_version(filename)


def get_hdu(url):
    if not url:
        return None
    if hasattr(settings, 'MONGODB') and settings.MONGODB["enabled"]:
        try:
            mongo_file = fetch(url)
        except NoFile:
            logging.error("cant find %s on mongo server")
            return None
        mongo_file.closed = False  # astropy assumes a closed property
        return astropy.io.fits.open(mongo_file)
    elif os.path.exists(url):
        if os.path.isdir(url):
            # probably a casa table
            logger.error("can't open dir %s as FITS" % url)
            return None
        else:
            # probably a fits file
            return astropy.io.fits.open(url)
    else:
        logger.error("no mongodb in config and file %s doesn't exists" % url)
        return None
