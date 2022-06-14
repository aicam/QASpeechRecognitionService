import pymongo

def create_connection(connectionString):
    myclient = pymongo.MongoClient(connectionString)

