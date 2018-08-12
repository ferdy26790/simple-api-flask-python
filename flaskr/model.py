from mongoengine import Document, DateTimeField, StringField, EmailField, DictField, ReferenceField
import datetime
class User(Document):
    username = StringField(max_length=50, required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password = StringField(max_length=100, required=True)

class Posts(Document):
    content = DictField(required=True)
    user_post = ReferenceField(User)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)

    search_field=("user_post",)