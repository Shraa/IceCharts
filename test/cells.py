# -*- coding: utf-8 -*-

import copy
import unittest
import uuid

from random import choice
from string import ascii_letters

from test import do_init_grids, do_init_cells, do_get, do_delete, do_post, GRIDS, CELLS, DELETE_INDEX_RESPONSE


class TestCellsService(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:5000'
        self.service = 'cells'

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
        self.assertEqual(
            ret.json().sort(key=lambda item: item['id']),
            CELLS.sort(key=lambda item: item['id'])
        )
        self.assertEqual(ret.status_code, 200)

    def test_get_filled_base_for_grid(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            ret = do_get('{0}/{1}/{2}'.format(self.url, self.service, grid['id']))
            good_response = []
            for cell in CELLS:
                if cell['grid_id'] == grid['id']:
                    good_response.append(cell)
            self.assertEqual(
                ret.json().sort(key=lambda item: item['id']),
                good_response.sort(key=lambda item: item['id'])
            )
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
            self.assertEqual(
                ret.json().sort(key=lambda item: item['id']),
                good_responses.sort(key=lambda item: item['id'])
            )
            self.assertEqual(ret.status_code, 200)

    def test_post_cells_grid_not_found(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        do_delete('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            request = []
            for cell in CELLS:
                if cell['grid_id'] == grid['id']:
                    request.append(cell)
            ret = do_post("{0}/{1}/{2}".format(self.url, self.service, str(uuid.uuid4())), request)
            self.assertEqual(ret.json(), 'Not found')
            self.assertEqual(ret.status_code, 404)

    def test_post_cells_without_id(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        do_delete('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            request = []
            for cell in CELLS:
                if cell['grid_id'] == grid['id']:
                    cell.pop('id')
                    request.append(cell)
            good_responses = copy.deepcopy(request)
            for good_response in good_responses:
                good_response['status'] = 'created'
            ret = do_post("{0}/{1}/{2}".format(self.url, self.service, grid['id']), request)
            self.assertEqual(
                ret.json().sort(key=lambda item: item['name']),
                good_responses.sort(key=lambda item: item['name'])
            )
            self.assertEqual(ret.status_code, 200)

    def test_post_cells_grid_not_found(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        do_delete('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            request = []
            for cell in CELLS:
                if cell['grid_id'] == grid['id']:
                    cell['grid_id'] = str(uuid.uuid4())
                    request.append(cell)
            good_responses = copy.deepcopy(request)
            for good_response in good_responses:
                good_response['status'] = 'Grid not match'
            ret = do_post("{0}/{1}/{2}".format(self.url, self.service, grid['id']), request)
            self.assertEqual(
                ret.json().sort(key=lambda item: item['id']),
                good_responses.sort(key=lambda item: item['id'])
            )
            self.assertEqual(ret.status_code, 200)

    def test_post_cells_duplicate_by_id(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            request = []
            for cell in CELLS:
                if cell['grid_id'] == grid['id']:
                    request.append(cell)
            good_responses = copy.deepcopy(request)
            for good_response in good_responses:
                good_response['status'] = 'Cell with this id already in index'
            ret = do_post("{0}/{1}/{2}".format(self.url, self.service, grid['id']), request)
            self.assertEqual(
                ret.json().sort(key=lambda item: item['id']),
                good_responses.sort(key=lambda item: item['id'])
            )
            self.assertEqual(ret.status_code, 200)

    def test_post_cells_duplicate_by_name(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            request = []
            for cell in CELLS:
                if cell['grid_id'] == grid['id']:
                    cell['id'] = str(uuid.uuid4())
                    request.append(cell)
            good_responses = copy.deepcopy(request)
            for good_response in good_responses:
                good_response['status'] = 'Cell with this name for the grid already in index'
            ret = do_post("{0}/{1}/{2}".format(self.url, self.service, grid['id']), request)
            self.assertEqual(
                ret.json().sort(key=lambda item: item['id']),
                good_responses.sort(key=lambda item: item['id'])
            )
            self.assertEqual(ret.status_code, 200)

    def test_delete_base(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        ret = do_delete('{0}/{1}'.format(self.url, self.service))
        self.assertEqual(ret.json(), DELETE_INDEX_RESPONSE)
        self.assertEqual(ret.status_code, 200)

    def test_delete_for_grid(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        for grid in GRIDS:
            good_responses = []
            for cell in CELLS:
                if cell['grid_id'] == grid['id']:
                    good_responses.append(cell)
            for good_response in good_responses:
                good_response['status'] = 'deleted'
            ret = do_delete("{0}/{1}/{2}".format(self.url, self.service, grid['id']))
            self.assertEqual(
                ret.json().sort(key=lambda item: item['id']),
                good_responses.sort(key=lambda item: item['id'])
            )
            self.assertEqual(ret.status_code, 200)

    def test_delete_for_grid_not_found(self):
        do_init_grids('{0}/{1}'.format(self.url, str('grids')))
        do_init_cells('{0}/{1}'.format(self.url, self.service))
        for i in range(10):
            ret = do_delete('{0}/{1}/{2}'.format(self.url, self.service, str(uuid.uuid4())))
            self.assertEqual(ret.json(), 'Not found')
            self.assertEqual(ret.status_code, 404)


if __name__ == '__main__':
    unittest.main()
