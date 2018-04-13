# -*- coding: utf-8 -*-

import requests
from elasticsearch import Elasticsearch


class ElasticSearch(object):
    def __init__(self):
        self.host = None
        self.port = None
        self.index_name = None
        self.doc_type = None
        self.index_mapper = None
        self.instance = self.connect()

    def connect(self) -> Elasticsearch:
        return Elasticsearch(
            [{'host': self.host, 'port': self.port}]
        )

    def create_index(self):
        return self.instance.indices.create(
            index=self.index_name,
            body=self.index_mapper
        )

    def delete_index(self):
        return self.instance.indices.delete(
            index=self.index_name
        )

    def check_index(self):
        if not self.instance.indices.exists(self.index_name):
            return self.create_index()
        return True

    def refresh_index(self):
        self.instance.indices.refresh(index=self.index_name)

    def flush_index(self):
        self.instance.indices.flush(index=self.index_name)

    def search(self, body: dict) -> dict:
        self.check_index()
        ret = []
        matches = self.instance.search(
            index=self.index_name,
            doc_type=self.doc_type,
            body=body,
            filter_path=[
                'hits.hits._id',
                'hits.hits._source'
            ]
        )
        if 'hits' in matches:
            for match in matches['hits']['hits']:
                ret.append(match['_source'])
        return ret

    def fetch_all(self) -> dict:
        self.check_index()
        return self.search(
            {
                'query': {
                    'match_all': {}
                }
            }
        )

