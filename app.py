from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth1

load_dotenv()

app = Flask(__name__)

CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

@app.route("/")
def home():
    return "✅ API is running. Use POST /tweet-reply to send a reply."

@app.route("/tweet-reply", methods=["POST"])
def tweet_reply():
    data = request.get_json()
    tweet_id = data.get("tweet_id")
    text = data.get("text")

    if not tweet_id or not text:
        return jsonify({"error": "Missing tweet_id or text"}), 400

    payload = {
        "text": text,
        "reply": {
            "in_reply_to_tweet_id": tweet_id
        }
    }

    try:
        response = requests.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
            auth=auth
        )
        return jsonify({"status": response.status_code, "result": response.json()}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
