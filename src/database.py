from pymongo import MongoClient
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read('src/secrets.ini')
dbCred = config_object['DB']

def initDatabase(username, password):
    client = MongoClient(f"mongodb+srv://{username}:{password}@spotifycluster.8np2cmv.mongodb.net/?retryWrites=true&w=majority")
    return client.test_database

initDatabase(dbCred['username'], dbCred['password'])