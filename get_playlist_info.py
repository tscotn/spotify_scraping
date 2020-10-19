#only problem with this is that by album, it cuts off at 50 tracks, so you'll lose some tracks on really long albums

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

client_id = '0c4083c7184e45d58daa3ebe3a71bfa6'
client_secret = 'e7e4ade9655a4095bd5ee0f7d81ca6d0'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

artist_name = 'talking heads'
artist_uri = 'spotify:artist:2x9SpqnPi8rlE9pjHBwmSC'

results = sp.artist_albums(artist_uri, album_type='album')
albums = results['items']
album_ids = []
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])
for album in albums:
    album_ids.append(album['id'])
    
#album_ids = ['6YSI6A71X8MOFqst8mMLh9', '6bVFYqSwHNl2lBX7mLlist', '6iOPhFscLxdpzGug0qxpcZ', '4fR8vS8yMLungmCG0Igw6m', '5PvkD4XryLL9oC4NFItYIM', '4LiLg6t10oOw8csXA1CQ0Y', '5Dja2ASXd7MOM628iwYdtA', '1ErneCyxOnZ1KTiEcNmnjw', '7IMqoztesjFDgyeibke8Jz', '4FR8Z6TvIsC56NLyNomNRE', '4sLCQxMRfn3gAHrBNZtbTH', '78MM8HrabEGPLVWaJkM2t1', '2WTDHjiVNCHY3ju9kmGNOY', '1JvXxLsm0PxlGH4LXzqMGq', '3AQgdwMNCiN7awXch5fAaG', '4OLsnJQPTX0S6lODXw1MqC', '5dVZpNJraoqCo3BssinMoo', '72IniHocIaJhIvZsIES0vq', '39jsLMRmrTpfdq2vE4TCUe', '5kMxEbEtS6a2jyzkqI5JGa', '01RJdKvXyz515O37itqMIJ', '0r7o2FeARRr23EZ0TJ0a8S', '5eqcF7pWzHgWpGdEmHgeSN']

#def getTrackIDs(user, playlist_id):
#    ids = []
#    playlist = sp.user_playlist(user, playlist_id)
#    for item in playlist['tracks']['items']:
#        track = item['track']
#        ids.append(track['id'])
#    return ids

#def getTrackIDs(user, playlist_id):
#    ids = []
#    playlist = sp.user_playlist(user, playlist_id)
#    for item in playlist['tracks']['items']:
#        track = item['track']
#        ids.append(track['id'])
#    return ids
    
track_ids = []
for id in album_ids:
    result = sp.album_tracks(id)
    print(len(result))
    print(result)
    for item in result['items']:
        track = item['id']
        track_ids.append(track)


#ids = getTrackIDs('scotnielson', '2AKgaM9kx33LBY69StGKjR')

#print(len(ids))

#this is to get more than 100 tracks
#def get_playlist_tracks(username,playlist_id):
#    results = sp.user_playlist_tracks(username,playlist_id)
#    tracks = results['items']
#    while results['next']:
#        results = sp.next(results)
#        tracks.extend(results['items'])
#
#    return tracks

###

def getTrackFeatures(id):
    meta = sp.track(id)
    features = sp.audio_features(id)
    
    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    
    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    
    track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    return track

tracks = []
for i in range(len(track_ids)):
  time.sleep(.5)
  track = getTrackFeatures(track_ids[i])
  tracks.append(track)

# create dataset
df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
df.to_csv(artist_name + ".csv", sep = ',')
