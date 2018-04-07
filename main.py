from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from SentimentAnalyst import Analyst
from visualization import Visualizer
import re

TCP_IP = 'localhost'
TCP_PORT = 50010


def analyze(iters):
    '''
    :param iters: tweets in each partition
    :return: sentiment analysis and tweets in each partition
    '''
    res = []
    for sentence in iters:
        res.append((sentence, Analyst.analyze(sentence)))
    return iter(res)


def seperate_tweets(iters):
    '''
    :param iters: tweets in each partition
    :return: partition of tweets seperated by |, which is real tweets
    '''
    strs = ''
    for tweet in iters:
        strs += tweet
    res = strs.split(r'|')
    return iter(res[1:len(res) - 1])


def format_data(tup):
    '''
    :param tup: extract location from content
    :return: tuple containing coordinate, content, sentiment
    '''
    tweet = tup[0]
    m = re.search(r'^\((.+)\).+', tweet)
    addr = ""
    if m: addr = m.group(1)
    offset = tweet.find(")") + 1
    content = tweet[offset:]
    return addr, content, tup[1]


def upload_to_kibana(iters):
    '''
    setup connection to kibana and upload data
    :param iters: tweets in each partition
    :return: None
    '''
    res = list(iters)
    if not len(res): return
    Visualizer.upload(res)


if __name__ == '__main__':
    sc = SparkContext('local[2]', 'TwitterApp')
    ssc = StreamingContext(sc, 4)
    ssc.checkpoint(r'./checkpoint')
    streams = ssc.socketTextStream(TCP_IP, TCP_PORT)
    # windowed stream and combine data in each rdd then devide tweet correctly
    windowed_stream = streams.window(4, 4).repartition(1)
    corrected_stream = windowed_stream.mapPartitions(lambda iters: seperate_tweets(iters), preservesPartitioning=False)
    # fileter out tweets which have no coordinates
    corrected_stream = corrected_stream.filter(lambda x: re.search('\\(.+\\)', x))
    sentiments = corrected_stream.filter(lambda x: len(x) > 0).\
        mapPartitions(lambda iters: analyze(iters), preservesPartitioning=False)

    reformat_stream = sentiments.map(lambda tup: format_data(tup))
    reformat_stream.pprint()

    reformat_stream.foreachRDD(lambda rdd: rdd.foreachPartition(upload_to_kibana))

    Visualizer.init()
    ssc.start()
    ssc.awaitTermination()
    Analyst.my_nlp.close()
