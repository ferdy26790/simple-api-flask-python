from mongoengine import Document, StringField, EmailField

class User(Document):
    username = StringField(max_length=50, required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=100, required=True)