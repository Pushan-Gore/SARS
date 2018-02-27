import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
    #Generic Twitter Class for sentiment analysis.
    def __init__(self):
        # Pushan Gore Twitte account//  Change these keys for different account
        consumer_key="sG4mFIbzlMH3gs3nWSTHyjpNN"
        consumer_secret="mG1kv6J6z3zTJeaQEl5T6qtm3av90D2adXneoKha5b2Wr5Z8ao"
        access_token="700610683033907200-1jCFP0qrFw4y8cuWrc5O6XBfVLgx5LS"
        access_token_secret="JkTv6cXq56hnkGjxwxlwplFB3ZKGx4afmilddKSemGj2F"

        # Try catch, statement to make an attempt at Auth
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) \
                                    |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
        tweets = []

        try:
            fetched_tweets = self.api.search(q = query, count = count)

            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))

def main():
    api = TwitterClient()

    # Query and number for tweets
    tweets = api.get_tweets(query = 'Padmavat', count = 200)

    # Need to check this, recode this ###SOMETHING IS WRONG HERE###
    if tweets == 0:
        print "Error Mining for tweets or query is beyond scope"
        abort()

    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

    print("Neutral tweets percentage: {} %".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
    main()
