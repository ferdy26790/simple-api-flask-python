from model import *
from flask_bcrypt import Bcrypt

def register_user(app, user_data):
    username = user_data['username']
    password = user_data['password']
    email = user_data['email']

    if not username or not password or not email:
        return 'all field must be filled'
    
    bcrypt = Bcrypt(app)
    password_hash = bcrypt.generate_password_hash(password)

    new_user = User(username=username, email=email, password=password_hash)
    new_user.save()
    return 'add user success'
