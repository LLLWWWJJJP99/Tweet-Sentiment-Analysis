from stanfordcorenlp import StanfordCoreNLP
import json, re


class Analyst(object):
    my_nlp = StanfordCoreNLP(r'/home/davidli/Documents/stanford-corenlp-full-2018-02-27', memory='8g')

    @staticmethod
    def analyze(sentence):
        '''
        Connect to StanfordCoreNLP to get the sentiment analysis for each tweet
        :param sentence:
        :return:
        '''
        res = Analyst.my_nlp.annotate(sentence, properties={
            'annotators': 'sentiment',
            'outputFormat': 'json',
            'timeout': '50000'
        }).strip()
        if not res:
            return "None"
        else:
            res = json.loads(res)
            if res['sentences']:
                return res['sentences'][0]['sentiment']
            else:
                return "None"


if __name__ == '__main__':
    nlp = Analyst.my_nlp
    print(Analyst.analyze(r'Guangdong University of Foreign Studies is located in Guangzhou.'))
    nlp.close()
