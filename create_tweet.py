from requests_oauthlib import OAuth1Session
import sys
import json

# Replace these with your own credentials
consumer_key = "rCZdEWmTWmJcOXdJ7u1ZgKfUD"
consumer_secret = "A0P5BBL5QVLDfY28U5zIuYpzSK2TL4RQfFQIVoXg5qpfbqmHR3"
access_token = "1784564201627009024-QYkKJQas0NvDl4ZbF7YOiQ4cQ5oRat"
access_token_secret = "ECis4teMQ0tUaIcOiC1IXB1D1CcmIHy6GSNsaaqmdFnlX"

# Get the tweet text from the command-line argument
if len(sys.argv) > 1:
    tweet_text = sys.argv[1]
else:
    print("Error: Tweet text not provided.")
    sys.exit(1)

payload = {"text": tweet_text}

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Making the request
response = oauth.post(
    "https://api.twitter.com/2/tweets",
    json=payload,
)

if response.status_code != 201:
    raise Exception(
        "Request returned an error: {} {}".format(response.status_code, response.text)
    )

print("Response code: {}".format(response.status_code))

# Saving the response as JSON
json_response = response.json()
print(json.dumps(json_response, indent=4, sort_keys=True))