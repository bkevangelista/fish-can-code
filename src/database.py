from pymongo import MongoClient
from configparser import ConfigParser
import datetime
from pprint import pprint
import sys

import spotify

config_object = ConfigParser()
config_object.read('src/secrets.ini')
dbCred = config_object['DB']

def initDatabase(username, password):
    client = MongoClient(f"mongodb+srv://{username}:{password}@spotifycluster.8np2cmv.mongodb.net/?retryWrites=true&w=majority")
    return client.test_database

def insertSongsIntoDB(collection, spotifyObject, playlists):
    #New approach: Insert into database after going through every song in each playlist
    allSongs = []
    for playlist in playlists:
        playlistSongs = spotify.getSongsFromPlaylist(spotifyObject, playlist['playlistID'])
        for song in playlistSongs:
            if collection.find_one({"songTitle": song['songTitle'], "artists": song['artists'], "album": song['album']}):
                continue
            else:
                allSongs.append(song)
        
        if allSongs:
            print("Inserting into DB")
            tracks.insert_many(allSongs)
            allSongs.clear()
        else:
            print("Skipped over all songs in playlist")


db = initDatabase(dbCred['username'], dbCred['password'])
sp = spotify.initializeSpotifyConnection()

allUsernames = [
                'spotify'
            ]

playlists = spotify.compileAllPlaylists(sp, allUsernames)

tracks = db.tracks

insertSongsIntoDB(tracks, sp, playlists)
print("done!")

