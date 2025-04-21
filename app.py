from flask import Flask, request, jsonify
import os
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

@app.route("/")
def home():
    return "API is running. Use POST /tweet-reply to send a reply."

@app.route("/tweet-reply", methods=["POST"])
def tweet_reply():
    data = request.json
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

    auth = HTTPBasicAuth(
        os.environ.get("API_KEY"),
        os.environ.get("API_KEY_SECRET")
    )

    try:
        response = requests.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
            auth=auth
        )
        return jsonify({"status": response.status_code, "result": response.json()}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ BU KISIM ÇOK ÖNEMLİ:
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
