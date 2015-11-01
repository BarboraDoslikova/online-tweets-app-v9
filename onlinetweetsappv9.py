# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:30:08 2015

@author: BD

The main script to run the Online Tweets App (OTA).
"""

from flask import Flask, render_template, request, redirect
onlinetweetsappv9 = Flask(__name__)

import simplejson
import requests
from requests_oauthlib import OAuth1
from itertools import islice

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

onlinetweetsappv9.vars = {}

onlinetweetsappv9.regions = {}
onlinetweetsappv9.regions['Which region would you like to select?']=('West USA','East USA')

@onlinetweetsappv9.route('/main', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        a1, a2 = onlinetweetsappv9.regions.values()[0]
        return render_template('form.html', ans1=a1, ans2=a2)
    else:
        # request was a POST
        onlinetweetsappv9.vars['region'] = request.form['answer_from_layout']     
        return redirect('/graph')

@onlinetweetsappv9.route('/graph', methods=['GET', 'POST'])
def graph():    
    """AUTHENTICATION
    """
    fh = open("twitter_secrets.json.nogit.txt")
    string = fh.read() #file.read() returns one big string
    secrets = simplejson.loads(string) #deserialises a string into a python object
    
    auth = OAuth1(
        secrets["api_key"],
        secrets["api_secret"],
        secrets["access_token"],
        secrets["access_token_secret"]
    )
    
    """GENERATE TWEETS
    """
    def pick_location():
        ''' returns a location based on user's choice
        '''
        bounding_box = ""
        if onlinetweetsappv9.vars['region'] == 'West USA':
            bounding_box = "-125.00,24.94,-95.50,49.59"
        else:
            bounding_box = "-95.50,24.94,-66.93,49.59"
        return bounding_box
    
    def tweet_generator():
        ''' generates tweets in lowercase ascii with no weird characters
        '''
        bounding_box = pick_location()
        stream = requests.post('https://stream.twitter.com/1.1/statuses/filter.json?track=weed,marihuana&language=en',
                         auth=auth,
                         stream=True,
                         data={"locations" : bounding_box})
    
        for line in stream.iter_lines():
            if not line:  # filter out keep-alive new lines
                continue
            tweet = simplejson.loads(line)
            if 'text' in tweet:
                yield tweet['text'].encode('ascii', 'ignore').strip().lower()
            
    all_tweets = []
    def generate_1_tweet():
        ''' uses tweet generator to return 1 tweet
        '''
        for tweet in islice(tweet_generator(), 1): # returns 1st tweet
            return all_tweets.append(tweet)
    number_of_tweets = 5   
    def generate_x_tweets():
        ''' generates a desired number of tweets
        '''
        count = number_of_tweets
        while count > 0:
           generate_1_tweet()
           count = count - 1   
    generate_x_tweets()
    
    """COUNT TWEETS
    """
    countables = ["weed", "marihuana", "stoned", "pot", "#weed", "#marihuana", "#stoned", "#pot"]      
    def search_in_a_list(list):
        ''' 
        takes a list
        compares it with another list
        returns a number of times there is a match
        ''' 
        search_in = countables
        count = 0
        for lis in search_in:
            for li in list:
                if (lis == li):
                    count = count + 1
        return count
    
    def sentences_to_words(list):
        ''' 
        takes a list of (sentences) strings
        returns a list of (words) strings
        ''' 
        pre_words = []
        words = []
    
        def to_pre_words(list):
            for li in list:
                li = li.split(" ")
                pre_words.append(li)

        def to_words(list):
            for li in pre_words:
                for l in li:
                    words.append(l)
        to_pre_words(list) 
        to_words(list)
        results = search_in_a_list(words)
        
        return results
           
    """MAKE GRAPH
    """
    t = sentences_to_words(all_tweets) 
    tit = onlinetweetsappv9.vars['region']
    plot = figure(title=tit, plot_width=300,plot_height=300)
    plot.annulus(x=t, y=t, color="#7FC97F", inner_radius=0.2, outer_radius=0.5)
    script, div = components(plot, CDN)
    
    """RENDER TEMPLATE
    """
    g = all_tweets
    ch = onlinetweetsappv9.vars['region']
    
    return render_template('graph.html', graph=g, choice=ch, script=script, div=div)

if __name__ == '__main__':
    onlinetweetsappv9.run(port=33507)
