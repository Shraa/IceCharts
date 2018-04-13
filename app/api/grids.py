# -*- coding: utf-8 -*-

import uuid
from app.models.grids import Grids

storage = Grids()


def post(info: dict) -> dict:
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
    storage.check_index()
    return storage.delete_index(), 200


def search() -> dict:
    # NOTE: we need to wrap it with list for Python 3 as dict_values is not JSON serializable
    storage.check_index()
    return storage.get_all(), 200
