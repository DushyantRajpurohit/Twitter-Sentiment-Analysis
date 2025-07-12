import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import time

class TwitterClient(object):
    #Generic Twitter Class for sentiment analysis.
    def __init__(self):
        #Class constructor or initialization method.

        #Bearer Token from the X Developer Portal.
        self.bearer_token='AAAAAAAAAAAAAAAAAAAAALnr2wEAAAAArr3aARAxQ7zQwEovdBWA1mKWJk0%3DfgqvQYygGbsevxkgeMfuhBJ53N9yz2aWcFymOZmzCGzGGIOcuS'
        self.client=tweepy.Client(bearer_token=self.bearer_token)

    def clean_tweet(self, tweet):
        #Removing links, special characters using simple regex statements.
        return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",tweet).split())

    def get_tweet_sentiment(self, tweet):
        #Utility function to classify sentiment of passes tweet using textblob's sentiment method.

        #Create TextBlob object of passed tweet text.
        analysis=TextBlob(self.clean_tweet(tweet))

        #Set sentiment.
        if analysis.sentiment.polarity>0:
            return 'positive'
        elif analysis.sentiment.polarity==0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        #Main function to fetch tweets.

        #Empty list to store parsed tweets.
        tweets=[]

        try:
            #Fetch tweets.
            time.sleep(2)
            response=self.client.search_recent_tweets(query, max_results=min(count, 100), tweet_fields=['text'])

            #Parsing tweets in one by one.
            if response.data:
                for tweet in  response.data:
                    #Empty dictionary to store required params of a tweet.
                    parsed_tweet={
                        'text':tweet.text,
                        'sentiment':self.get_tweet_sentiment(tweet.text)
                    }
                    tweets.append(parsed_tweet)
            return tweets

        except tweepy.TooManyRequests as e:
            print('Rate limit hit. Try again later.')
            return []

        except tweepy.TweepyException as e:
            #Print error(if any).
            print("Error:"+str(e))
            return []

def main():
    #Creating object of TwitterClient Class.
    api=TwitterClient()
    #Calling function to get tweets.
    tweets=api.get_tweets(query='Donald Trump', count=20)

    if not tweets:
        print('No tweets fetched.')
        return

    #Picking positive tweets from tweets.
    ptweets=[tweet for tweet in tweets if tweet['sentiment']=='positive']

    #Picking negative tweets from tweets.
    ntweets=[tweet for tweet in tweets if tweet['sentiment']=='negative']

    #Percentage of positive tweets.
    print("Positive Tweets Percentage: {}".format(100*len(ptweets)/len(tweets)))

    #Percentage of negative tweets.
    print("Negative Tweets Percentage: {}".format(100*len(ntweets)/len(tweets)))

    #Percentage of neutral tweets.
    print("Neutral Tweets Percentage: {}".format(100*(len(tweets)-(len(ptweets)+len(ntweets)))/len(tweets)))

    #Printing first 5 positive tweets.
    print("\n\nPositive Tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # Printing first 5 positive tweets.
    print("\n\nNegative Tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

if __name__=="__main__":
    #Calling main function.
    main()


