from django.conf import settings
from pymongo import Connection
from gridfs import GridFS


def fetch(filename):
    mongo_connection = Connection(host=settings.MONGODB["host"], port=settings.MONGODB["port"])
    gfs = GridFS(mongo_connection[settings.MONGODB["database"]])
    return gfs.get_version(filename)
