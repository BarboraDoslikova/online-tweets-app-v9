# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 14:30:08 2015
@author: BD

The main script to run the Online Tweets App.
"""

from flask import Flask, render_template, request, redirect
onlinetweetsappv2 = Flask(__name__)

import pandas as pd
from bokeh.embed import components
from bokeh.charts import Bar
from bokeh.resources import CDN

import app_functions  # My own

onlinetweetsappv2.vars = {}
onlinetweetsappv2.vars["regions_offered"]=["WestUSA","EastUSA", "Canada"]

@onlinetweetsappv2.route("/", methods=["GET", "POST"])
def redirecting():
    return redirect("/main")
   
@onlinetweetsappv2.route("/main", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        a1, a2, a3 = onlinetweetsappv2.vars["regions_offered"]
        return render_template("form.html", ans1=a1, ans2=a2, ans3=a3)
    else:
        # request was a POST
        onlinetweetsappv2.vars["regions_selected"] = request.form.getlist("region")
        return redirect("/graph")

@onlinetweetsappv2.route("/graph", methods=["GET", "POST"])
def graph():     
    """GENERATE TWEETS
    """
    my_list = onlinetweetsappv2.vars["regions_selected"]
          
    all_tweets = []  # Has to be here, not in app_functions.
       
    def generate_1_tweet(my_list):
        """Uses tweet generator from my app_functions module
        to append 1 tweet to all_tweets.
        """
        for tweet in app_functions.tweet_generator(my_list): # returns 1st tweet
            return all_tweets.append(tweet)        
        
    def generate_x_tweets(my_list):
        """ Generates a desired number of tweets.
        I.e. Runs the tweet generator x-times.
        """ 
        NUMBER_OF_TWEETS = 10 
        count = NUMBER_OF_TWEETS
        while count > 0:
           generate_1_tweet(my_list)
           count = count - 1
    
    def main_function(my_list):
        data = {}
        for each in my_list:
            if each == "WestUSA":
                generate_x_tweets(each)
                li = app_functions.count_matches(all_tweets)
                data.update({"WestUSA":li})
            elif each == "EastUSA":
                generate_x_tweets(each)
                li = app_functions.count_matches(all_tweets)
                data.update({"EastUSA":li})
            elif each == "Canada":
                generate_x_tweets(each)
                li = app_functions.count_matches(all_tweets)
                data.update({"Canada":li})
        return data
    
    
    """MAKE GRAPH
    """
    data = main_function(my_list)    
    df = pd.DataFrame(data.items(), columns=["region", "count"])
    plot = Bar(df, "region", values="count", title="Selected Regions")
    
    
    """RENDER TEMPLATE
    """
    script, div = components(plot, CDN)
    g = all_tweets
    
    pre_choice = onlinetweetsappv2.vars["regions_selected"]
    pr_choice = [str(x) for x in pre_choice]
    choice = " & ".join(str(x) for x in pr_choice)    
    
    return render_template("graph.html", graph=g, choice=choice, script=script, div=div)

if __name__ == "__main__":
    onlinetweetsappv2.run(debug=True)