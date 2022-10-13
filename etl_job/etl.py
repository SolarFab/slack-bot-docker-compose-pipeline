"""
This code connects to the "twitter" MongoDB and runs the tweets 
through a sentiment analyzer.
At the end it puts the tweet and the result of the sentiment analyzer into a sql - DB
"""


import pymongo #package with tools to wirk with MongoDB
import time
from sqlalchemy import create_engine #package with tools to work with sql DB
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #package for sentiment analysis of text

analyser = SentimentIntensityAnalyzer()


# Establish a connection to the MongoDB server
client = pymongo.MongoClient(host="mymongodb", port=27017)

# Choose the "twitter" db which is created in get_tweets.py
db = client.twitter

time.sleep(2)  # seconds

# USER= "docker_user"
# PASSWORD = 1234
# DB = 'twitter'
# HOST = 'localhost'
# PORT = '5555'

# Assign the connection string 
conn_string = f'postgresql://docker_user:1234@postgresdb:5432/twitter'

#pg = create_engine('postgresql://user:password@host:5432/dbname', echo=True)

# create an engine to the above mentioned db
engine = create_engine(conn_string)
engine

# create a table named "tweets" with following columns
engine.execute('''
    CREATE TABLE tweets (
    date TIMESTAMP,
    text VARCHAR(500),
    compound NUMERIC,
    pos NUMERIC,
    neu NUMERIC,
    neg NUMERIC    
);
''')



# connects to the MongoDB "twitter" and finds the tweets
docs = db.tweets.find()

#loops the single tweets fo the docs object trough the sentiment analyzer
# and inserts the tweets and the reults into the postgres "tweets" db
for doc in docs:
    text = doc['text']
    compound = analyser.polarity_scores(text)['compound']
    pos = analyser.polarity_scores(text)['pos']
    neg = analyser.polarity_scores(text)['neg']
    neu = analyser.polarity_scores(text)['neu']
    date = doc['created_at']
    query = "INSERT INTO tweets VALUES (%s, %s, %s, %s, %s, %s);"
    engine.execute(query, (date, text, compound, pos, neu, neg ))
    print(doc)


