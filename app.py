from flask import Flask,request,jsonify
from twitter_api import tweet_fetcher 

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/getSentiment",methods=["POST"])
def sentiment_analyzer():
    content = request.json
    tweets = tweet_fetcher(content["hashtag"])
    tweet_obj = {}
    tweet_obj["tweets"] = tweets
    return jsonify(tweet_obj)

if __name__ == '__main__':
    app.run()