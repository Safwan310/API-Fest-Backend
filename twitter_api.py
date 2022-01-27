import tweepy
import configparser
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#authentication 
auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def tweet_fetcher(keyword):
    data = []
    limit = 300

    tweets = tweepy.Cursor(api.search_tweets, q=keyword,count=100,tweet_mode='extended').items(limit)

    for tweet in tweets:
        data.append(tweet.full_text)
    
    return data


# public_tweets = api.home_timeline()

# columns = ['Time','User','Tweet']
# data = []

# for tweet in public_tweets:
#     data.append([tweet.created_at,tweet.user.screen_name,tweet.text])

# df = pd.DataFrame(data,columns=columns)
# df.to_csv('tweets.csv')
# print(df)