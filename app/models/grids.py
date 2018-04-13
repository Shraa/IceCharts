# -*- coding: utf-8 -*-

from app.models import ElasticSearch
from app.models.mappers import grid_mapper


class Grids(ElasticSearch):
    def __init__(self):
        self.host = 'localhost'
        self.port = '9200'
        self.index_name = 'grids'
        self.doc_type = 'grid'
        self.index_mapper = grid_mapper
        self.instance = self.connect()

    def get(self, id: str):
        self.check_index()
        grid = self.fetch_by_param('id', id)
        # if grid['id'] == id:
        if grid:
            return grid
        return []

    def get_all(self):
        self.check_index()
        return self.fetch_all()

    def put(self, id: str, doc: dict):
        self.check_index()
        ret = self.instance.index(
            index=self.index_name,
            doc_type=self.doc_type,
            body=doc,
            id=id
        )['result']
        self.flush_index()
        return ret

    def delete(self, id: str):
        self.check_index()
        ret = 'Not Found'
        if self.exists_by_id(id):
            ret = self.instance.delete(
                index=self.index_name,
                doc_type=self.doc_type,
                id=id
            )
            self.flush_index()
        return ret

    def exists_by_id(self, id: str) -> bool:
        self.check_index()
        grid = self.fetch_by_param('id', id)
        if grid:
            return True
        return False

    def exists_by_name(self, name: str) -> bool:
        self.check_index()
        grid = self.fetch_by_param('name', name)
        if grid:
            return True
        return False

    def fetch_by_param(self, key: str, value: str) -> dict:
        self.check_index()
        matches = self.search(
            {
                'query': {
                    'match': {
                        key: {
                            'query': value,
                            'operator': 'and'
                        }
                    }
                }
            }
        )
        for match in matches:
            if match[key] == value:
                return match
        else:
            return []
