# -*- coding: utf-8 -*-

import uuid
from app.models.grids import Grids

storage = Grids()


def search() -> dict:
    """
    Summary: Get a list of grids
    Description: Returns a list of available grids for cells with ice maps

    """
    # NOTE: we need to wrap it with list for Python 3 as dict_values is not JSON serializable
    storage.check_index()
    return storage.get_all(), 200


def post(**kwargs) -> dict:
    """
    Summary: Post a list of grids
    Description: Returns the result of importing a list of available grids for cells with ice maps

    """
    info = kwargs.pop('info')
    for grid in info:
        if 'id' not in grid:
            grid['id'] = str(uuid.uuid4())
        if storage.exists_by_name(grid['name']):
            grid['status'] = 'Grid with this name already in index'
        elif storage.exists_by_id(grid['id']):
            grid['status'] = 'Grid with this id already in index'
        else:
            grid['status'] = storage.put(str(grid['id']), grid)
    return info, 200


def delete() -> dict:
    """
    Summary: Drop all grids
    Description: Returns the status of an operation

    """
    storage.check_index()
    return storage.delete_index(), 200
