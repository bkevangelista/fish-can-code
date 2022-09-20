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
    
    #Return dictionary of an array of playlists categorized by username
    return {"username": username, "playlists": allPlaylists}

#Very slow to go through all liked songs
def getSongsFromPlaylist(spotifyObject, playlistID):
    allTracks = []
    results = spotifyObject.playlist_tracks(playlist_id=playlistID)
    tracks = results['items']

    while results['next']:
        #Go to the next set of songs
        results = spotifyObject.next(results)
        tracks.extend(results['items'])
    
    for idx, item in enumerate(tracks):
        track = item['track']
        allArtists = []
        for artist in track['artists']:
            allArtists.append(artist['name'])

        trackInfo = {
            "songTitle": str(track['name']),
            "artists": allArtists,
            "album": str(track['album']['name'])
        }
        allTracks.append(trackInfo)
    return allTracks
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
def initializeSpotifyConnection():
    config_object = ConfigParser()
    config_object.read('src/secrets.ini')
    spotifyCredentials = config_object["SPOTIFY"]
    clientID = spotifyCredentials["CLIENT_ID"]
    clientSecret = spotifyCredentials["CLIENT_SECRET"]
    uri = spotifyCredentials["URI"]

    return spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth
                                    (client_id=clientID,
                                    client_secret=clientSecret,
                                    redirect_uri=uri,
                                    scope="user-library-read playlist-read-private app-remote-control playlist-modify-public"))

def main():
    sp = initializeSpotifyConnection()
    username = sp.me()['id']

    allPlaylists = []
    allPlaylists.append(listAllPlaylists(sp, username))
    allPlaylists.append(listAllPlaylists(sp, '12155045153')) #this is James
    allPlaylists.append(listAllPlaylists(sp, 'kate.sm'))
    allPlaylists.append(listAllPlaylists(sp, 'saxguitarguy'))
    allPlaylists.append(listAllPlaylists(sp, '22ag7odizaakrf6vgghlut6ni')) #this is Mel
    allPlaylists.append(listAllPlaylists(sp, 'galamares12'))

    # print(json.dumps(allPlaylists, indent=4))

    tracks = getSongsFromPlaylist(sp, allPlaylists[0]['playlists'][0]["playlistID"])
    print(len(tracks))
    print(json.dumps(tracks, sort_keys=True, indent=4))

    # tracks = getSongsFromPlaylist(sp, 5, 0, allPlaylists[0]['playlists'][0]["playlistID"])
    # print(json.dumps(tracks, indent=4))

if __name__ == '__main__':
    main()