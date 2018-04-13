# -*- coding: utf-8 -*-

import requests


def do_get_grid(id: str):
    url = 'http://localhost:5000/grid'
    return requests.get(url='{}/{}'.format(str(url), str(id)))
