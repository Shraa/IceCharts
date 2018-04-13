# -*- coding: utf-8 -*-

import uuid

from multimethod import multimethod

from app.models.grids import Grids
from app.models.cells import Cells
from app.api import do_get_grid

storage = Cells()


"""
Summary: Get a list of cells from all grids
Description: Returns a list of available cells with ice maps from all grids

"""
def search() -> dict:
    # NOTE: we need to wrap it with list for Python 3 as dict_values is not JSON serializable
    storage.check_index()
    return storage.get_all(), 200


"""
Summary: Get a list of cells from the grid
Description: Returns a list of available cells with ice maps from the grid

"""
def get(grid_id: str):
    storage.check_index()
    if not do_get_grid(grid_id):
        return 'Not found', 404
    return storage.get(grid_id=grid_id), 200


def post(grid_id: str, info: dict) -> dict:
    storage.check_index()
    grid = do_get_grid(grid_id)
    if not grid:
        return 'Not found', 404
    for cell in info:
        if 'id' not in cell:
            cell['id'] = str(uuid.uuid4())
        if 'grid_id' not in cell:
            cell['grid_id'] = grid_id
        if not grid:
            cell['status'] = 'Grids not found'
        elif grid_id != cell['grid_id']:
            cell['status'] = 'Grids not match'
        elif storage.exists_by_id(cell['id']):
            cell['status'] = 'Cell with this id already in index'
        elif storage.exists_by_name(grid_id, cell['name']):
            cell['status'] = 'Cell with this name for the grid already in index'
        else:
            cell['status'] = storage.put(str(cell['id']), cell)
    return info, 200


def delete_all() -> dict:
    storage.check_index()
    return storage.delete_index(), 200


def delete(grid_id: str) -> dict:
    storage.check_index()
    if not do_get_grid(grid_id):
        return 'Not found', 404
    else:
        cells = storage.get(grid_id=grid_id)
        for cell in cells:
            cell['status'] = storage.delete(cell['id'])
        return cells
