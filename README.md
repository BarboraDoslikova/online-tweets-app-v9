# online-tweets-app-v9

<h2>What is it?</h2>
A Python application that uses the Flask web framework and Bokeh interactive visualisations, deployed to Heroku.

<h2>What does it do?</h2>
With one click, you can see the number of times marijuana-related words are currently being tweeted in a region of your choice!

<h2>What coud it ultimately do?</h2>
See how much different regions tweet about a topic of your interest.<br>
Example 1: Do people tweet more about marijuana in states where its use is legal?<br>
Example 2: Do people tweet more about your product in places where you focused your marketing campaign?

<h4>How does it do it?</h4>
1. Get current tweets from Twitter API which mention marijuana.<br>
2. Tokenize them.<br>
3. Count the number of times marijuana-related words are used.<br>
4. Return the number of times marijuana-related words are used in an interactive graph.<br>

<h4>What is the current state of the app?</h4>
1. At the moment, the user can choose from West USA, East USA and Canada. The app counts marijuana-related words in the first 3 tweets in real time.<br>
2. I'm working on analyzing more tweets. However, analyzing the first e.g. 10 tweets per region in real time takes me over the Heroku HTTP 30 second timeout limit. <br>
3. My next step is for the user to be able to choose more regions at once and see their comparison.<br>
4. My ultimate step is for the user to be able to choose any topic of interest and compare the volume of tweets about the topic across different regions.

