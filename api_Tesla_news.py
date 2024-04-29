import requests
import subprocess
import sys
import os
import time

# Set the API endpoint URL
api_url = "https://api.tickertick.com/feed?q=(and z:tsla (or s:bloomberg s:forbes s:axios s:barrons s:bbc s:ft s:cnbc s:cnn s:cnet s:economist s:marketwatch s:mckinsey s:nikkei s:seekingalpha s:techcrunch s:theverge s:nytimes s:nypost s:washingtonpost s:wsj s:theguardian s:abcnews s:apnews s:reuters s:wired s:benzinga s:zacks))&n=1"

# Set the initial value of history to None
history = None

# Load the last posted tweet content from the file
last_tweet_file = os.path.join(os.path.dirname(__file__), "last_tweet.txt")
if os.path.exists(last_tweet_file):
    with open(last_tweet_file, "r") as f:
        previous_tweet_text = f.read().strip()
else:
    previous_tweet_text = None

def check_and_post(id, title, link):
    global history, previous_tweet_text  # Use the global history and previous_tweet_text variables

    # Check if the id has changed
    if id != history:
        # Prepare the text to be sent to the Twitter API V2
        text = f"{title}\n{link}"

        # Check if the new tweet text is different from the previous one
        if text != previous_tweet_text:
            # Call the create_tweet.py script with the text as an argument
            script_path = os.path.join(os.path.dirname(__file__), "create_tweet.py")
            result = subprocess.run(["python", script_path, text], capture_output=True, text=True)

            if result.returncode == 0:
                history = id  # Update the history variable
                previous_tweet_text = text  # Update the previous_tweet_text variable

                # Save the new tweet content to the file
                last_tweet_file = os.path.join(os.path.dirname(__file__), "last_tweet.txt")
                with open(last_tweet_file, "w") as f:
                    f.write(text)

                print("Tweet posted successfully!")
                return True
            else:
                print(f"Error posting tweet: {result.stderr}")
        else:
            print("Tweet content is the same as the previous one. Skipping...")
    else:
        print("ID has not changed.")

    return False

def run_script():
    while True:
        # Fetch data from the API endpoint
        response = requests.get(api_url)
        data = response.json()

        # Extract the relevant information from the JSON data
        story = data["stories"][0]
        id = story["id"]
        title = story["title"]
        link = story["url"]

        # Call the check_and_post function
        check_and_post(id, title, link)

        # Wait for a specified amount of time before making the next request
        time.sleep(60)  # Wait for 1 minute

if __name__ == "__main__":
    run_script()