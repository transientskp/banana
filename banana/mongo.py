import os.path
from django.conf import settings
from pymongo import Connection
from gridfs import GridFS, NoFile
import pyfits


def fetch(filename):
    mongo_connection = Connection(host=settings.MONGODB["host"],
                                  port=settings.MONGODB["port"])
    gfs = GridFS(mongo_connection[settings.MONGODB["database"]])
    return gfs.get_last_version(filename)


def get_hdu(url):
    if hasattr(settings, 'MONGODB') and settings.MONGODB["enabled"]:
        try:
            mongo_file = fetch(url)
        except NoFile:
            return None
        return pyfits.open(mongo_file, mode="readonly")
    elif os.path.exists(url):
        if os.path.isdir(url):
            # probably a casa table
            return None
        else:
            # probably a fits file
            return pyfits.open(url, readonly=True)
    else:
        return None
