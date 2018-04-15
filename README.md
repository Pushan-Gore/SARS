# Twitter-Sentiment-Analysis

Gets tweets from Twitter, containing user-given keywords and performs a sentiment analysis 
Uses this sentiment and the keyword to provide movie recommendations from the data set

##  Usage
  1. Modify the 'sentiment_analysis.py' file to enter your access tokens.
  2. Train the data set using : 
    <code>python train.py</code>
     (This will create a pickle classifier file in ./data)
  3. To Run an example of sentiment analysis use: 
    <code>python sentiment_analysis.py KEYWORD</code>
  4. To Run an example of recommendation system use:
    <code>python movie_rec.py</code>
  5. To run the entire project along with GUI:
    <code>python ../"NAME OF DIRECTORY"</code>

