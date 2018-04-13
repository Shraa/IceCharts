# -*- coding: utf-8 -*-

from app.models.grids import Grids


storage = Grids()


def get(grid_id: str):
    """
    Summary: Get a grid by id
    Description: Returns a grid info

    """
    storage.check_index()
    grid = storage.get(grid_id)
    if not grid:
        return 'Not found', 404
    else:
        return grid, 200


def put(grid_id: str, info: dict):
    """
    Summary: Add or update a grid info by grid id
    Description: Returns the result of adding or updating the grid info by gridID

    """
    storage.check_index()
    old_id = None
    if 'id' not in info:
        info['id'] = grid_id
    if grid_id != info['id']:
        info['status'] = "the parameters id and doc['id'] do not match"
        return info, 400, {'Content-type': 'application/json', 'charset': 'utf-8'}
    if storage.exists_by_name(info['name']):
        grid = storage.fetch_by_param('name', info['name'])
        if grid:
            old_id = grid['id']
        if grid_id != old_id:
            storage.delete(old_id)
    # TODO: Check all cells and replace old to new grid id
    info['status'] = storage.put(grid_id, info)
    if old_id is not None:
        info['status'] = 'updated'
    return info, 200


def delete(grid_id: str):
    """
    Summary: Delete a grid by grid id
    Description: Returns the result of deleting the grid

    """
    storage.check_index()
    if not storage.exists_by_id(grid_id):
        return 'Not found', 404, {'Content-type': 'application/json', 'charset': 'utf-8'}
    grid = storage.get(grid_id)
    grid['status'] = storage.delete(grid_id)['result']
    return grid, 200
