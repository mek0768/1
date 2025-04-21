from flask import Flask, request, jsonify
from requests_oauthlib import OAuth1
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = OAuth1(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

@app.route('/tweet-reply', methods=['POST'])
def tweet_reply():
    data = request.json
    tweet_id = data.get('tweet_id')
    text = data.get('text')

    if not tweet_id or not text:
        return jsonify({"error": "tweet_id and text required"}), 400

    payload = {
        "text": text,
        "reply": {
            "in_reply_to_tweet_id": tweet_id
        }
    }

    response = requests.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
        auth=auth
    )

    if response.status_code == 201:
        return jsonify({"status": "success", "response": response.json()}), 201
    else:
        return jsonify({"status": "error", "response": response.json()}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
