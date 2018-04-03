import re, math, collections, itertools, os, sys, json, pickle
import html_helper
import nltk
import nltk.classify.util
import nltk.metrics
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.metrics import precision, recall
from nltk.probability import FreqDist, ConditionalFreqDist
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob

CLASSIFIER_FILE = os.path.join('data', 'naive_bayes_classifier.pickle')

class TwitterClient(object):
    #Generic Twitter Class for sentiment analysis.
    def __init__(self):
        # Pushan Gore Twitter account// Change these keys for different account

        consumer_key="sG4mFIbzlMH3gs3nWSTHyjpNN"
        consumer_secret="mG1kv6J6z3zTJeaQEl5T6qtm3av90D2adXneoKha5b2Wr5Z8ao"
        access_token="700610683033907200-1jCFP0qrFw4y8cuWrc5O6XBfVLgx5LS"
        access_token_secret="JkTv6cXq56hnkGjxwxlwplFB3ZKGx4afmilddKSemGj2F"

        classifier_file = open(CLASSIFIER_FILE, 'r')

        #load the unpickle object into a variable
        self.classifier = pickle.load(classifier_file)
        self.html = html_helper.HTMLHelper()

        self.results = {}
        self.neut_count = [0] * 200
        self.pos_count = [0] * 200
        self.neg_count = [0] * 200

        # Try catch, statement to make an attempt at Auth
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

        print("Authentication Success")

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

            for i, tweet in enumerate(fetched_tweets):
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                words = re.findall(r"[\w']+|[.,!?;]", tweet.text.rstrip())
                parsed_tweet['sentiment'] = self.classifier.classify(dict([(word, True) for word in words]))
                #get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                if(parsed_tweet['sentiment'] == 'positive' or parsed_tweet['sentiment'] == 'pos'):
                    self.pos_count[i] += 1
                elif(parsed_tweet['sentiment'] == 'negative' or parsed_tweet['sentiment'] == 'neg'):
                    self.neg_count[i] += 1
                else:
                    self.neut_count[i] += 1
                #self.results[i] = {'text': parsed_tweet['text'], 'tweet': tweet , 'label': parsed_tweet['sentiment']}

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))

    def getHTML(self, keyword, results, time, pos_count, neg_count, neut_count):
        return self.html.getResultHTML(keyword, self.results, time, self.pos_count, \
                self.neg_count, self.neut_count)

def main():
    api = TwitterClient()

    #query_input = str(raw_input("Enter Query: "))
    query_input = str(sys.argv[1])

    # Query and number for tweets
    tweets = api.get_tweets(query = query_input, count = 200)

    # Need to check this, recode this ###SOMETHING IS WRONG HERE###
    if not tweets:
        print "Error Mining for tweets or query is beyond scope"
        exit()

    ptweets = [tweet for tweet in tweets if (tweet['sentiment'] == 'positive' or tweet['sentiment'] == 'pos')]
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

    ntweets = [tweet for tweet in tweets if (tweet['sentiment'] == 'negative' or tweet['sentiment'] == 'neg')]
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
