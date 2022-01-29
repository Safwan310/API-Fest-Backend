# API-Fest-Backend
- [Frontend repository](https://github.com/HimikaP/Team-Jalebi-Fafda)
- [Deployed frontend]()

### API Link
- https://sentimental-analysis33.herokuapp.com
### Available Endpoints
- /getSentiment
  - Returns the public sentiment over an event/topic by parsing tweets on that hashtag/keyword
  - Request body: 
  ```js
  {
  "keyword": "#APIFest2022",
  "tweets": 100
  }
  ```
  - Response: 
  ```js
  {
   "final_sentiment": "Positive",
   "negative": 7,
   "neutral": 30,
   "positive": 63
  }
  ```
- /getTweets
  - Returns an array of tweets for the requested hashtag/keyword which can then be downloaded
  - Request body: 
  ```js
  {
  "keyword": "#APIFest2022",
  "tweets": 100
  }
  ```
  - Response:
  ```js
  {
   "tweets": [
    "Thie event was so cool",
    "Participating in this event was rewarding",
    "Learnt a lot from this event"
   ]
  }
  ```
  
