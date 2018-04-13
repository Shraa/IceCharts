# -*- coding: utf-8 -*-

from app.models import ElasticSearch
from app.models.mappers import cell_mapper


class Cells(ElasticSearch):
    def __init__(self):
        self.host = 'localhost'
        self.port = '9200'
        self.index_name = 'cells'
        self.doc_type = 'cell'
        self.index_mapper = cell_mapper
        self.instance = self.connect()

    def get(self, grid_id: str, **kwargs) -> dict:
        # if id in kwargs:
        #     return self.fetch_by_params({'grid_id': grid_id, 'id': kwargs[id]})
        return self.fetch_by_param(key='grid_id', value=grid_id)

    def get_all(self, grid_id=None) -> dict:
        self.check_index()
        if grid_id:
            return self.fetch_by_param(key='grid_id', value=grid_id)
        else:
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
        cell = self.fetch_by_param('id', id)
        if cell:
            return True
        return False

    def exists_by_name(self, grid_id: str, name: str) -> bool:
        self.check_index()
        cell = self.fetch_by_params({'grid_id': grid_id, 'name': name})
        if cell:
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

    def fetch_by_params(self, params: dict) -> dict:
        self.check_index()
        filter = []
        for key, value in params.items():
            filter.append(
                {
                    'match': {
                        key: {
                            'query': value,
                            'operator': 'and'
                        }
                    }
                }
            )
        matches = self.search(
            {
                'query': {
                    'bool': {
                        'should': filter
                    }
                }
            }
        )
        for match in matches:
            if all(item in match.items() for item in params.items()):
                return match
            else:
                return []
