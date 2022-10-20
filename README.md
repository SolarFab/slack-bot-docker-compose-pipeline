# slackbot_docker_etl_pipeline

The goal of this project is to build a data pipeline that connects to the twitter API and collects tweets, stores those in a MongoDB database, analyzes the sentiments of the tweets and stores thosein a PostgreSQL data base. Finally the tweets with the best and worse sentiment is published on slack every given time.

![image](https://user-images.githubusercontent.com/101807190/196934947-3de4a828-40de-4910-87aa-b8e3b56665e3.png)

This program uses the following packages:

- pymongo
- sqlalchemy
- vaderSentiment
- tweepy
- panda, requests, time etc.
