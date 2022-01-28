import os
from flask import Flask,request,jsonify
from twitter_api import tweet_fetcher 
from flask_pymongo import PyMongo

app = Flask(__name__)

mongodb_client = PyMongo(app,uri=os.environ.get("MONGO_URI"))
db = mongodb_client.db

@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/login")
def login_user():
    pass

@app.route("/register")
def register_user():
    user_details = request.json
    full_name = user_details["fullName"]
    email = user_details["email"]
    password = user_details["password"]
    response = {}
    try:
        db.users.insert_one({'fullName':full_name,'email':email,'password':password})
        response["message"] = "User created successfully"
        return jsonify(response),201
    except:
        response["message"] = "Internal server error"
        return  jsonify(response),500

@app.route("/getSentiment",methods=["POST"])
def sentiment_analyzer():
    content = request.json
    tweets = tweet_fetcher(content["hashtag"])
    tweet_obj = {}
    tweet_obj["tweets"] = tweets
    return jsonify(tweet_obj)

if __name__ == '__main__':
    app.run()