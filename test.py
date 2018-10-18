import time
from elasticsearch import Elasticsearch

INDEX = 'package_processing'
TYPE = 't_'


def create_index(es):
    body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,

            "analysis": {
                "tokenizer": {
                    "ngram_tokenizer": {
                        "type": "ngram",
                        "min_gram": 6,
                        "max_gram": 49
                    }
                },
                "analyzer": {
                    "ngram_tokenizer_analyzer": {
                        "type": "custom",
                        "tokenizer": "ngram_tokenizer"
                    }
                }
            }
        },
        "mappings": {
            "t_": {
                "properties": {
                    "type": {
                        "type": "text",
                        "analyzer": "ngram_tokenizer_analyzer"
                    },
                    "3gram_1": {
                        "type": "text",
                        "analyzer": "ngram_tokenizer_analyzer"
                        # "term_vector": "yes",
                    },
                    "3gram_2": {
                        "type": "text",
                        "analyzer": "ngram_tokenizer_analyzer"
                        # "term_vector": "yes",
                    },
                }
            }
        }
    }
    es.indices.create(INDEX, body=body)


def populate(es):
    # 54321abcd9876efgh
    doc1 = {'3gram_1': 'abcd9876efgh'}
    es.index(index=INDEX, doc_type=TYPE, body=doc1, id=1)
    doc2 = {'3gram_2': '541243cdab7698ghef'}
    es.index(index=INDEX, doc_type=TYPE, body=doc2, id=2)
    ###
    doc3 = {'3gram_1': '789barcode'}
    es.index(index=INDEX, doc_type=TYPE, body=doc3, id=3)
    doc4 = {'3gram_2': '790barcode'}
    es.index(index=INDEX, doc_type=TYPE, body=doc4, id=4)


if __name__ == '__main__':
    query = \
        {
            "size": 1,
            "query": {
                "bool": {
                    "should": [
                        {"match": {"3gram_1": "54321abcd9876efgh"}},
                        {"match": {"3gram_2": "54321abcd9876efgh"}}
                    ]
                }
            }
        }
    time.sleep(10)
    es = Elasticsearch(['http://es:9200'])
    create_index(es)
    populate(es)
