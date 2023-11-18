import configparser
import pathlib

from mongoengine import Document, StringField, ListField, ReferenceField
from mongoengine import connect

file_config = pathlib.Path(__file__).parent.parent.joinpath('config.ini')
config = configparser.ConfigParser()
config.read(file_config)

host = config.get("DEV_DB", "HOST")
db = config.get("DEV_DB", "DB_NAME")

connect(db=db, host=host)


class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=100)
    born_location = StringField()
    description = StringField()
    meta = {'collection': 'authors'}


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)
    meta = {'collection': 'quotes'}
