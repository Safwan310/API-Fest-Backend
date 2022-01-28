import os
from flask import Flask,request,jsonify, json, Response, make_response, render_template
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
import tweepy
import re
from textblob import TextBlob
import matplotlib
matplotlib.use('agg')


#import jwt

app = Flask(__name__)
bcrypt = Bcrypt(app)

mongodb_client = PyMongo(app,uri=os.environ.get("MONGO_URI"))
db = mongodb_client.db

class SentimentAnalysis:
 

    def __init__(self):
        self.tweets = []
        self.tweetText = []
    
    def DownloadData(self, keyword, tweets):

        consumerKey = os.environ.get("api_key")
        consumerSecret = os.environ.get("api_key_secret")
        accessToken = os.environ.get("access_token")
        accessTokenSecret = os.environ.get("access_token_secret")
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
 
        tweets = int(tweets)

        self.tweets = tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(tweets)
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0

        for tweet in self.tweets:

            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))

            analysis = TextBlob(tweet.text)

            polarity += analysis.sentiment.polarity

            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1

        positive = self.percentage(positive, tweets)
        wpositive = self.percentage(wpositive, tweets)
        spositive = self.percentage(spositive, tweets)
        negative = self.percentage(negative, tweets)
        wnegative = self.percentage(wnegative, tweets)
        snegative = self.percentage(snegative, tweets)
        neutral = self.percentage(neutral, tweets)

        polarity = polarity / tweets
 
        if (polarity == 0):
            htmlpolarity = "Neutral"
        elif (polarity > 0 and polarity <= 0.3):
            htmlpolarity = "Weakly Positive"
        elif (polarity > 0.3 and polarity <= 0.6):
            htmlpolarity = "Positive"
        elif (polarity > 0.6 and polarity <= 1):
            htmlpolarity = "Strongly Positive"
        elif (polarity > -0.3 and polarity <= 0):
            htmlpolarity = "Weakly Negative"
        elif (polarity > -0.6 and polarity <= -0.3):
            htmlpolarity = "Negative"
        elif (polarity > -1 and polarity <= -0.6):
            htmlpolarity = "strongly Negative"
        

        return polarity, htmlpolarity, positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword, tweets

    def cleanTweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

@app.route("/", methods=['GET'])
def hello_world():
    return "Working"

@app.route("/login", methods=['POST'])
def login_user():
    try:
        if request.method == 'POST':
            form_data = request.get_json()
            email = form_data['email']
            password = form_data['password']
            if(email != '' and password != ''):
                data = list(db.users.find({'email': email}))
                if(len(data) == 0):
                    return Response(status=404, response=json.dumps({'message': 'user does not exist'}), mimetype='application/json')
                else:
                    data = data[0]
                    if(bcrypt.check_password_hash(data['password'], password)):
                        #token =jwt.encode({'email': email}, app.config['SECRET_KEY'])
                        return make_response(jsonify({'message':'User logged in successfully'}), 201)
                    else:
                        return Response(status=402, response=json.dumps({'message': 'Invalid password'}), mimetype='application/json')
            else:
                return Response(status=400, response=json.dumps({'message': 'Bad request'}), mimetype='application/json')
        else:
            return Response(status=401, response=json.dumps({'message': 'invalid request type'}), mimetype='application/json')
    except Exception as Ex:
        print('\n\n\n*********************************')
        print(Ex)
        print('*********************************\n\n\n')
        return Response(response=json.dumps({'message': "Internal Server error"}), status=500, mimetype="application/json")


@app.route("/register", methods=['POST'])
def register_user():
    try:
        if request.method == "POST":
            user_details = request.get_json()
            full_name = user_details["fullName"]
            email = user_details["email"]
            password = user_details["password"]
            password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
            if (full_name != '' and email != '' and password_hash != ''):
                db.users.insert_one({'fullName':full_name,'email':email,'password':password_hash})
                return Response(response=json.dumps({'message': 'User created successfully'}), status=200, mimetype="application/json")
            else:
                return Response(status=400, response=json.dumps({'message': 'Please enter your details'}), mimetype='application/json')
        else:
            return Response(status=400, response=json.dumps({'message': 'Bad request'}), mimetype='application/json')
    except Exception as Ex:
        print('\n\n\n*********************************')
        print(Ex)
        print('*********************************\n\n\n')
        return Response(response=json.dumps({'message': "Internal Server Error"}), status=500, mimetype="application/json")        

@app.route("/getSentiment",methods=["POST"])
def sentiment_analyzer():
    tweet_info = request.get_json()
    keyword = tweet_info["keyword"]
    tweets = tweet_info["tweets"]
    sa = SentimentAnalysis()
    polarity, htmlpolarity, positive, wpositive, spositive, negative, wnegative, snegative, neutral, keyword1, tweet1 = sa.DownloadData(keyword, tweets)
    analysis = {}
    analysis["polarity"] = polarity
    analysis["htmlpolarity"] = htmlpolarity
    analysis["wpositive"] = wpositive
    analysis["spositive"] = spositive
    analysis["negative"] = negative
    analysis["wnegative"] = wnegative
    analysis["snegative"] = polarity
    analysis["neutral"] = neutral
    analysis["keyword1"] = keyword1
    analysis["tweet1"] = polarity
    return jsonify(analysis)
    # content = request.json
    # tweets = tweet_fetcher(content["hashtag"])
    # tweet_obj = {}
    # tweet_obj["tweets"] = tweets
    # return jsonify(tweet_obj)

 

if __name__ == '__main__':
    app.run()

    