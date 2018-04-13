# -*- coding: utf-8 -*-

import copy
import json
import unittest
import uuid

from test import do_init_grids, do_get, do_delete, do_put, do_search, GRIDS


class TestGridService(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5000'
        self.service = 'grid'

    def test_get_grids(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        good_responses = copy.deepcopy(GRIDS)
        for good_response in good_responses:
            ret = do_get('{0}/{1}/{2}'.format(self.url, self.service, good_response['id']))
            self.assertEqual(ret.json(), good_response)
            self.assertEqual(ret.status_code, 200)

    def test_get_grid_not_found(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        for i in range(10):
            ret = do_get('{0}/{1}/{2}'.format(self.url, self.service, str(uuid.uuid4())))
            self.assertEqual(ret.json(), str('Not found'))
            self.assertEqual(ret.status_code, 404)

    def test_put_grids(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        requests = copy.deepcopy(GRIDS)
        good_responses = copy.deepcopy(GRIDS)
        for good_response in good_responses:
            good_response['status'] = 'updated'
        for request in requests:
            good_response = do_search('id', request['id'], good_responses)
            ret = do_put('{0}/{1}/{2}'.format(self.url, self.service, request['id']), json.dumps(request))
            self.assertEqual(ret.json(), good_response)
            self.assertEqual(ret.status_code, 200)

    def test_put_new_grid(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        request = {
            'id': str(uuid.uuid4()),
            'name': 'grid',
            'description': 'one more grid'
        }
        good_response = copy.deepcopy(request)
        good_response['status'] = 'created'
        ret = do_put('{0}/{1}/{2}'.format(self.url, self.service, request['id']), json.dumps(request))
        self.assertEqual(ret.json(), good_response)
        self.assertEqual(ret.status_code, 200)

    def test_put_grid_without_id_in_body(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        requests = copy.deepcopy(GRIDS)
        for request in requests:
            request.pop('id')
        good_responses = copy.deepcopy(GRIDS)
        for good_response in good_responses:
            good_response['status'] = 'updated'
        for grid in GRIDS:
            request = do_search('name', grid['name'], requests)
            good_response = do_search('name', grid['name'], good_responses)
            ret = do_put('{0}/{1}/{2}'.format(self.url, self.service, grid['id']), json.dumps(request))
            self.assertEqual(ret.json(), good_response)
            self.assertEqual(ret.status_code, 200)

    def test_put_grid_with_new_id(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        requests = copy.deepcopy(GRIDS)
        for request in requests:
            request['id'] = str(uuid.uuid4())
        good_responses = copy.deepcopy(requests)
        for good_response in good_responses:
            good_response['status'] = 'updated'
        for request in requests:
            good_response = do_search('id', request['id'], good_responses)
            ret = do_put('{0}/{1}/{2}'.format(self.url, self.service, request['id']), json.dumps(request))
            self.assertEqual(ret.json(), good_response)
            self.assertEqual(ret.status_code, 200)

    def test_put_grids_id_not_match(self):
        # TODO: Break the testcase into subtests
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        requests = copy.deepcopy(GRIDS)
        good_responses = copy.deepcopy(requests)
        for good_response in good_responses:
            good_response['status'] = "the parameters id and doc['id'] do not match"
        for request in requests:
            good_response = do_search('id', request['id'], good_responses)
            ret = do_put('{0}/{1}/{2}'.format(self.url, self.service, str(uuid.uuid4())), json.dumps(request))
            self.assertEqual(ret.json(), good_response)
            self.assertEqual(ret.status_code, 400)
        requests = copy.deepcopy(GRIDS)
        for request in requests:
            request['id'] = str(uuid.uuid4())
        good_responses = copy.deepcopy(requests)
        for good_response in good_responses:
            good_response['status'] = "the parameters id and doc['id'] do not match"
        for request in requests:
            grid = do_search('name', request['name'], GRIDS)
            good_response = do_search('id', request['id'], good_responses)
            ret = do_put('{0}/{1}/{2}'.format(self.url, self.service, grid['id']), json.dumps(request))
            self.assertEqual(ret.json(), good_response)
            self.assertEqual(ret.status_code, 400)

    def test_delete_grids(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        requests = copy.deepcopy(GRIDS)
        good_responses = copy.deepcopy(requests)
        for good_response in good_responses:
            good_response['status'] = 'deleted'
        for request in requests:
            good_response = do_search('id', request['id'], good_responses)
            ret = do_delete('{0}/{1}/{2}'.format(self.url, self.service, request['id']))
            self.assertEqual(ret.json(), good_response)
            self.assertEqual(ret.status_code, 200)

    def test_delete_grid_not_found(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        for i in range(10):
            ret = do_delete('{0}/{1}/{2}'.format(self.url, self.service, str(uuid.uuid4())))
            self.assertEqual(ret.json(), str('Not found'))
            self.assertEqual(ret.status_code, 404)


if __name__ == '__main__':
    unittest.main()
