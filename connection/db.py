from pymongo import MongoClient

def conection():
    client = MongoClient("mongodb://localhost:27017/")
    db = client['e-comerce']
    return db