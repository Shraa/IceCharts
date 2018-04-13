# -*- coding: utf-8 -*-

import requests


def do_init_grids(url: str):
    do_delete('{}'.format(url))
    do_post('{}'.format(url), GRIDS)

def do_init_cells(url: str):
    do_delete('{}'.format(url))
    for grid in GRIDS:
        cells = []
        for cell in CELLS:
            if cell['grid_id'] == grid['id']:
                cells.append(cell)
        do_post("{0}/{1}".format(url, grid['id']), cells)


def do_delete(url: str):
    return requests.delete(url='{}'.format(url))


def do_get(url: str):
    return requests.get(url='{}'.format(url))


def do_post(url: str, json: dict):
    return requests.post(url='{}'.format(url), json=json)


def do_put(url: str, data: str):
    return requests.put(url='{}'.format(url), data='{}'.format(data), headers={'Content-type': 'application/json'})


def do_search(key: str, value: str, grids: dict):
    for grid in grids:
        if grid[key] == value:
            return grid


GRIDS = [
    {
        'id': '33f62123-6bca-4863-9bbb-320302056410',
        'name': 'Северный морской путь',
        'description': 'The Northern Sea Route'
    },
    {
        'id': 'c545ffa7-cf78-4c9b-aba1-b763f08507b7',
        'name': 'Caspian Sea',
        'description': 'The northern part of the Caspian Sea'
    },
    {
        'id': '1b1a21b2-fb11-4449-9d86-7295f4bb4aa2',
        'name': 'Black Sea',
        'description': 'Black and Azov Seas'
    }
]


CELLS = [
    {
        'id': 'cfaad02c-f968-48b4-960e-904e69a665aa',
        'grid_id': '33f62123-6bca-4863-9bbb-320302056410',
        'name': 'cell #1',
        'description': "Cell #1 for grid 'Северный морской путь'"
    },
    {
        'id': '6880bc26-ed0b-4154-9537-b4e01332401b',
        'grid_id': '33f62123-6bca-4863-9bbb-320302056410',
        'name': 'cell #2',
        'description': "Cell #2 for grid 'Северный морской путь'"
    },
    {
        'id': '6dbe782f-8a5b-4605-8596-1ad30fce2016',
        'grid_id': '33f62123-6bca-4863-9bbb-320302056410',
        'name': 'cell #3',
        'description': "Cell #3 for grid 'Северный морской путь'"
    },
    {
        'id': '474c32df-63ec-461c-98d7-5e367f7cc963',
        'grid_id': 'c545ffa7-cf78-4c9b-aba1-b763f08507b7',
        'name': 'cell #a',
        'description': "cell #a for grid 'Caspian Sea'"
    },
    {
        'id': '2945d952-f94f-438b-ab37-f292e960f5de',
        'grid_id': 'c545ffa7-cf78-4c9b-aba1-b763f08507b7',
        'name': 'cell #b',
        'description': "cell #b for grid 'Caspian Sea'"
    },
    {
        'id': '2a1a89dc-b5c0-41ad-a2d3-7ebabdade04e',
        'grid_id': '1b1a21b2-fb11-4449-9d86-7295f4bb4aa2',
        'name': 'cell I',
        'description': "cell I for grid 'Black Sea'"
    },
    {
        'id': '9ba86f1c-b4c7-4457-b3c6-f2fe50f1b59a',
        'grid_id': '1b1a21b2-fb11-4449-9d86-7295f4bb4aa2',
        'name': 'cell II',
        'description': "cell II for grid 'Black Sea'"
    },
    {
        'id': '06c55cc5-e421-4972-b98c-f45783bf4665',
        'grid_id': '1b1a21b2-fb11-4449-9d86-7295f4bb4aa2',
        'name': 'cell III',
        'description': "cell III for grid 'Black Sea'"
    },
    {
        'id': '6ff6deff-7963-4365-85cd-65e238e394c1',
        'grid_id': '1b1a21b2-fb11-4449-9d86-7295f4bb4aa2',
        'name': 'cell IV',
        'description': "cell IV for grid 'Black Sea'"
    }
]


DELETE_INDEX_RESPONSE = {
    'acknowledged': True
}
