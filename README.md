# online-tweets-app-v9

<h3>What is it?</h3>
A Python application that uses the Flask web framework and Bokeh interactive visualisations, deployed to Heroku.

<h3>What does it do?</h3>
With one click, you can see the number of times marihuana-related words are currently being tweeted in a region of your choice!

<h3>What coud it ultimately do?</h3>
See how much different regions tweet about a topic of your interest.
Example 1: Do people tweet more about marihuana in states where its use is legal?
Example 2: Do people tweet more about your product in places where you focused your marketing campaign?

<h4>How does it do it?</h4>
Get current tweets from Twitter API which mention marihuana.<br>
Tokenize them.<br>
Count the number of times marihuana-related words are used.<br>
Return the number of times marihuana-related words are used in an interactive graph.<br>

<h4>What is the current state of the app?</h4>
At the moment, the user can choose either West or East USA and the app counts marihuana-related words in the current first 5 tweets.<br>
I'm working on including more regions and analyzing more tweets.<br>
My next step is for the user to be able to choose more regions at once and see their comparison.<br>
My final step is for the user to be able to choose any topic of interest and compare the volume of tweets about the topic across different regions.
