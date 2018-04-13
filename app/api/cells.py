# -*- coding: utf-8 -*-

import requests
import uuid

from app.models.cells import Cells

storage = Cells()


def search() -> dict:
    """
    Summary: Get a list of cells from all grids
    Description: Returns a list of available cells with ice maps from all grids

    """
    storage.check_index()
    return storage.get(), 200
    # return storage.get_all(), 200


def get(**kwargs):
    """
    Summary: Get a list of cells from the grid
    Description: Returns a list of available cells with ice maps from the grid

    """
    storage.check_index()
    grid_id = kwargs.pop('grid_id')
    return storage.get(grid_id=grid_id), 200


def post(**kwargs):
    """
    Summary: Post a list of cells for the grids
    Description: Returns the result of importing a list of cells for the grid

    """
    storage.check_index()
    grid_id = kwargs.pop('grid_id')
    info = kwargs.pop('info')
    grid = storage.get_grid(grid_id=grid_id)
    if grid.status_code == 404:
        return 'Not found', 404
    for cell in info:
        if 'id' not in cell:
            cell['id'] = str(uuid.uuid4())
        if 'grid_id' not in cell:
            cell['grid_id'] = grid_id
        if grid.status_code == 404:
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


def delete_all():
    """
    Summary: Drop all cells
    Description: Returns the status of an operation

    """
    storage.check_index()
    return storage.delete_index(), 200


def delete(**kwargs):
    """
    Summary: Drop all cells from the grid
    Description: Returns the status of an operation

    """
    grid_id = kwargs.pop('grid_id')
    storage.check_index()
    if storage.get_grid(grid_id=grid_id).status_code == 404:
        return 'Not found', 404
    else:
        cells = storage.get(grid_id=grid_id)
        for cell in cells:
            cell['status'] = storage.delete(cell['id'])
        return cells
