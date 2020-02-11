# twitter_poet

twitter_poet is a python program which uses TwythonStreamer to generate a stream of tweets from the Twitter Search API relating to a key term entered by the user. The program then parses these tweets to create Haikus (one verse poems with 3 lines of the form 5 syllables- 7 syllables- 5 syllables).

This program is configured to use the twitter API keys associated with your Twitter developper account stored in 'twitter_credentials.json'. For obvious reasons, I have not made my Twitter API keys available on this public repo, so this program will not work properly unless you replace the dummy values currently in the JSON file with your own API keys.
