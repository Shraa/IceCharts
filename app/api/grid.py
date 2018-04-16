# -*- coding: utf-8 -*-

from app.models.grids import Grids


storage = Grids()


def get(** kwargs):
    """
    Summary: Get a grid by id
    Description: Returns a grid info

    """
    grid_id = kwargs.pop('grid_id')

    storage.check_index()
    grid = storage.get(grid_id)
    if not grid:
        return 'Not found', 404
    else:
        return grid, 200


def put(**kwargs):
    """
    Summary: Add or update a grid info by grid id
    Description: Returns the result of adding or updating the grid info by gridID

    """
    grid_id = kwargs.pop('grid_id')
    info = kwargs.pop('info')

    storage.check_index()
    old_id = None
    if 'id' not in info:
        info['id'] = grid_id
    if grid_id != info['id']:
        info['status'] = "the parameters id and doc['id'] do not match"
        return info, 400
    if storage.exists_by_name(info['name']):
        if grid_id != storage.fetch_by_param('name', info['name']).pop('id'):
            info['status'] = "the parameters id can not be changed"
            return info, 400
    info['status'] = storage.put(grid_id, info)
    return info, 200


def delete(**kwargs):
    """
    Summary: Delete a grid by grid id
    Description: Returns the result of deleting the grid

    """
    grid_id = kwargs.pop('grid_id')

    storage.check_index()
    if not storage.exists_by_id(grid_id):
        return 'Not found', 404, {'Content-type': 'application/json', 'charset': 'utf-8'}
    grid = storage.get(grid_id)
    grid['status'] = storage.delete(grid_id)['result']
    return grid, 200
