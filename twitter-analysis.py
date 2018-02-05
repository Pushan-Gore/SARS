from textblob import TextBlob
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import sqlite3 as lite
import datetime
import sys

consumer_key="sG4mFIbzlMH3gs3nWSTHyjpNN"
consumer_secret="mG1kv6J6z3zTJeaQEl5T6qtm3av90D2adXneoKha5b2Wr5Z8ao"
access_token="700610683033907200-1jCFP0qrFw4y8cuWrc5O6XBfVLgx5LS"
access_token_secret="JkTv6cXq56hnkGjxwxlwplFB3ZKGx4afmilddKSemGj2F"

class StdOutListener(StreamListener):
    con = lite.connect("data.db")
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Sentiment(polarity FLOAT,subjectivity FLOAT, time TEXT)")


    def on_data(self, data):
        try:
            tweet = json.loads(data,encoding="utf8")
            tweet_text = tweet["text"]
            x = TextBlob(tweet_text)
            if x.polarity == 0.0 and x.subjectivity == 0.0:
                pass
            else:
                pola = float(round(x.polarity,3))
                subj = float(round(x.subjectivity,3))
                print(x.sentiment)
                t = str(datetime.datetime.now().time())
                self.cur.execute("INSERT INTO Sentiment VALUES(?,?,?)", (pola,subj,t))
                self.con.commit()
        except:
           pass


        return True

    def on_error(self, status):
        print(status)





if __name__ == "__main__":
        print(" twitter-sentiment-analysis  Copyright (C) 2017  YassinS
        This program comes with ABSOLUTELY NO WARRANTY.
        This is free software, and you are welcome to redistribute it
        under certain conditions")
        print("Saving sentiment and time values in data.db")
        listener = StdOutListener()
        auth = OAuthHandler(consumer_key,consumer_secret)
        auth.set_access_token(access_token,access_token_secret)
        stream = Stream(auth,listener)

        stream.filter(track=sys.argv[1:])

