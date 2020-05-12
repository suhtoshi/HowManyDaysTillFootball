import tweepy
import datetime
import time

consumer_key = 'insert yours here'
consumer_secret = 'insert yours here'
key = 'insert yours here'
secret = 'insert yours here'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)
file_name = 'last_seen.txt'


NFL = (datetime.datetime(2020, 9, 10, 19, 20) - datetime.datetime.today()).days
NCAA = (datetime.datetime(2020, 8, 29, 19, 20) - datetime.datetime.today()).days


def read_last_seen(file_name):
    file_read = open(file_name, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id


def store_last_seen(file_name, last_seen_id):
    file_write = open(file_name, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return


def reply():
    tweets = api.mentions_timeline(read_last_seen(file_name), tweet_mode='extended')
    for tweet in reversed(tweets):
        if '#howmanydaysnfl' in tweet.full_text.lower():
            print(str(tweet.id) + ' - ' + tweet.full_text)
            api.update_status("@" + tweet.user.screen_name + " " + str(NFL) + " days until the 2020 NFL season!", tweet.id)
            api.create_favorite(tweet.id)
            store_last_seen(file_name, tweet.id)
    for tweet in reversed(tweets):
        if '#howmanydaysncaa' in tweet.full_text.lower():
            print(str(tweet.id) + ' - ' + tweet.full_text)
            api.update_status("@" + tweet.user.screen_name + " " + str(NCAA) + " days until the 2020 NCAA Football season!", tweet.id)
            api.create_favorite(tweet.id)
            store_last_seen(file_name, tweet.id)


while True:
    reply()
    time.sleep(12)
