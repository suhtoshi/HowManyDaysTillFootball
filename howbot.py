import tweepy
import datetime
import time

#this is the required keys for the developer twitter account that connects it to the bot account
consumer_key = 'insert yours here'
consumer_secret = 'insert yours here'
key = 'insert yours here'
secret = 'insert yours here'

#twitter auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)
file_name = 'last_seen.txt'

#variables created to calculate number of days until the season starts
NFL = (datetime.datetime(2020, 9, 10, 19, 20) - datetime.datetime.today()).days
NCAA = (datetime.datetime(2020, 8, 29, 19, 20) - datetime.datetime.today()).days

#defining a function that reads the last seen twitter id associated with response from mentions timeline
def read_last_seen(file_name):
    file_read = open(file_name, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

#defining a function that stores the last seen twitter id it responded to from mentions timeline
def store_last_seen(file_name, last_seen_id):
    file_write = open(file_name, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()
    return


def reply():
    #tweets variable that includes the list of mentions starting at the last stored id in file file_name
    tweets = api.mentions_timeline(read_last_seen(file_name), tweet_mode='extended')
    #tweets are typically returned in reverse order(newest at bottom), so i reversed 
    for tweet in reversed(tweets):
        #if this hashtag is in the tweet in "tweets". i converted to lowercase to make the tweet and hashtag non-capital required
        if '#howmanydaysnfl' in tweet.full_text.lower():
            #prints the tweet id in a string and adds the full text of the tweet
            print(str(tweet.id) + ' - ' + tweet.full_text)
            #updates bot status to include the user screen name + a string of the number of days
            api.update_status("@" + tweet.user.screen_name + " " + str(NFL) + " days until the 2020 NFL season!", tweet.id)
            #favorites the tweet of the user tweet id
            api.create_favorite(tweet.id)
            #stores the last user tweet id to know next time where to start
            store_last_seen(file_name, tweet.id)
    #same for NCAA
    for tweet in reversed(tweets):
        if '#howmanydaysncaa' in tweet.full_text.lower():
            print(str(tweet.id) + ' - ' + tweet.full_text)
            api.update_status("@" + tweet.user.screen_name + " " + str(NCAA) + " days until the 2020 NCAA Football season!", tweet.id)
            api.create_favorite(tweet.id)
            store_last_seen(file_name, tweet.id)

#created a loop to re-run every 12 seconds
while True:
    reply()
    time.sleep(12)
