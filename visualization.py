from elasticsearch import Elasticsearch
from datetime import datetime as dt


class Visualizer(object):
    INDEX_NAME = "twitter"
    TYPE_NAME = "tweets"
    ID_FILE = 0
    ES_HOST = {"host": "localhost", "port": 9200}
    header = ['geo', 'content', 'sentiment', 'time']
    es = Elasticsearch(hosts=[ES_HOST], http_auth="elastic:elastic")

    @staticmethod
    def init():
        '''
        if index already exits, then delete it. And recreate the index with correct mapping
        :return:
        '''
        if Visualizer.es.indices.exists(Visualizer.INDEX_NAME):
            print("deleting '%s' index..." % Visualizer.INDEX_NAME)
            res = Visualizer.es.indices.delete(index=Visualizer.INDEX_NAME)
            print(" response: '%s'" % res)
        request_body = {
            "settings": {
                "number_of_shards": 2,
                "number_of_replicas": 2
            },
            "mappings": {
                "tweets": {
                    "properties": {
                        "time": {
                            "type": "date",
                            "format": "MM/dd/yyyy HH:mm:ss"
                        },
                        "geo": {
                            "properties": {
                                "coordinates": {
                                    "type": "geo_point"
                                }
                            }
                        }
                    }
                }
            }
        }

        print("creating '%s' index..." % Visualizer.INDEX_NAME)
        res = Visualizer.es.indices.create(index=Visualizer.INDEX_NAME, body=request_body)
        print(" response for create: '%s'" % res)

    @staticmethod
    def upload(source):
        '''
        reformat data and
        upload data in json object
        :param source:
        :return:
        '''
        bulk_data = []
        for tup in source:
            data_dict = {}
            location = tup[0].split(",")

            data_dict[Visualizer.header[0]] = {"coordinates": {"lat": float(location[1]), "lon": float(location[0])}}

            for i in range(1, len(tup)):
                data_dict[Visualizer.header[i]] = tup[i]
            data_dict[Visualizer.header[-1]] = dt.now().strftime("%m/%d/%Y %H:%M:%S")
            op_dict = {
                "index": {
                    "_index": Visualizer.INDEX_NAME,
                    "_type": Visualizer.TYPE_NAME,
                    "_id": Visualizer.ID_FILE
                }
            }
            Visualizer.ID_FILE += 1
            bulk_data.append(op_dict)
            bulk_data.append(data_dict)

        res = Visualizer.es.bulk(index=Visualizer.INDEX_NAME, body=bulk_data, refresh=True)
        print(" response for bulk: '%s'" % res)


if __name__ == '__main__':
    Visualizer.init()
    source = [
        ['beijing', 'Hello World', 'good'],
        ['shanghai', 'roasted DUck', 'bad'],
        ['shenzhen', 'petrabbit', 'netural']
    ]
    Visualizer.upload(source)
