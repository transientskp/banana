from banana.settings import MONGODB
from pymongo import Connection
from gridfs import GridFS


def fetch(filename):
    mongo_connection = Connection(host=MONGODB["host"], port=MONGODB["port"])
    gfs = GridFS(mongo_connection[MONGODB["database"]])
    return gfs.get_version(filename)
