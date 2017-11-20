# encoding: utf-8

import tweepy
import pickle
import string
import re
import time
import MySQLdb



# def createConnection():
#     db = MySQLdb.connect(host="localhost",
#                          user="root",
#                          passwd="12341234",
#                          db="video_recommendation")
#     cur = db.cursor()
#     return db, cur

# def executeQuery(query):
#     db, cur = createConnection()
#     res = cur.execute(query)
#     db.commit()
#     db.close()
#     return res

def constructURLStrings(stringlist):
    res = ""
    for s in stringlist:
        res += s + ","
    return res

consumer_key = "uRE8t5t6fWorWnRPMyekBAGDh"
consumer_secret = "EWTMKzEDYCUPPxcNp8XjYgEJB7s9MFaYHFT5c2wgiOWh0UU5En"
access_key = "779127824401793026-cfeMtPii7NXXJQt9HazxPzHjpbkm0Gt"
access_secret = "sM1QV9NN292I9UWzfqa5k1nJw8oJgI60E8UeWu2Q6LU7p"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


accept_letters=string.ascii_letters

# TODO: Replace all the print() statements with SQL queries to store the data
# TODO: Check that the user doesn't already exist in the DB before inserting

class MyStreamListener(tweepy.StreamListener):

    """
    Called whenever a new random tweet is found

    @param tweet: tweet object representation of the new tweet
    """
    def on_status(self, tweet):
        if tweet_contains_video(tweet):

            user_name = tweet.author.screen_name
            checkexist = "select username from tweets where username='" + user_name + "'"

            print("NAME: " + user_name)
            tweet_string = get_users_tweets_by_screen_name(user_name)
            print("TWEET33 " + tweet.text)
            print("TWEETS: " + tweet_string)

            # if executeQuery(checkexist) == 0:
            #     print("NAME: " + user_name)
            #     tweet_string, video_links = get_users_tweets_and_links(tweet)
            #     #print("TWEETS: " + tweet_string)
            #     #print("VIDEO_URLS: " + str(video_links))
            #     #  TODO: For loop through the video_links and add to database
            #     video_links_strings = constructURLStrings(video_links)
            #     querystr = "INSERT into tweets (username, tweets, urls) VALUES ('" + user_name + "', '" + tweet_string + "', '" + video_links_strings + "')"
            #     executeQuery(querystr)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_status disconnects the stream
            return False
"""
Checks if the tweet has a video media type

@param tweet: tweet object
@return: Boolean
"""
def tweet_contains_video(tweet):
    if (hasattr(tweet, 'extended_entities')):
        temptweet = tweet.extended_entities
        mediatype = temptweet['media'][0]['type']
        return mediatype == 'video'
    return False


"""
Gets the 200 most recent tweets from the user of the input tweet

@param tweet: tweet object of the person of interest
@return: tuple of (tweet_string,video_links),
where tweet_string is the 200 tweets put together as one string
and video_links is a List of strings of video URLS found within the 200 tweets
"""
def get_users_tweets_and_links(tweet):
    user_tweets = api.user_timeline(screen_name=tweet.author.screen_name,count=200)
    video_links = []
    for user_tweet in user_tweets:
        if tweet_contains_video(user_tweet):
            video_links.append(user_tweet.extended_entities['media'][0]['video_info']['variants'][0]['url'])
    user_tweets = [timeline_tweet.text for timeline_tweet in user_tweets]
    # add original tweet with the video + 200 of user's most recent tweet
    # into one string
    tweet_string = tweet.text + " " + " ".join(user_tweets)
    regex = re.compile('[^a-zA-Z @/.,#"]')
    fixed_tweet_string = regex.sub('', tweet_string)
    return (fixed_tweet_string,video_links)

def get_users_tweets_by_screen_name(screen_name):
    user_tweets = api.user_timeline(screen_name=screen_name,count=200)
    user_tweets = [timeline_tweet.text for timeline_tweet in user_tweets]
    video_links = []
    tweet_string = " ".join(user_tweets)
    regex = re.compile('[^a-zA-Z @/.,#"]')
    fixed_tweet_string = regex.sub('', tweet_string)
    return fixed_tweet_string





def search(interests,phrase="*"):
    # searchQuery looks like: "pepsi OR coke OR sprite -filter:retweets AND -filter:replies lang:en"
    phrasedInterests = ["\""+phrase.replace("*",interest)+"\"" for interest in interests]
    searchQuery = " OR ".join(phrasedInterests)
    searchQuery += "-filter:retweets AND -filter:replies lang:en" # filter retweets/replies, and english only
    #searchQuery = "coke -filter:retweets AND -filter:replies"
    maxTweets = 10000000  # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                obj_of_interest = ""
                for interest in interests:
                    if interest in tweet.text.replace(" ","").lower():
                        obj_of_interest = interest
                print (obj_of_interest + ": ",tweet.author.screen_name, tweet.text)
            tweetCount += len(new_tweets)
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break


"""
Returns List of video URLs from a list of the user's tweets
"""

"""
Start retrieving random sample of live tweets, and whenever a tweet is found, calls on_status
http://docs.tweepy.org/en/v3.5.0/streaming_how_to.html
"""
def stream_tweets():
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(api.auth, listener=myStreamListener)

    # myStream.sample() keeps getting random sample of live tweets
    # it calls on_status method of myStreamListner every time
    # a new tweet is found
    #myStream.sample(async=False, languages=["en"])

    # use myStream.filter() to get keyword searches for the 2nd part of the project
    #myStream.filter(track=interests, async=False, languages=["en"])

if __name__ == '__main__':
    interests = ["coke", "pepsi"]
    phrase = "i love *"
    search(interests,phrase)
    #stream_tweets()
