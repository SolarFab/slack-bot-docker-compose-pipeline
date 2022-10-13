"""
This code does connect to the Twitter API via the tweepy package and 
downloads related tweets to Elon Musk. 
Tweets are then inserted into a MongoDB db.
"""

import tweepy # tools to work with twitter in python
import pymongo # tools to work with MongoDB
import os 


##################
# Authentication #
##################
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
)

########################
# Get User Information #
########################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_user
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user

response = client.get_user(
    username='elonmusk',
    user_fields=['created_at', 'description', 'location',
                 'public_metrics', 'profile_image_url']
)

user = response.data


#####################
# Search for Tweets #
#####################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.search_recent_tweets
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

# define search query 
search_query = "elon musk -is:retweet -is:reply -is:quote lang:en -has:links"

# search for tweets and save in Paginator() obejct
cursor = tweepy.Paginator(
    method=client.search_recent_tweets,
    query=search_query,
    tweet_fields=['author_id', 'created_at', 'public_metrics'],
).flatten(limit=100000)


#####################
# Create MongoDB and insert tweets #
#####################

### Creates a MongoDB database with name twitter
client = pymongo.MongoClient(host="mymongodb", port = 27017)
db = client.twitter

### Adds the tweets of the cursor object into the MongoDB "Twitter" as dict.
for tweet in cursor:

    db.tweets.insert_one(dict(tweet))
### end for mongoDB
