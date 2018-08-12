import os

from flask import Flask, request
from mongoengine import connect
from .controllers import *
from flask_jwt_extended import JWTManager, jwt_required

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(

    # )
    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    jwt = JWTManager(app)
    connect(
        host = os.getenv('DATABASE')
    )
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
        print(request.form)
        try:
            return register_user(app, request.form)
        except Exception as e:
            return e.message, 500

    @app.route('/login', methods=['POST'])
    def login():
        try:
            return login_user(app, request.form)
        except Exception as e:
            return e.message, 500

    @app.route('/user')
    @jwt_required
    def user():
        try:
            return user_detail()
        except Exception as e:
            return e.message, 500

    @app.route('/scrape', methods=['POST', 'GET'])
    @jwt_required
    def scrape():
        if request.method == 'POST':
            return get_scrape(request.form)
        else:
            return show_scrape()
        # try:
        #     return scrape_instagram_profile(request.form)
        # except Exception as e:
        #     return e.message, 500
    return app