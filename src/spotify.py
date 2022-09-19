import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from configparser import ConfigParser
import json

def listAllPlaylists(spotifyObject, username):
    allPlaylists = []
    playlists = spotifyObject.user_playlists(username)
    for playlist in playlists['items']:
        allPlaylists.append({
            "playlistName": playlist['name'],
            "playlistID": playlist['id']
        })
    return allPlaylists

#Very slow to go through all liked songs
def getSongsFromPlaylist(spotifyObject, limit, offset, playlistID):
    tracks = []
    results = spotifyObject.playlist_tracks(playlist_id=playlistID, limit=limit, offset=offset)
    for idx, item in enumerate(results['items']):
        track = item['track']
        allArtists = []
        for artist in track['artists']:
            allArtists.append(artist['name'])

        trackInfo = {
            "songTitle": str(track['name']),
            "artists": allArtists,
            "album": str(track['album']['name'])
        }
        tracks.append(trackInfo)
    return tracks
    # for idx, item in enumerate(results['items']):
    #     track = item['track']
    #     print(idx+1, track['artists'][0]['name'], " – ", track['name'])

#Get song information based on a search query
def getSongInformation(searchObject):
    songInfo = {}

    item = searchObject['tracks']['items'][0]
    songInfo['album'] = item['album']['name']
    songInfo['title'] = item['name']

    allArtists = []
    for artist in item['album']['artists']:
        allArtists.append(artist['name'])
    songInfo['artists'] = allArtists

    #Also get the spotify URL to the song
    songInfo['songUrl'] = item['external_urls']['spotify']

    return songInfo

#Initialize connection to Spotify
config_object = ConfigParser()
config_object.read('src/secrets.ini')
spotifyCredentials = config_object["SPOTIFY"]
clientID = spotifyCredentials["CLIENT_ID"]
clientSecret = spotifyCredentials["CLIENT_SECRET"]
uri = spotifyCredentials["URI"]

sp = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth
                                (client_id=clientID,
                                client_secret=clientSecret,
                                redirect_uri=uri,
                                scope="user-library-read playlist-read-private"))
username = sp.me()['id']
kaitlinPlaylists = listAllPlaylists(sp, 'kate.sm')
print(json.dumps(kaitlinPlaylists, sort_keys=True, indent=4))

tracks = getSongsFromPlaylist(sp, 5, 0, kaitlinPlaylists[5]["playlistID"])
print(json.dumps(tracks, indent=4))


# # Simple program that allows user to search a song and play it through the web browser
# while True:
#     print("Welcome")
#     print("0 - Exit console")
#     print("1 - Search for a song")
#     user_input = int(input("Enter your choice: "))

#     if user_input == 1:
#         search_song = input("Enter song name: ")
#         search_artist = input("Enter artist name: ")
#         q = f'Track:{search_song} Artist:{search_artist}'
#         results = spotifyObject.search(q, type="track", limit=1)

#         songInfo = getSongInformation(results)
#         print(json.dumps(songInfo, sort_keys=True, indent=4))
#         webbrowser.open(songInfo['songUrl'])
        
#         # songs_dict = results['tracks']
#         # song_items = songs_dict['items']

#         # print(json.dumps(song_items, sort_keys=True, indent=4))
#         # print('Album: ' + song_items[0]['album']['name'])
#         # print('Song title: ' + song_items[0]['name'])
#         # print('Artist name: ' + song_items[0]['album']['artists'][0]['name'])

#         # song = song_items[0]['external_urls']['spotify']
#         # webbrowser.open(song)
#     elif user_input == 0:
#         print("Exiting console")
#         break
#     else:
#         print("Please enter a valid input")