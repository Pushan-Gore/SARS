import re, math, collections, itertools, os, sys
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

POLARITY_DATA_DIR = os.path.join('polarityData', 'rt-polaritydata')
RT_POLARITY_POS_FILE = os.path.join(POLARITY_DATA_DIR, 'rt-polarity-pos.txt')
RT_POLARITY_NEG_FILE = os.path.join(POLARITY_DATA_DIR, 'rt-polarity-neg.txt')

#this function takes a feature selection mechanism and returns its performance in a variety of metrics
def evaluate_features():
    posFeatures = []
    negFeatures = []

    #breaks up the sentences into lists of individual words (as selected by the input mechanism) and appends 'pos' or 'neg' after each list
    train_pos = []
    train_neg = []
    with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
        for i in posSentences:
            train_pos.append((i, 'pos'))

        all_words = set(word.lower() for passage in train_pos for word in word_tokenize(passage[0]))
        print "Extracted all positive words..."
        posFeatures = [[{word: (word in word_tokenize(x[0])) for word in all_words}, x[1]] for x in train_pos]
        print "Prepared positive word feature set..."
    with open(RT_POLARITY_NEG_FILE, 'r') as negSentences:
        for i in negSentences:
            train_neg.append((i, 'neg'))

        all_words = set(word.lower() for passage in train_neg for word in word_tokenize(passage[0]))
        print "Extracted all negative words..."
        negFeatures = [[{word: (word in word_tokenize(x[0])) for word in all_words}, x[1]] for x in train_neg]
        print "Prepared negative word feature set..."

    trainFeatures = posFeatures[:] + negFeatures[:]

    #trains a Naive Bayes Classifier
    classifier = NaiveBayesClassifier.train(trainFeatures)

    #prints metrics to show how well the feature selection did
    classifier.show_most_informative_features(10)
    return classifier

class TwitterClient(object):
    #Generic Twitter Class for sentiment analysis.
    def __init__(self):
        # Pushan Gore Twitter account// Change these keys for different account
        consumer_key="sG4mFIbzlMH3gs3nWSTHyjpNN"
        consumer_secret="mG1kv6J6z3zTJeaQEl5T6qtm3av90D2adXneoKha5b2Wr5Z8ao"
        access_token="700610683033907200-1jCFP0qrFw4y8cuWrc5O6XBfVLgx5LS"
        access_token_secret="JkTv6cXq56hnkGjxwxlwplFB3ZKGx4afmilddKSemGj2F"

        self.classifier = evaluate_features()
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
                words = re.findall(r"[\w']+|[.,!?;]", tweet.text.rstrip())
                parsed_tweet['sentiment'] = self.classifier.classify(dict([(word, True) for word in words]))
                #get_tweet_sentiment(tweet.text)

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

    #query_input = str(raw_input("Enter Query: "))
    query_input = str(sys.argv[1])

    # Query and number for tweets
    tweets = api.get_tweets(query = query_input, count = 200)

    # Need to check this, recode this ###SOMETHING IS WRONG HERE###
    if tweets == 0:
        print "Error Mining for tweets or query is beyond scope"
        abort()

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
