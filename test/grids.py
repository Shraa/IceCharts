# -*- coding: utf-8 -*-

import copy
import unittest
import uuid

from random import choice
from string import ascii_letters

from test import do_init_grids, do_get, do_delete, do_post, do_search, GRIDS, DELETE_INDEX_RESPONSE


class TestGridsService(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5000'
        self.service = 'grids'

    def test_delete_base(self):
        do_init_grids('{0}/{1}'.format(self.url, self.service))
        ret = do_delete('{0}/{1}'.format(self.url, self.service))
        self.assertEqual(ret.json(), DELETE_INDEX_RESPONSE)
        self.assertEqual(ret.status_code, 200)

    def test_get_empty_base(self):
        do_delete('{0}/{1}'.format(self.url, self.service))
        ret = do_get('{0}/{1}'.format(self.url, self.service))
        self.assertEqual(ret.json(), [])
        self.assertEqual(ret.status_code, 200)

    def test_get_filled_base(self):
        do_init_grids('{0}/{1}'.format(self.url, self.service))
        ret = do_get('{0}/{1}'.format(self.url, self.service))
        for good_response in GRIDS:
            response = do_search('id', good_response['id'], ret.json())
            self.assertEqual(response, good_response)
            self.assertEqual(ret.status_code, 200)

    def test_post_grids(self):
        do_delete('{0}/{1}'.format(self.url, self.service))
        good_responses = copy.deepcopy(GRIDS)
        for good_response in good_responses:
            good_response['status'] = 'created'
        ret = do_post("{0}/{1}".format(self.url, self.service), GRIDS)
        for good_response in good_responses:
            response = do_search('id', good_response['id'], ret.json())
            self.assertEqual(response, good_response)
            self.assertEqual(ret.status_code, 200)

    def test_post_grids_without_id(self):
        do_delete('{0}/{1}'.format(self.url, self.service))
        grids = copy.deepcopy(GRIDS)
        for response in grids:
            response.pop('id')
        good_responses = copy.deepcopy(grids)
        for good_response in good_responses:
            good_response['status'] = 'created'
        ret = do_post('{0}/{1}'.format(self.url, self.service), grids)
        for good_response in good_responses:
            response = do_search('name', good_response['name'], ret.json())
            response.pop('id')
            self.assertEqual(response, good_response)
            self.assertEqual(ret.status_code, 200)

    def test_post_duplicate_by_name(self):
        do_init_grids('{0}/{1}'.format(self.url, self.service))
        good_responses = copy.deepcopy(GRIDS)
        for good_response in good_responses:
            good_response['status'] = 'Grid with this name already in index'
        ret = do_post('{0}/{1}'.format(self.url, self.service), GRIDS)
        for good_response in good_responses:
            response = do_search('id', good_response['id'], ret.json())
            self.assertEqual(response, good_response)
            self.assertEqual(ret.status_code, 200)

    def test_post_duplicate_by_id(self):
        do_init_grids('{0}/{1}'.format(self.url, self.service))
        requests = copy.deepcopy(GRIDS)
        for request in requests:
            request['name'] = ''.join(choice(ascii_letters) for i in range(12))
        good_responses = copy.deepcopy(requests)
        for good_response in good_responses:
            good_response['status'] = 'Grid with this id already in index'
        ret = do_post('{0}/{1}'.format(self.url, self.service), requests)
        for good_response in good_responses:
            response = do_search('id', good_response['id'], ret.json())
            self.assertEqual(response, good_response)
            self.assertEqual(ret.status_code, 200)


if __name__ == '__main__':
    unittest.main()
