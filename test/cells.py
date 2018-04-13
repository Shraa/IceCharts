# -*- coding: utf-8 -*-

import copy
import unittest
import uuid

from random import choice
from string import ascii_letters

from test import do_init_grids, do_init_cells, do_get, do_delete, do_post, do_search, GRIDS, CELLS, DELETE_INDEX_RESPONSE


class TestGridsService(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5000'
        self.service = 'cells'

    def test_delete_base(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        ret = do_delete('{0}/{1}'.format(self.url, self.service))
        self.assertEqual(ret.json(), DELETE_INDEX_RESPONSE)
        self.assertEqual(ret.status_code, 200)

    def test_delete_all_for_grid(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        do_delete('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            ret = do_get('{0}/{1}/{2}'.format(self.url, self.service, grid['id']))
            self.assertEqual(ret.json(), [])
            self.assertEqual(ret.status_code, 200)

    def test_get_empty_base(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        do_delete('{0}/{1}'.format(self.url, self.service))
        ret = do_get('{0}/{1}'.format(self.url, self.service))
        self.assertEqual(ret.json(), [])
        self.assertEqual(ret.status_code, 200)

    def test_get_empty_base_for_grid(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        do_delete('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            ret = do_get('{0}/{1}/{2}'.format(self.url, self.service, grid['id']))
            self.assertEqual(ret.json(), [])
            self.assertEqual(ret.status_code, 200)

    def test_get_filled_base(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        ret = do_get('{0}/{1}'.format(self.url, self.service))
        for good_response in CELLS:
            response = do_search('id', good_response['id'], ret.json())
            self.assertEqual(response, good_response)
            self.assertEqual(ret.status_code, 200)

    def test_get_filled_base_for_grid(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            good_response = []
            for cell in CELLS:
                if cell['grid_id'] == grid['id']:
                    good_response.append(cell)
            ret = do_get('{0}/{1}/{2}'.format(self.url, self.service, grid['id']))
            self.assertEqual(ret.json(), good_response)
            self.assertEqual(ret.status_code, 200)


    def test_post_cells(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        do_delete('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            request = []
            for cell in CELLS:
                if cell['grid_id'] == grid['id']:
                    request.append(cell)
            good_responses = copy.deepcopy(request)
            for good_response in good_responses:
                good_response['status'] = 'created'
            ret = do_post("{0}/{1}/{2}".format(self.url, self.service, grid['id']), request)
            for good_response in good_responses:
                response = do_search('id', good_response['id'], ret.json())
                self.assertEqual(response, good_response)
                self.assertEqual(ret.status_code, 200)


if __name__ == '__main__':
    unittest.main()
