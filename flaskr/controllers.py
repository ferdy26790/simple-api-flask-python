import json

from flask import jsonify
from .constants import StatusCodes
from .model import *
from .helpers import *
from .services import *

def register_user(app, user_data):
    username = user_data['username']
    password = user_data['password']
    email = user_data['email']

    if not username or not password or not email:
        return 'all field must be filled'
    
    password_hash = generate_password(app, user_data['password'])

    new_user = User(username=username, email=email, password=password_hash)
    new_user.save()
    return 'add user success'

def login_user(app, user_data):
    username = user_data['username']
    password = user_data['password']

    if not username or not password:
        return 'all field must be filled', StatusCodes.HTTP_400_BAD_REQUEST
    
    db_user = User.objects.get(username=username)
    
    if not check_password(app, db_user['password'], password):
        return 'wrong password', StatusCodes.HTTP_400_BAD_REQUEST

    return jsonify(access_token=create_token(username))

def user_detail():
    identity = authenticate_user()
    user = User.objects.get(username=identity)
    return jsonify({
        'username':user['username'],
        'email':user['email']
        })

def get_scrape(insta_account):
    identity = authenticate_user()
    print(identity)
    try:
        data_scrape = scrape_instagram_profile(insta_account, identity)
    except Exception as e:
        return e.__str__(), StatusCodes.HTTP_500_INTERNAL_SERVER_ERROR
    return "successfully load post data to db"

def show_scrape():
    identity = authenticate_user()
    user = User.objects.get(username=identity)
    content = Posts.objects(user_post=str(user.id))
    return content.to_json()
