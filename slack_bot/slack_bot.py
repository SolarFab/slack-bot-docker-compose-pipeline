"""
This code connects to the "twitter"-postgres-db and finds the tweets with
the best/worse scored by the sentiment analyzer.
Then connect to a slack channel and posts every fifteen seconds a new best/worse tweet.
"""

import pandas as pd
from sqlalchemy import create_engine
import requests
import time
import os

time.sleep(15) 
# create an engine and connect to the postgres db "twitter"
pg = create_engine('postgresql://docker_user:1234@postgresdb:5432/twitter', echo=True)

# Create a Webhook object to connect to SLACK
webhook_url = os.getenv('Slack_Hook')


# The query to get the worse score tweet
query_worst = f"""
    SELECT text, compound
    FROM tweets
    ORDER BY compound LIMIT 1
    """
# The query to get the best score tweet 
query_best = f"""
    SELECT text, compound
    FROM tweets
    ORDER BY compound DESC LIMIT 1
    """


while True:
    time.sleep(10)
    # reading query and write to variable with pandas:
    tweet_worst = pd.read_sql_query(query_worst, con=pg)
    tweet_best = pd.read_sql_query(query_best, con=pg)



    # get value of text and sentiment
    text_tweet_best = tweet_best['text'].iloc[0]
    sentiment_tweet_best =  tweet_best['compound'].iloc[0]
        
    text_tweet_worst = tweet_worst['text'].iloc[0]
    sentiment_tweet_worst =  tweet_worst['compound'].iloc[0]
    
    # Create the JSON data object
    data = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*The Best Tweet Received*\n:+1: With a Score of {sentiment_tweet_best}\n{text_tweet_best}"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*The Worst Tweet Received*\n:-1: With a Score of {sentiment_tweet_worst}\n{text_tweet_worst}"
                }
            }
        ]
    }
    # Post the data to the Slack
    requests.post(url=webhook_url, json = data)

