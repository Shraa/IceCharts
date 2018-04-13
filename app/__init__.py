# -*- coding: utf-8 -*-

import connexion
import flask
import gevent.monkey

from connexion.resolver import RestyResolver
from flask_injector import FlaskInjector
from time import sleep


gevent.monkey.patch_all()


def get_greeting():
    def generator():
        while True:
            yield 'beat\n\n'
            sleep(5)
    response = flask.Response(generator(), mimetype='text/plain', status=200)
    return response


def main():
    app = connexion.App(__name__, server='gevent', specification_dir='swagger/')
    app.add_api('indexer.yaml', resolver=RestyResolver('app.api'), arguments={'title': 'Sample Ice Chart Service'})
    FlaskInjector(app=app.app)
    app.run(port=5000)
