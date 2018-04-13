# -*- coding: utf-8 -*-

from app.models.grids import Grids


storage = Grids()


def get(id: str):
    storage.check_index()
    grid = storage.get(id)
    if not grid:
        return 'Not found', 404
    else:
        return grid, 200


def put(id: str, info: dict):
    storage.check_index()
    old_id = None
    if 'id' not in info:
        info['id'] = id
    if id != info['id']:
        info['status'] = "the parameters id and doc['id'] do not match"
        return info, 400, {'Content-type': 'application/json', 'charset': 'utf-8'}
    if storage.exists_by_name(info['name']):
        grid = storage.fetch_by_param('name', info['name'])
        if grid:
            old_id = grid['id']
        if id != old_id:
            storage.delete(old_id)
    # TODO: Check all cells and replace old to new grid id
    info['status'] = storage.put(id, info)
    if old_id is not None:
        info['status'] = 'updated'
    return info, 200


def delete(id: str):
    storage.check_index()
    if not storage.exists_by_id(id):
        return 'Not found', 404, {'Content-type': 'application/json', 'charset': 'utf-8'}
    grid = storage.get(id)
    grid['status'] = storage.delete(id)['result']
    return grid, 200
