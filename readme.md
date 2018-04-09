# Tweet Sentiment Analysis Project
This project deals with real-time streaming data arriving from twitter streams.

## ** 1.Task.**
I implement the following framework using Apache Spark Streaming, StandfordCoreNLP, Twitter Developer Restful API, 
ElasticSearch and Kibana. The framework performs sentiment analysis
of particular hashtags in twitter data in real time. For example, we want to do the
sentiment analysis for all the tweets for #guncontrolnow and show their
(e.g.,positive, neutral, negative) statistics in Kibana.

For this, I get the tweets via scrapper. Next, I write a
sentiment analysis program to predict sentiment of the tweet message. Finally, I
 visualize Ir fndings using ElasticSearch/Kibana.

Scrapper -> Sentiment Analyzer/Common topic finder -> Visualizer
(ElasticSearch/Kibana)

### Module Details

### **1) Scrapper**

**We provide a sample scrapper (stream.py). However, I need to extend
the code to support the following functionality.**


The scrapper collects tweets and pre-process them for analytics. It is a standalone
program written in Python by using twitter dev restful api and should perform the following:

1. Collect tweets in real-time with particular hashtag. For example, I
    collect all tweets with #guncontrolnow.
2. After getting tweets, I fliter them by removing emoji symbols and special
    characters and discard any noisy tweet that do not belong to
    #guncontrolnow. Note that the returned tweet contains both the meta data
    (e.g., location) and text contents. I have to keep at least the text
    content and the location meta data.
3. After fltering, I convert the location meta data of each tweet back
    to its geolocation info by calling google geo API and send the text and
    geolocation info to spark streaming.
4. My scrapper program  run infnitely and should take hash tags as
    input parameters while running.

### **2) Sentiment Analyzer**

Sentiment Analyzer determines whether a piece of tweet is positive, neutral or
negative. For example,

I use any third-party sentiment analyzer like Stanford CoreNLP for
sentiment analyzing.

In summary, for each hashtag, I perform sentiment analysis using sentiment
analysis tools discussed above and output sentiment and geolocation of each tweet
to some external bases (either save in a json fle or send them to kibana for
visualization).

### **3) Visualizer**

I install ElasticSearch and Kibana. Create an index for visualization. Create a data
table to show the sentiment of each tweet, i.e., "sentiment | tweet". Then, create a
number of geo coordinate maps to show the geolocation distribution of tweets. More
specifcally, frst geo coordinate map show the geolocation distribution of all tweets,
regardless of sentiment related to #guncontrolnow. Second and Third geo coordinate map
show geolocation distributions of positive tweets and negative tweets, respectively.
When I send data from spark to ElasticSearch, I need to add a time stamp. In
the dashboard, set the refresh time to 2 min as an example.

## ** 2.How to run it.**
1. Install tweepy, standfordcorenlp, googlemap and kibana packages in your ide.
2. Install elasticsearch and kibana locally.
3. run MyScraper.py firstly and then run main.py.
4. If you have already install kibana or used kibana cloud, you can access my bashboard at
[My Tweets Bashboard](http://localhost:5601/app/kibana#/dashboard/cd2e2440-3945-11e8-a3f7-19e82329e45b?_g=(refreshInterval:(display:Off,pause:!f,value:0),time:(from:'2015-05-18T05:00:00.000Z',mode:absolute,to:'2015-05-21T04:59:59.999Z'))&_a=(description:'',filters:!(),fullScreenMode:!f,options:(darkTheme:!f,hidePanelTitles:!f,useMargins:!t),panels:!((gridData:(h:3,i:'1',w:6,x:0,y:0),id:eddeec60-3940-11e8-a3f7-19e82329e45b,panelIndex:'1',type:visualization,version:'6.2.3'),(embeddableConfig:(mapCenter:!(48.3416461723746,-47.81250000000001),mapZoom:2),gridData:(h:3,i:'2',w:6,x:6,y:0),id:'1ab754c0-3941-11e8-a3f7-19e82329e45b',panelIndex:'2',type:visualization,version:'6.2.3'),(embeddableConfig:(mapCenter:!(38.28993659801203,-100.986328125),mapZoom:5),gridData:(h:3,i:'3',w:6,x:0,y:3),id:'6d2e04b0-3941-11e8-a3f7-19e82329e45b',panelIndex:'3',type:visualization,version:'6.2.3')),query:(language:lucene,query:''),timeRestore:!f,title:Twitter_Sentiment_Analysis_Dashboard,viewMode:view))

Bashboard Screenshot
![alt text](https://github.com/DavidLi210/Tweet-Sentiment-Analysis/bashboard.png "Bashboard Screenshot")
```
feel free to email me about how to run the project. My email: wxl163530@gmail.com
```
