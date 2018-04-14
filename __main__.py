import json, web, html_helper, logging
import sentiment_analysis
import movie_reco

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        query = web.ctx.get('query')
        html = html_helper.HTMLHelper()
        #twitterData = get_twitter_data.TwitterData()
        if query:
            print "Query returned"
            if(query[0] == '?'):
                query = query[1:]
            arr = query.split('&')
            logging.warning(arr)

            #default values

            for item in arr:
                if 'keyword' in item:
                    keyword = item.split('=')[1]

            print "Query is " + str(keyword)
            #reco_system = movie_reco.RecoSystem()
            recommendations = movie_reco.show_recommendations(keyword)
            print recommendations

            twitter_api = sentiment_analysis.TwitterClient()
            tweets = twitter_api.get_tweets(keyword, 200)
            if(tweets):
                results = recommendations
                ptweets = [tweet for tweet in tweets if (tweet['sentiment'] == 'positive' or tweet['sentiment'] == 'pos')]
                ntweets = [tweet for tweet in tweets if (tweet['sentiment'] == 'negative' or tweet['sentiment'] == 'neg')]
                neut_count = 100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)
                twitter_api.get_frequency_list()
                return twitter_api.getHTML(keyword, results, len(ptweets), len(ntweets), neut_count, tweets, twitter_api.frequency_list)
        else:
            return html.getDefaultHTML()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
