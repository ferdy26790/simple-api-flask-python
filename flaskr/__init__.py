import os

from flask import Flask, request
from mongoengine import connect
from controllers import *

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(

    # )
    connect('flask-simple-api')
    print('database connected')
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/register', methods=['POST'])
    def register():
        try:
            return register_user(app, request.form)
        except Exception as e:
            return e.message, 500
    return app