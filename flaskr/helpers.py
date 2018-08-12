from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity

def generate_password(app, password):
    bcrypt = Bcrypt(app)
    password_hash = bcrypt.generate_password_hash(password)
    return password_hash

def check_password(app, db_password, password):
    bcrypt = Bcrypt(app)
    is_match = bcrypt.check_password_hash(db_password, password)
    return is_match

def create_token(username):
    return create_access_token(identity=username)

def authenticate_user():
    return get_jwt_identity()
    