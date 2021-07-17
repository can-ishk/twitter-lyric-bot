import tweepy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import time
from lyrics_extractor import SongLyrics


fileName = 'lastSeen.txt'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))
extract_lyrics = SongLyrics(google_search_api_key, custom_search_engine_id)



def read_last_seen():
    file = open(fileName, 'r')
    lastSeenId = int(file.read().strip())
    file.close()
    return lastSeenId


def write_last_seen(lastSeenId):
    file = open(fileName, 'w')
    file.write(str(lastSeenId))
    file.close()
    return


class tweetInfo:
    def __init__(self, tweeid, twlink):
        self.tweetId = tweeid
        self.playlistId = twlink


# //TWITTER AUTHENTICATION AHEAD//


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)  # OAUTH

while True:
    tweets = api.mentions_timeline(read_last_seen(), tweet_mode="extended", include_entities=True)
    # print(tweets[0].id)
    links = []
    #  GETTING LINKS AND TWEET IDs
    for tweet in tweets:
        if tweet.entities['urls']:
            a_string = tweet.entities['urls'][0]['expanded_url'].split('https://open.spotify.com/playlist/', 1)[1]
            split = []
            n = 22
            for index in range(0, len(a_string), n):
                split.append(a_string[index: index + n])
            links.append(tweetInfo(tweet.id, split[0]))

    last_id: str = ' '

    # GETTING PLAYLISTS
    if links:
        for link in links:
            print(str(link.tweetId) + ' - ' + link.playlistId)
            playlist = sp.playlist_items(link.playlistId, fields='items.track.name,items.track.artists.name')
            # print(playlist)
            songNum = random.randint(0, len(playlist['items']))
            string = extract_lyrics.get_lyrics(
                playlist['items'][songNum]['track']['artists'][0]['name'] + playlist['items'][songNum]['track'][
                    'name'])['lyrics']
            randomLyric = random.randint(0, len(string.split('\n')) - 3)
            print(string.split('\n')[randomLyric])

            while not string.split('\n')[randomLyric][0]:
                randomLyric = random.randint(0, len(string.split('\n')))

            while string.split('\n')[randomLyric][0] == '[':
                randomLyric = random.randint(0, len(string.split('\n')))

            print(string.split('\n')[randomLyric])
            api.update_status(
                status=string.split('\n')[randomLyric] + '\n' + 'https://twitter.com/twitter/statuses/' + str(
                    link.tweetId), in_reply_to_status_id=int(link.tweetId))
    write_last_seen(tweets[0].id)
    time.sleep(5)
