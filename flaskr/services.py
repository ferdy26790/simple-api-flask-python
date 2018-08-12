import glob
import instaloader
import json
import os

from instaloader.exceptions import InstaloaderException
from .model import *


def login_instagram(username, password):
    insta_client = instaloader.Instaloader(compress_json=False)
    try:
        print('mo login nih')
        insta_client.login(username,password)
    except InstaloaderException as e:
        raise Exception(e.__str__())
    print(insta_client)
    return insta_client

def scrape_instagram_profile(credentials, identity):
    username = credentials['username']
    password = credentials['password']
    l_insta = login_instagram(username, password)
    profile = instaloader.Profile.from_username(l_insta.context, credentials['username'])
    dirname = 'data/{}/{}'.format(profile.username, 'post')

    path = os.getcwd()
    dir_path = os.path.join(path, dirname)
    l_insta.dirname_pattern=dir_path
    for post in profile.get_posts():
        l_insta.download_post(post, profile.username)

    data = load_post(dir_path)
    user = User.objects.get(username=identity)
    new_post = Posts(content=data, user_post=user)
    new_post.save()

def load_post(dir_path):
    files = glob.glob(dir_path+'/*.json')
    for file in files:
        with open(file, 'r') as f:
            # print(f.read())
            data = json.loads(f.read())
        return data
