from twython import Twython
import json
import pandas as pd
from twython import TwythonStreamer
import string
# Load credentials from json file
with open("twitter_credentials.json", "r") as file:
    creds = json.load(file)

def syllable_count(word):
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
            if word.endswith("e"):
                count -= 1
    if count == 0:
        count += 1
    return count

def _removeNonAscii(s):
    return "".join(i for i in s if ord(i)<128)

def get_syllables(word, n):
    if word == None:
        return 0
    word = word.lower()
    _removeNonAscii(word)
    array = word.split()
    word = ""
    for i in array:
        if '@' not in i:
            if "http" not in i:
                word = word + ' ' + i
    word = word.replace('@', "")
    word = word.replace("rt", "")
    word = word.replace("\"","")
    word = word.strip()
    word = word.strip('"')
    count = 0
    array = word.split()
    word = ""
    for i in array:
        count = count + syllable_count(i)
        word = word + ' ' + i
        if count >= n-1:
            return word
    return 0

def process_tweet(tweet):
    global line1
    global line2
    global line3
    word = tweet
    if line1 != "" and line2 == "":
        n = 7
    else:
        n = 5
    syllables = get_syllables(word, n)
    if syllables != 0:
        if line1 == "" and n == 5:
            line1 = syllables
        elif line3 == "" and n == 5:
            line3 = syllables
        elif line2 == "" and n == 7:
            line2 = syllables
    return

def complete_haiku():
    if line1 != "" and line2 != "" and line3 != "":
        return True
    else:
        return False
# Create a class that inherits TwythonStreamer
class MyStreamer(TwythonStreamer):
    # Received data
    def on_success(self, data):
        # Only collect tweets in English
        if data['lang'] == 'en':
            tweet = data['text']
            tweet_data = process_tweet(tweet)
            if complete_haiku() == True:#if the haiku is finished, stop the tweet stream
                self.disconnect()

    # Problem with the API
    def on_error(self, status_code, data):
        print(status_code, data)
        self.disconnect()

# Instantiate from our streaming class
stream = MyStreamer(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'],
                    creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])

query = input("Please enter a theme: \n")

line1 = ""
line2 = ""
line3 = ""
# Start the stream
query = query.lower()
stream.statuses.filter(track=query)#this twitter stream will track tweets with the user query in them
print(line1)
print(line2)
print(line3)
