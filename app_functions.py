# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 18:49:38 2015
@author: Barbora Doslikova
"""

import simplejson
import requests
import unicodedata
from requests_oauthlib import OAuth1


"""1. MATCH BOUNDING BOX
"""
def pick_bounding_boxes(my_list):
    """Takes a list of 1-3 locations as strings based on user's previous choice and
    returns a list of 1-3 bounding boxes for those 1-3 locations as strings.
    """
    bounding_boxes = []
    for item in my_list:
        if item == "WestUSA":
            bounding_box_WestUSA = "-125.00,24.94,-95.50,49.59"  # W, S, E, N
            bounding_boxes.append(bounding_box_WestUSA)                
        elif item == "EastUSA":
            bounding_box_EastUSA = "-95.50,24.94,-66.93,49.59"  # W, S, E, N
            bounding_boxes.append(bounding_box_EastUSA) 
        elif item == "Canada":
            bounding_box_Canada = "-125.00,49.59,-66.93,69.94"  # W, S, E, N
            bounding_boxes.append(bounding_box_Canada)
        else:
            bounding_box_Default = "-125.00,49.59,-66.93,69.94"  # W, S, E, N
            bounding_boxes.append(bounding_box_Default)
    return bounding_boxes


"""2. GENERATE TWEETS
"""
fh = open("twitter_secrets.json.nogit.txt")
string = fh.read()  # file.read() returns one big string
secrets = simplejson.loads(string)  # Deserialises a string into a python object
    
auth = OAuth1(
    secrets["api_key"],
    secrets["api_secret"],
    secrets["access_token"],
    secrets["access_token_secret"]
)

   
def tweet_generator(my_list):
    """Generates tweets in lowercase ascii with no weird characters.
    """
    bounding_box = pick_bounding_boxes(my_list)
        
    stream = requests.post("https://stream.twitter.com/1.1/statuses/filter.json?track=weed,marihuana&language=en",
                     auth=auth,
                     stream=True,
                     data={"locations" : bounding_box})
    
    for line in stream.iter_lines():
        try:
            if not line:  # Filter out keep-alive new lines
                continue
            tweet = simplejson.loads(line)
            if "text" in tweet:
                convert = tweet["text"]
                k = unicodedata.normalize('NFKD', convert).encode('ascii', 'ignore').strip().lower()
                yield k
        except:
            pass
            
"""3. COUNT MATCHES
"""
WORDS_TO_COUNT = ["weed", "stoned", "stoner", "stoners", "marihuana", "marijuana", "cannabis", "pot", "bong",
                 "#weed", "#stoned", "#stoner", "#stoners", "#marihuana", "#marijuana","#cannabis", "#pot", "#bong"]      
   
def tokenize(list):
    """Takes a list of sentences/tweets/strings and
    returns a list of words/tokens/strings.
    """ 
    pre_words = []
    words = []   
    
    def sentences_to_words(list):
        for item in list:
            item = item.split(" ")
            pre_words.append(item)

    def append_words(list):
        for item in pre_words:
            for it in item:
                words.append(it)
                
    sentences_to_words(list) 
    append_words(list)            
    return words
    
def count_matches(list):
    """Takes a list of strings to be tokenized,
    compares tokens with a list of words to count and
    returns a number of times the words to count appeared among the tokens.
    """
    tokens = tokenize(list)    
    search_in = WORDS_TO_COUNT
    count = 0
    
    for word in search_in:
        for token in tokens:
            if (word == token):
                count = count + 1
    return count
