# encoding: utf-8

import tweepy
import pickle
import string
import re

consumer_key = "uRE8t5t6fWorWnRPMyekBAGDh"
consumer_secret = "EWTMKzEDYCUPPxcNp8XjYgEJB7s9MFaYHFT5c2wgiOWh0UU5En"
access_key = "779127824401793026-cfeMtPii7NXXJQt9HazxPzHjpbkm0Gt"
access_secret = "sM1QV9NN292I9UWzfqa5k1nJw8oJgI60E8UeWu2Q6LU7p"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

accept_letters=string.ascii_letters

def get_all_tweets(screen_name):
    alltweets = []
    tweetstring=""
    counter = 0
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1


    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1

    for tweet in alltweets:
        if (hasattr(tweet,'extended_entities')):
            temptweet=tweet.extended_entities
            mediatype=temptweet['media'][0]['type']
            if mediatype=='video':
                tempvids.append(temptweet['media'][0]['video_info']['variants'][0]['url'])

        tweetstring+=tweet.text
        counter += 1
    print(screen_name,counter)

    regex = re.compile('[^a-zA-Z @/.,#"]')
    fixedstring=regex.sub('', tweetstring)

    return fixedstring


if __name__ == '__main__':
    userlist=["BernieSanders","BarackObama","HillaryClinton", "KingJames"
        ,"CNN","rihanna","billgates", "facebook","CallofDuty","realDonaldTrump"]
    testlist=["realDonaldTrump"]

    usertweets=[]
    testtweets=[]

    videolists=[]
    temptweets=[]
    tempvids=[]
    testtweets.append(get_all_tweets(testlist[0]))

    for i in userlist:
        temptweets=[]
        tempvids=[]
        usertweets.append(get_all_tweets(i))
        videolists.append(tempvids)


print(videolists)

with open('all_tweets.txt', 'wb') as f:
    pickle.dump(usertweets, f)

with open('userlist.txt', 'wb') as f:
    pickle.dump(userlist, f)

with open('queryname.txt', 'wb') as f:
    pickle.dump(testlist, f)

with open('testlist.txt', 'wb') as f:
    pickle.dump(testtweets, f)

with open('tempvids.txt', 'wb') as f:
    pickle.dump(videolists, f)
